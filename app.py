"""
Enhanced Flask application for Portkey food ordering app.
Includes simplified payment system and ML chatbot integration.
"""

import os
import hashlib
import secrets
from datetime import datetime, timedelta
from decimal import Decimal
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_mail import Mail, Message
from dotenv import load_dotenv
from db import SessionLocal
from models import Restaurant, MenuItem, CartItem, User, Order, OrderItem, Feedback, DeliveryFeedback
from chatbot import chatbot
from functools import wraps

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', os.urandom(24))
app.config['SESSION_TYPE'] = 'filesystem'

# Email configuration
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'True').lower() == 'true'
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER', app.config['MAIL_USERNAME'])

mail = Mail(app)

# Currency conversion rate (USD to INR) - simplified to 1:1 for this demo
USD_TO_INR = 1.0

def hash_password(password):
    """Hash a password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()

def login_required(f):
    """Decorator for routes that require login."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to access this page.', 'info')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def get_current_user():
    """Get the current logged-in user."""
    if 'user_id' not in session:
        return None
    db = SessionLocal()
    try:
        user = db.query(User).filter_by(id=session['user_id']).first()
        return user
    finally:
        db.close()

def get_session_id():
    """Get or create a session ID for the current user."""
    if 'session_id' not in session:
        session['session_id'] = os.urandom(16).hex()
    return session['session_id']

def get_cart_count():
    """Get the number of items in the current user's cart."""
    session_id = session.get('session_id')
    if not session_id:
        return 0
    db = SessionLocal()
    try:
        count = db.query(CartItem).filter_by(session_id=session_id).count()
        return count
    finally:
        db.close()

def get_cart_total():
    """Calculate the total for the current user's cart in INR."""
    session_id = session.get('session_id')
    if not session_id:
        return Decimal('0.00')
    db = SessionLocal()
    try:
        cart_items = db.query(CartItem).filter_by(session_id=session_id).all()
        total = sum(item.subtotal for item in cart_items)
        # Convert to INR
        total_inr = Decimal(str(total)) * Decimal(str(USD_TO_INR))
        return total_inr
    finally:
        db.close()

def convert_to_inr(usd_amount):
    """Convert USD to INR."""
    return float(usd_amount)  # Simplified - assuming prices are already in INR

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login page."""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        db = SessionLocal()
        try:
            user = db.query(User).filter_by(username=username).first()
            if user and user.password_hash == hash_password(password):
                session['user_id'] = user.id
                session['username'] = user.username
                flash('Welcome back!', 'success')
                return redirect(url_for('index'))
            else:
                flash('Invalid username or password.', 'error')
        finally:
            db.close()
    return render_template('login.html', cart_count=0)

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration page."""
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if password != confirm_password:
            flash('Passwords do not match.', 'error')
            return render_template('register.html', cart_count=0)
        
        db = SessionLocal()
        try:
            existing_user = db.query(User).filter(
                (User.username == username) | (User.email == email)
            ).first()
            
            if existing_user:
                flash('Username or email already exists.', 'error')
                return render_template('register.html', cart_count=0)
            
            new_user = User(
                username=username,
                email=email,
                password_hash=hash_password(password)
            )
            db.add(new_user)
            db.commit()
            flash('Welcome dear Hogwarts! Welcome Home <3\n\nYour profile\'s been created. Let\'s have some food shall we!? (^v^)', 'success')
            return redirect(url_for('login'))
        finally:
            db.close()
    return render_template('register.html', cart_count=0)

@app.route('/logout')
def logout():
    """User logout."""
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/')
def index():
    """Home page displaying all restaurants with filtering, sorting, and location-based recommendations."""
    db = SessionLocal()
    try:
        # Get filter parameters
        diet_filter = request.args.get('diet', '')
        sort_option = request.args.get('sort', 'relevance')
        user = get_current_user()

        # Base query
        query = db.query(Restaurant)

        # Apply location-based filtering if user has preferred location
        if user and user.preferred_location:
            # Simple location-based filtering (in real app, use geocoding)
            if user.preferred_location.lower() == 'manipal':
                # Show Manipal restaurants first, then others
                query = query.order_by(Restaurant.distance_km.asc())
            elif user.preferred_location.lower() == 'mangalore':
                # Show Mangalore restaurants first
                query = query.order_by(Restaurant.distance_km.asc())

        # Apply dietary filter if specified
        if diet_filter == 'veg':
            # Filter restaurants that have vegetarian items
            veg_restaurant_ids = db.query(MenuItem.restaurant_id).filter_by(is_vegetarian=True).distinct().subquery()
            query = query.filter(Restaurant.id.in_(veg_restaurant_ids))
        elif diet_filter == 'nonveg':
            # Filter restaurants that have non-vegetarian items
            nonveg_restaurant_ids = db.query(MenuItem.restaurant_id).filter_by(is_vegetarian=False).distinct().subquery()
            query = query.filter(Restaurant.id.in_(nonveg_restaurant_ids))

        # Apply sorting
        if sort_option == 'popularity':
            query = query.order_by(Restaurant.popularity_score.desc())
        elif sort_option == 'distance_low':
            query = query.order_by(Restaurant.distance_km.asc())
        elif sort_option == 'distance_high':
            query = query.order_by(Restaurant.distance_km.desc())
        elif sort_option == 'price_low':
            # Sort by average price of menu items (lowest first)
            from sqlalchemy import func
            avg_prices = db.query(
                MenuItem.restaurant_id,
                func.avg(MenuItem.price).label('avg_price')
            ).group_by(MenuItem.restaurant_id).subquery()
            query = query.join(avg_prices, Restaurant.id == avg_prices.c.restaurant_id).order_by(avg_prices.c.avg_price.asc())
        elif sort_option == 'price_high':
            # Sort by average price of menu items (highest first)
            from sqlalchemy import func
            avg_prices = db.query(
                MenuItem.restaurant_id,
                func.avg(MenuItem.price).label('avg_price')
            ).group_by(MenuItem.restaurant_id).subquery()
            query = query.join(avg_prices, Restaurant.id == avg_prices.c.restaurant_id).order_by(avg_prices.c.avg_price.desc())
        else:  # relevance (default)
            query = query.order_by(Restaurant.popularity_score.desc(), Restaurant.distance_km.asc())

        restaurants = query.all()
        cart_count = get_cart_count()
        return render_template('index.html', restaurants=restaurants, cart_count=cart_count, user=user)
    finally:
        db.close()

@app.route('/restaurant/<int:restaurant_id>')
def restaurant(restaurant_id):
    """Display menu for a specific restaurant."""
    db = SessionLocal()
    try:
        restaurant = db.query(Restaurant).filter_by(id=restaurant_id).first()
        if not restaurant:
            flash('Restaurant not found.', 'error')
            return redirect(url_for('index'))
        
        menu_items = db.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
        cart_count = get_cart_count()
        
        # Convert prices to INR for display
        for item in menu_items:
            item.price_inr = convert_to_inr(item.price)
        
        return render_template('restaurant.html', restaurant=restaurant, menu_items=menu_items, cart_count=cart_count)
    finally:
        db.close()

@app.route('/cart/add', methods=['POST'])
def add_to_cart():
    """Add an item to the cart."""
    menu_item_id = request.form.get('menu_item_id')
    quantity = int(request.form.get('quantity', 1))
    
    if quantity < 1:
        quantity = 1
    elif quantity > 20:
        quantity = 20
    
    db = SessionLocal()
    try:
        menu_item = db.query(MenuItem).filter_by(id=menu_item_id).first()
        if not menu_item:
            flash('Menu item not found.', 'error')
            return redirect(url_for('index'))
        
        if not menu_item.is_in_stock:
            flash('This item is currently out of stock.', 'error')
            return redirect(url_for('restaurant', restaurant_id=menu_item.restaurant_id))
        
        if menu_item.stock_quantity < quantity:
            flash(f'Only {menu_item.stock_quantity} items available in stock.', 'warning')
            quantity = menu_item.stock_quantity
        
        user_id = session.get('user_id') if 'user_id' in session else None
        session_id = get_session_id() if not user_id else None
        
        query = db.query(CartItem).filter_by(menu_item_id=menu_item_id)
        if user_id:
            query = query.filter_by(user_id=user_id)
        else:
            query = query.filter_by(session_id=session_id)
        
        existing_item = query.first()
        menu_item.stock_quantity -= quantity
        
        if existing_item:
            existing_item.quantity += quantity
            if existing_item.quantity > 20:
                existing_item.quantity = 20
        else:
            cart_item = CartItem(
                session_id=session_id,
                user_id=user_id,
                menu_item_id=menu_item_id,
                quantity=quantity,
                unit_price=menu_item.price
            )
            db.add(cart_item)
        
        db.commit()
        flash(f'Added {menu_item.name} to cart!', 'success')
        return redirect(url_for('restaurant', restaurant_id=menu_item.restaurant_id))
    finally:
        db.close()

@app.route('/cart')
def cart():
    """Display the shopping cart."""
    db = SessionLocal()
    try:
        from sqlalchemy.orm import joinedload

        if 'user_id' in session:
            cart_items = db.query(CartItem).options(joinedload(CartItem.menu_item)).filter_by(user_id=session['user_id']).all()
        else:
            session_id = session.get('session_id')
            if not session_id:
                cart_items = []
            else:
                cart_items = db.query(CartItem).options(joinedload(CartItem.menu_item)).filter_by(session_id=session_id).all()

        subtotal = sum(item.subtotal for item in cart_items)
        subtotal_inr = Decimal(str(subtotal))

        tax = Decimal('0.00')
        total_inr = subtotal_inr + tax

        # Add INR prices to cart items for display
        for item in cart_items:
            item.unit_price_inr = convert_to_inr(item.unit_price)
            item.subtotal_inr = convert_to_inr(item.subtotal)

        cart_count = len(cart_items)
        user = get_current_user()

        return render_template('cart.html', cart_items=cart_items,
                             subtotal=subtotal_inr, tax=tax, total=total_inr,
                             cart_count=cart_count, user=user, currency='INR')
    finally:
        db.close()

@app.route('/cart/update/<int:item_id>/<action>', methods=['POST'])
def update_cart_item(item_id, action):
    """Update cart item quantity (increase/decrease)."""
    if action not in ['increase', 'decrease']:
        flash('Invalid action.', 'error')
        return redirect(url_for('cart'))

    db = SessionLocal()
    try:
        # Find the cart item
        if 'user_id' in session:
            cart_item = db.query(CartItem).filter_by(id=item_id, user_id=session['user_id']).first()
        else:
            session_id = session.get('session_id')
            cart_item = db.query(CartItem).filter_by(id=item_id, session_id=session_id).first()

        if not cart_item:
            flash('Cart item not found.', 'error')
            return redirect(url_for('cart'))

        menu_item = cart_item.menu_item
        if not menu_item:
            flash('Menu item not found.', 'error')
            return redirect(url_for('cart'))

        if action == 'increase':
            if cart_item.quantity >= 20:
                flash('Maximum quantity per item is 20.', 'warning')
            elif menu_item.stock_quantity <= 0:
                flash('This item is out of stock.', 'error')
            else:
                cart_item.quantity += 1
                menu_item.stock_quantity -= 1
                flash('Quantity increased.', 'success')
        elif action == 'decrease':
            if cart_item.quantity <= 1:
                flash('Minimum quantity is 1. Use remove to delete item.', 'warning')
            else:
                cart_item.quantity -= 1
                menu_item.stock_quantity += 1
                flash('Quantity decreased.', 'success')

        db.commit()
        return redirect(url_for('cart'))
    finally:
        db.close()

@app.route('/cart/remove/<int:item_id>', methods=['POST'])
def remove_cart_item(item_id):
    """Remove an item from the cart."""
    db = SessionLocal()
    try:
        # Find the cart item
        if 'user_id' in session:
            cart_item = db.query(CartItem).filter_by(id=item_id, user_id=session['user_id']).first()
        else:
            session_id = session.get('session_id')
            cart_item = db.query(CartItem).filter_by(id=item_id, session_id=session_id).first()

        if not cart_item:
            flash('Cart item not found.', 'error')
            return redirect(url_for('cart'))

        # Restore stock quantity
        if cart_item.menu_item:
            cart_item.menu_item.stock_quantity += cart_item.quantity

        # Remove the cart item
        db.delete(cart_item)
        db.commit()

        flash('Item removed from cart.', 'success')
        return redirect(url_for('cart'))
    finally:
        db.close()

@app.route('/place-order', methods=['POST'])
def place_order():
    """Place order directly without payment processing."""
    session_id = session.get('session_id')
    user_id = session.get('user_id')

    if not session_id and not user_id:
        flash('Session expired. Please try again.', 'error')
        return redirect(url_for('cart'))

    db = SessionLocal()
    try:
        # Get cart items
        if user_id:
            cart_items = db.query(CartItem).filter_by(user_id=user_id).all()
        else:
            cart_items = db.query(CartItem).filter_by(session_id=session_id).all()

        if not cart_items:
            flash('Cart is empty.', 'error')
            return redirect(url_for('cart'))

        # Calculate total
        total_inr = sum(item.subtotal for item in cart_items)
        total_inr = Decimal(str(total_inr))

        # Create order
        order = Order(
            user_id=user_id,
            total_amount=total_inr,
            status='confirmed',
            payment_id=f'simplified_order_{hashlib.md5(str(total_inr).encode()).hexdigest()[:10]}'
        )
        db.add(order)
        db.flush()  # Get order ID

        # Create order items
        for cart_item in cart_items:
            order_item = OrderItem(
                order_id=order.id,
                menu_item_id=cart_item.menu_item_id,
                quantity=cart_item.quantity,
                unit_price=cart_item.unit_price,
                subtotal=Decimal(str(cart_item.subtotal))
            )
            db.add(order_item)

        # Clear cart
        for item in cart_items:
            db.delete(item)

        db.commit()

        # Store order ID in session for thank you page
        session['last_order_id'] = order.id

        flash('Order placed successfully! Your food will be prepared soon.', 'success')
        return redirect(url_for('thank_you'))
    finally:
        db.close()





@app.route('/thank-you')
def thank_you():
    """Thank you page after successful payment."""
    cart_count = 0
    order_id = session.get('last_order_id')
    order = None

    if order_id:
        db = SessionLocal()
        try:
            order = db.query(Order).filter_by(id=order_id).first()
        finally:
            db.close()

    return render_template('thank_you.html', cart_count=cart_count, order=order)

# Chatbot API endpoints
@app.route('/api/chatbot', methods=['POST'])
def chatbot_endpoint():
    """Chatbot API endpoint with enhanced error handling and user context."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Invalid JSON data'}), 400

        user_message = data.get('message', '').strip()
        if not user_message:
            return jsonify({
                'response': "I didn't receive any message. How can I help you with food ordering today? 🦉",
                'intent': 'empty_message',
                'success': True
            })

        # Get user context for conversation memory
        user_id = session.get('user_id') or session.get('session_id')

        response = chatbot.get_response(user_message, user_id)
        return jsonify(response)

    except Exception as e:
        print(f"Chatbot API error: {str(e)}")  # For debugging
        return jsonify({
            'response': "I'm experiencing some technical difficulties. Please try again in a moment! 🦉",
            'intent': 'error',
            'success': False,
            'error': str(e)
        }), 500

@app.route('/chatbot-page')
def chatbot_page():
    """Chatbot interface page."""
    cart_count = get_cart_count()
    user = get_current_user()
    return render_template('chatbot.html', cart_count=cart_count, user=user)

@app.route('/profile')
@login_required
def profile():
    """User profile page with order history, average rating, and feedback history."""
    db = SessionLocal()
    try:
        user = get_current_user()
        orders = db.query(Order).filter_by(user_id=user.id).order_by(Order.created_at.desc()).all()

        # Calculate average rating from food and delivery feedback
        food_feedbacks = db.query(Feedback).filter_by(user_id=user.id).all()
        delivery_feedbacks = db.query(DeliveryFeedback).filter_by(user_id=user.id).all()

        food_ratings = [f.rating for f in food_feedbacks]
        delivery_ratings = [f.delivery_person_rating for f in delivery_feedbacks]

        all_ratings = food_ratings + delivery_ratings
        average_rating = sum(all_ratings) / len(all_ratings) if all_ratings else 0

        # Get all feedback for display
        all_feedback = []
        for feedback in food_feedbacks:
            all_feedback.append({
                'type': 'food',
                'order_id': feedback.order_id,
                'rating': feedback.rating,
                'comment': feedback.comment,
                'created_at': feedback.created_at
            })
        for feedback in delivery_feedbacks:
            all_feedback.append({
                'type': 'delivery',
                'order_id': feedback.order_id,
                'rating': feedback.delivery_person_rating,
                'comment': feedback.comment,
                'created_at': feedback.created_at
            })

        # Sort feedback by creation date
        all_feedback.sort(key=lambda x: x['created_at'], reverse=True)

        cart_count = get_cart_count()
        return render_template('profile.html', user=user, orders=orders, cart_count=cart_count,
                             average_rating=average_rating, feedback_history=all_feedback)
    finally:
        db.close()

@app.route('/order/<int:order_id>')
@login_required
def order_details(order_id):
    """Display detailed order information with live tracking."""
    db = SessionLocal()
    try:
        user = get_current_user()
        order = db.query(Order).filter_by(id=order_id, user_id=user.id).first()

        if not order:
            flash('Order not found.', 'error')
            return redirect(url_for('profile'))

        cart_count = get_cart_count()
        return render_template('order_tracking.html', order=order, cart_count=cart_count, user=user)
    finally:
        db.close()

@app.route('/feedback/<int:order_id>', methods=['GET', 'POST'])
@login_required
def submit_feedback(order_id):
    """Submit feedback for a completed order."""
    db = SessionLocal()
    try:
        user = get_current_user()
        order = db.query(Order).filter_by(id=order_id, user_id=user.id).first()

        if not order:
            flash('Order not found.', 'error')
            return redirect(url_for('profile'))

        # Check if feedback already exists
        existing_feedback = db.query(Feedback).filter_by(order_id=order_id).first()
        if existing_feedback:
            flash('Feedback already submitted for this order.', 'info')
            return redirect(url_for('order_details', order_id=order_id))

        if request.method == 'POST':
            rating = int(request.form.get('rating', 5))
            comment = request.form.get('comment', '').strip()

            feedback = Feedback(
                order_id=order_id,
                user_id=user.id,
                rating=rating,
                comment=comment if comment else None
            )
            db.add(feedback)
            db.commit()

            flash('Thank you for your feedback!', 'success')
            return redirect(url_for('order_details', order_id=order_id))

        cart_count = get_cart_count()
        return render_template('feedback_form.html', order=order, cart_count=cart_count, user=user)
    finally:
        db.close()

@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    """User account settings page with location preferences."""
    user = get_current_user()
    cart_count = get_cart_count()

    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'change_password':
            current_password = request.form.get('current_password')
            new_password = request.form.get('new_password')
            confirm_password = request.form.get('confirm_password')

            if not current_password or not new_password or not confirm_password:
                flash('All password fields are required.', 'error')
            elif new_password != confirm_password:
                flash('New passwords do not match.', 'error')
            elif hash_password(current_password) != user.password_hash:
                flash('Current password is incorrect.', 'error')
            else:
                db = SessionLocal()
                try:
                    user.password_hash = hash_password(new_password)
                    db.commit()
                    flash('Password changed successfully!', 'success')
                finally:
                    db.close()

        elif action == 'update_location':
            preferred_location = request.form.get('preferred_location', '').strip()
            latitude = request.form.get('latitude')
            longitude = request.form.get('longitude')

            db = SessionLocal()
            try:
                user.preferred_location = preferred_location if preferred_location else None
                if latitude and longitude:
                    try:
                        user.latitude = float(latitude)
                        user.longitude = float(longitude)
                    except ValueError:
                        flash('Invalid latitude or longitude values.', 'error')
                        return render_template('settings.html', user=user, cart_count=cart_count)
                db.commit()
                flash('Location preferences updated successfully!', 'success')
            finally:
                db.close()

        elif action == 'update_preferences':
            # Handle preference updates (theme, notifications, etc.)
            flash('Preferences updated successfully!', 'success')

    return render_template('settings.html', user=user, cart_count=cart_count)

@app.route('/delete-account', methods=['POST'])
@login_required
def delete_account():
    """Delete user account."""
    user = get_current_user()
    confirm_username = request.form.get('confirm_username')

    if confirm_username != user.username:
        flash('Username confirmation does not match.', 'error')
        return redirect(url_for('settings'))

    db = SessionLocal()
    try:
        # Delete user (cascade will handle related records)
        db.delete(user)
        db.commit()

        # Clear session
        session.clear()
        flash('Account deleted successfully.', 'info')
        return redirect(url_for('index'))
    finally:
        db.close()

@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    """Forgot password page."""
    if request.method == 'POST':
        email = request.form.get('email')
        if not email:
            flash('Email is required.', 'error')
            return render_template('forgot_password.html', cart_count=0)

        db = SessionLocal()
        try:
            user = db.query(User).filter_by(email=email).first()
            if user:
                # Generate reset token
                token = secrets.token_urlsafe(32)
                expires = datetime.utcnow() + timedelta(hours=1)
                user.reset_token = token
                user.reset_expires = expires
                db.commit()

                # Send reset email
                reset_url = url_for('reset_password', token=token, _external=True)
                msg = Message('Password Reset Request - Portkey',
                            recipients=[email])
                msg.body = f'''Hi {user.username},

You requested a password reset for your Portkey account.

Click the following link to reset your password:
{reset_url}

This link will expire in 1 hour.

If you didn't request this reset, please ignore this email.

Best regards,
Portkey Team
'''
                try:
                    mail.send(msg)
                    flash('Password reset link has been sent to your email.', 'success')
                except Exception as e:
                    print(f"Email sending failed: {e}")
                    # For demo purposes, show the reset link in flash message
                    reset_url = url_for('reset_password', token=token, _external=True)
                    flash(f'Demo mode: Reset link - {reset_url}', 'info')
                    flash('Password reset link has been sent to your email (demo mode).', 'success')
            else:
                # Don't reveal if email exists or not for security
                flash('If an account with that email exists, a reset link has been sent.', 'info')
        finally:
            db.close()

        return redirect(url_for('login'))

    return render_template('forgot_password.html', cart_count=0)

@app.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    """Reset password page."""
    db = SessionLocal()
    try:
        user = db.query(User).filter_by(reset_token=token).first()
        if not user or (user.reset_expires and user.reset_expires < datetime.utcnow()):
            flash('Invalid or expired reset token.', 'error')
            return redirect(url_for('login'))

        if request.method == 'POST':
            new_password = request.form.get('new_password')
            confirm_password = request.form.get('confirm_password')

            if not new_password or not confirm_password:
                flash('All fields are required.', 'error')
                return render_template('reset_password.html', token=token, cart_count=0)

            if new_password != confirm_password:
                flash('Passwords do not match.', 'error')
                return render_template('reset_password.html', token=token, cart_count=0)

            if len(new_password) < 6:
                flash('Password must be at least 6 characters long.', 'error')
                return render_template('reset_password.html', token=token, cart_count=0)

            # Update password and clear reset token
            user.password_hash = hash_password(new_password)
            user.reset_token = None
            user.reset_expires = None
            db.commit()

            flash('Password has been reset successfully. Please login with your new password.', 'success')
            return redirect(url_for('login'))

        return render_template('reset_password.html', token=token, cart_count=0)
    finally:
        db.close()

@app.route('/change-password', methods=['POST'])
@login_required
def change_password():
    """Change user password."""
    user = get_current_user()
    current_password = request.form.get('current_password')
    new_password = request.form.get('new_password')
    confirm_password = request.form.get('confirm_password')

    if not current_password or not new_password or not confirm_password:
        flash('All password fields are required.', 'error')
        return redirect(url_for('settings'))

    if new_password != confirm_password:
        flash('New passwords do not match.', 'error')
        return redirect(url_for('settings'))

    if hash_password(current_password) != user.password_hash:
        flash('Current password is incorrect.', 'error')
        return redirect(url_for('settings'))

    db = SessionLocal()
    try:
        user.password_hash = hash_password(new_password)
        db.commit()
        flash('Password changed successfully!', 'success')
    finally:
        db.close()

    return redirect(url_for('settings'))

# API endpoints for order management
@app.route('/api/orders')
@login_required
def get_orders_api():
    """API endpoint to get user's orders."""
    db = SessionLocal()
    try:
        user = get_current_user()
        orders = db.query(Order).filter_by(user_id=user.id).order_by(Order.created_at.desc()).all()
        return jsonify([order.to_dict() for order in orders])
    finally:
        db.close()

@app.route('/api/feedback', methods=['POST'])
@login_required
def submit_feedback_api():
    """API endpoint to submit feedback."""
    try:
        data = request.get_json()
        order_id = data.get('order_id')
        rating = data.get('rating')
        comment = data.get('comment')

        if not order_id or not rating:
            return jsonify({'error': 'Order ID and rating are required'}), 400

        db = SessionLocal()
        try:
            user = get_current_user()
            order = db.query(Order).filter_by(id=order_id, user_id=user.id).first()

            if not order:
                return jsonify({'error': 'Order not found'}), 404

            # Check if feedback already exists
            existing_feedback = db.query(Feedback).filter_by(order_id=order_id).first()
            if existing_feedback:
                return jsonify({'error': 'Feedback already submitted'}), 400

            feedback = Feedback(
                order_id=order_id,
                user_id=user.id,
                rating=rating,
                comment=comment
            )
            db.add(feedback)
            db.commit()

            return jsonify({'message': 'Feedback submitted successfully', 'feedback': feedback.to_dict()})
        finally:
            db.close()
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
