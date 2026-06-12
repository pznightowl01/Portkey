from app import app
from db import SessionLocal
from models import Order, CartItem, MenuItem, User

def test_place_order():
    print("🧪 Testing Place Order Endpoint")
    print("=" * 40)

    # Test the endpoint
    with app.test_client() as client:
        # First, create a test user and add items to cart
        db = SessionLocal()
        try:
            # Create test user if not exists
            test_user = db.query(User).filter_by(username='testuser').first()
            if not test_user:
                test_user = User(
                    username='testuser',
                    email='test@example.com',
                    password_hash='hashedpassword'
                )
                db.add(test_user)
                db.commit()

            # Get first menu item
            menu_item = db.query(MenuItem).first()
            if not menu_item:
                print("❌ No menu items found in database")
                return

            # Add item to cart
            cart_item = CartItem(
                user_id=test_user.id,
                menu_item_id=menu_item.id,
                quantity=2,
                unit_price=menu_item.price
            )
            db.add(cart_item)
            db.commit()

            print(f"Added {menu_item.name} to cart for test user")
            user_id = test_user.id  # Store user ID before closing session

        finally:
            db.close()

        # Now test the place order endpoint
        with client.session_transaction() as sess:
            sess['user_id'] = user_id

        # Place order
        response = client.post('/place-order')
        print(f"Response status: {response.status_code}")

        if response.status_code == 302:  # Redirect to thank you page
            print("✅ Order placed successfully (redirected to thank you page)")

            # Check orders after
            db = SessionLocal()
            try:
                orders_after = db.query(Order).filter_by(user_id=user_id).all()
                print(f"Total orders for user: {len(orders_after)}")

                # Check cart items after
                cart_after = db.query(CartItem).filter_by(user_id=user_id).all()
                print(f"Cart items after order: {len(cart_after)}")

                if len(orders_after) > 0:
                    last_order = orders_after[-1]
                    print(f"Last order ID: {last_order.id}")
                    print(f"Last order payment_id: {last_order.payment_id}")
                    print(f"Last order total: {last_order.total_amount}")
                    print("✅ Order created successfully!")
                else:
                    print("❌ No order was created")
            finally:
                db.close()
        else:
            print(f"❌ Order failed: {response.get_data(as_text=True)}")

if __name__ == "__main__":
    test_place_order()
