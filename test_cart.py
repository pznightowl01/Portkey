import requests
from app import app
from db import SessionLocal
from models import CartItem, MenuItem, User

def test_cart_functionality():
    """Test cart update and remove functionality."""
    print("🛒 Testing Cart Functionality")
    print("=" * 40)

    # Test the cart routes
    with app.test_client() as client:
        # First, create a test user and add items to cart
        db = SessionLocal()
        try:
            # Create test user if not exists
            test_user = db.query(User).filter_by(username='carttest').first()
            if not test_user:
                test_user = User(
                    username='carttest',
                    email='carttest@example.com',
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

            print(f"Added {menu_item.name} to cart for test user (quantity: 2)")
            cart_item_id = cart_item.id  # Store cart item ID before closing session
            user_id = test_user.id  # Store user ID before closing session

        finally:
            db.close()

        # Now test the cart update and remove routes
        with client.session_transaction() as sess:
            sess['user_id'] = user_id

        # Test increase quantity
        print("\nTesting quantity increase...")
        response = client.post(f'/cart/update/{cart_item_id}/increase')
        print(f"Increase response status: {response.status_code}")

        # Check cart after increase
        db = SessionLocal()
        try:
            updated_item = db.query(CartItem).filter_by(id=cart_item_id).first()
            if updated_item:
                print(f"Quantity after increase: {updated_item.quantity}")
                if updated_item.quantity == 3:
                    print("✅ Quantity increase successful")
                else:
                    print("❌ Quantity increase failed")
            else:
                print("❌ Cart item not found after increase")
        finally:
            db.close()

        # Test decrease quantity
        print("\nTesting quantity decrease...")
        response = client.post(f'/cart/update/{cart_item_id}/decrease')
        print(f"Decrease response status: {response.status_code}")

        # Check cart after decrease
        db = SessionLocal()
        try:
            updated_item = db.query(CartItem).filter_by(id=cart_item_id).first()
            if updated_item:
                print(f"Quantity after decrease: {updated_item.quantity}")
                if updated_item.quantity == 2:
                    print("✅ Quantity decrease successful")
                else:
                    print("❌ Quantity decrease failed")
            else:
                print("❌ Cart item not found after decrease")
        finally:
            db.close()

        # Test remove item
        print("\nTesting item removal...")
        response = client.post(f'/cart/remove/{cart_item_id}')
        print(f"Remove response status: {response.status_code}")

        # Check cart after removal
        db = SessionLocal()
        try:
            removed_item = db.query(CartItem).filter_by(id=cart_item_id).first()
            if removed_item:
                print("❌ Item still exists after removal")
            else:
                print("✅ Item successfully removed from cart")
        finally:
            db.close()

        print("\n✅ Cart functionality testing completed!")

if __name__ == "__main__":
    test_cart_functionality()
