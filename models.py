"""SQLAlchemy models for Portkey food ordering app."""

from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DECIMAL, DateTime
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

# Create base class here to avoid circular imports
Base = declarative_base()


class User(Base):
    """User model for authentication and user management."""

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    password_hash = Column(String(200), nullable=False)
    reset_token = Column(String(100), nullable=True)
    reset_expires = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    # Location preferences for dynamic filtering
    preferred_location = Column(String(100), nullable=True)  # e.g., "Manipal" or "Mangalore"
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    preferred_radius_km = Column(Float, default=5.0)  # Default radius, but will be dynamic

    # Relationships
    cart_items = relationship("CartItem", back_populates="user", cascade="all, delete-orphan")
    orders = relationship("Order", back_populates="user", cascade="all, delete-orphan")
    feedback = relationship("Feedback", back_populates="user", cascade="all, delete-orphan")
    delivery_feedback = relationship("DeliveryFeedback", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"

    def to_dict(self):
        """Convert user object to dictionary for API responses."""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class Restaurant(Base):
    """Restaurant model representing a food establishment with location and cuisine details."""

    __tablename__ = 'restaurants'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, index=True)
    address = Column(String(200), nullable=False)
    contact = Column(String(50), nullable=False)
    operating_hours = Column(String(100), nullable=False)  # e.g., "Mon-Sun: 10AM-10PM"
    cuisine_type = Column(String(50), nullable=False, index=True)  # e.g., "Italian", "Chinese"
    distance_km = Column(Float, nullable=False, default=1.0)  # Distance from user in km
    popularity_score = Column(Float, nullable=False, default=0.0)  # Based on order frequency

    # Relationship to menu items
    menu_items = relationship("MenuItem", back_populates="restaurant", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Restaurant(id={self.id}, name='{self.name}', cuisine='{self.cuisine_type}')>"

    def to_dict(self):
        """Convert restaurant object to dictionary for API responses."""
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address,
            'contact': self.contact,
            'operating_hours': self.operating_hours,
            'cuisine_type': self.cuisine_type,
            'menu_count': len(self.menu_items) if self.menu_items else 0
        }


class MenuItem(Base):
    """Menu item model representing a food item available from a restaurant with stock management."""

    __tablename__ = 'menu_items'

    id = Column(Integer, primary_key=True, autoincrement=True)
    restaurant_id = Column(Integer, ForeignKey('restaurants.id'), nullable=False, index=True)
    name = Column(String(100), nullable=False, index=True)
    description = Column(String(500), nullable=False)
    price = Column(DECIMAL(10, 2), nullable=False)
    category = Column(String(50), nullable=False, index=True)  # e.g., "Appetizer", "Main", "Dessert", "Beverage"
    availability = Column(Boolean, default=True, nullable=False)
    stock_quantity = Column(Integer, default=100, nullable=False)  # Available stock
    is_vegetarian = Column(Boolean, default=True, nullable=False)  # Veg/Non-veg classification

    # Relationship to restaurant
    restaurant = relationship("Restaurant", back_populates="menu_items")

    # Relationship to cart items
    cart_items = relationship("CartItem", back_populates="menu_item", cascade="all, delete-orphan")

    @property
    def is_in_stock(self):
        """Check if item is in stock."""
        return self.stock_quantity > 0 and self.availability

    def __repr__(self):
        return f"<MenuItem(id={self.id}, name='{self.name}', price={self.price}, stock={self.stock_quantity})>"

    def to_dict(self):
        """Convert menu item object to dictionary for API responses."""
        return {
            'id': self.id,
            'restaurant_id': self.restaurant_id,
            'name': self.name,
            'description': self.description,
            'price': float(self.price),
            'category': self.category,
            'availability': self.availability,
            'stock_quantity': self.stock_quantity,
            'is_in_stock': self.is_in_stock,
            'restaurant_name': self.restaurant.name if self.restaurant else None
        }


class CartItem(Base):
    """Cart item model representing an item in the user's shopping cart with session management."""

    __tablename__ = 'cart_items'

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String(100), nullable=True, index=True)  # Anonymous session tracking
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True, index=True)  # User ID for logged-in users
    menu_item_id = Column(Integer, ForeignKey('menu_items.id'), nullable=False, index=True)
    quantity = Column(Integer, nullable=False, default=1)
    unit_price = Column(DECIMAL(10, 2), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    menu_item = relationship("MenuItem", back_populates="cart_items")
    user = relationship("User", back_populates="cart_items")

    @property
    def subtotal(self):
        """Calculate subtotal for this cart item."""
        return float(self.unit_price) * self.quantity

    def __repr__(self):
        return f"<CartItem(id={self.id}, item='{self.menu_item.name if self.menu_item else 'Unknown'}', qty={self.quantity}, subtotal={self.subtotal:.2f})>"

    def to_dict(self):
        """Convert cart item object to dictionary for API responses."""
        return {
            'id': self.id,
            'session_id': self.session_id,
            'user_id': self.user_id,
            'menu_item_id': self.menu_item_id,
            'quantity': self.quantity,
            'unit_price': float(self.unit_price),
            'subtotal': self.subtotal,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'menu_item': self.menu_item.to_dict() if self.menu_item else None
        }


class Order(Base):
    """Order model representing a completed food order."""

    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True, index=True)
    total_amount = Column(DECIMAL(10, 2), nullable=False)  # Total in INR
    status = Column(String(50), nullable=False, default='confirmed')  # confirmed, preparing, ready, out_for_delivery, delivered, cancelled
    delivery_address = Column(String(500), nullable=True)
    payment_id = Column(String(100), nullable=True)  # Razorpay payment ID
    delivery_person_name = Column(String(100), nullable=True)  # Assigned delivery person
    delivery_person_contact = Column(String(20), nullable=True)  # Delivery person contact
    estimated_delivery_time = Column(DateTime, nullable=True)  # ETA
    # Live tracking coordinates
    delivery_lat = Column(Float, nullable=True)
    delivery_lng = Column(Float, nullable=True)
    # Dynamic ETA calculation factors
    preparation_time_minutes = Column(Integer, default=15)  # Restaurant prep time
    traffic_factor = Column(Float, default=1.0)  # Traffic multiplier (1.0 = normal, 1.5 = heavy traffic)
    weather_factor = Column(Float, default=1.0)  # Weather impact (1.0 = clear, 1.2 = rain)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    user = relationship("User", back_populates="orders")
    order_items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
    feedback = relationship("Feedback", back_populates="order", uselist=False, cascade="all, delete-orphan")
    delivery_feedback = relationship("DeliveryFeedback", back_populates="order", uselist=False, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Order(id={self.id}, user_id={self.user_id}, total={self.total_amount}, status='{self.status}')>"

    def to_dict(self):
        """Convert order object to dictionary for API responses."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'total_amount': float(self.total_amount),
            'status': self.status,
            'delivery_address': self.delivery_address,
            'payment_id': self.payment_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'order_items': [item.to_dict() for item in self.order_items] if self.order_items else []
        }


class OrderItem(Base):
    """Order item model linking orders to menu items with quantities and prices."""

    __tablename__ = 'order_items'

    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False, index=True)
    menu_item_id = Column(Integer, ForeignKey('menu_items.id'), nullable=False, index=True)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(DECIMAL(10, 2), nullable=False)  # Price at time of order
    subtotal = Column(DECIMAL(10, 2), nullable=False)

    # Relationships
    order = relationship("Order", back_populates="order_items")
    menu_item = relationship("MenuItem")

    def __repr__(self):
        return f"<OrderItem(id={self.id}, order_id={self.order_id}, menu_item_id={self.menu_item_id}, qty={self.quantity})>"

    def to_dict(self):
        """Convert order item object to dictionary for API responses."""
        return {
            'id': self.id,
            'order_id': self.order_id,
            'menu_item_id': self.menu_item_id,
            'quantity': self.quantity,
            'unit_price': float(self.unit_price),
            'subtotal': float(self.subtotal),
            'menu_item': self.menu_item.to_dict() if self.menu_item else None
        }


class Feedback(Base):
    """Feedback model for user feedback on orders."""

    __tablename__ = 'feedback'

    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    rating = Column(Integer, nullable=False)  # 1-5 stars
    comment = Column(String(1000), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    order = relationship("Order", back_populates="feedback")
    user = relationship("User", back_populates="feedback")

    def __repr__(self):
        return f"<Feedback(id={self.id}, order_id={self.order_id}, rating={self.rating})>"

    def to_dict(self):
        """Convert feedback object to dictionary for API responses."""
        return {
            'id': self.id,
            'order_id': self.order_id,
            'user_id': self.user_id,
            'rating': self.rating,
            'comment': self.comment,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class DeliveryFeedback(Base):
    """Delivery feedback model for feedback on delivery personnel and service."""

    __tablename__ = 'delivery_feedback'

    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    delivery_person_rating = Column(Integer, nullable=False)  # 1-5 stars
    delivery_time_rating = Column(Integer, nullable=False)  # 1-5 stars (how was delivery time)
    comment = Column(String(1000), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    order = relationship("Order", back_populates="delivery_feedback")
    user = relationship("User", back_populates="delivery_feedback")

    def __repr__(self):
        return f"<DeliveryFeedback(id={self.id}, order_id={self.order_id}, delivery_rating={self.delivery_person_rating})>"

    def to_dict(self):
        """Convert delivery feedback object to dictionary for API responses."""
        return {
            'id': self.id,
            'order_id': self.order_id,
            'user_id': self.user_id,
            'delivery_person_rating': self.delivery_person_rating,
            'delivery_time_rating': self.delivery_time_rating,
            'comment': self.comment,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
