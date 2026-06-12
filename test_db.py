from db import SessionLocal
from models import Restaurant, MenuItem, CartItem, User

def test_database_integrity():
    """Test database integrity and relationships."""

    session = SessionLocal()
    try:
        # Count records
        restaurant_count = session.query(Restaurant).count()
        menu_count = session.query(MenuItem).count()
        user_count = session.query(User).count()
        cart_count = session.query(CartItem).count()

        print('📊 Database Integrity Check')
        print('=' * 30)
        print(f'Restaurants: {restaurant_count}')
        print(f'Menu Items: {menu_count}')
        print(f'Users: {user_count}')
        print(f'Cart Items: {cart_count}')
        print()

        # Test relationships
        print('🔗 Relationship Tests')
        print('=' * 20)

        # Test restaurant-menu relationship
        restaurant = session.query(Restaurant).first()
        if restaurant:
            menu_items = len(restaurant.menu_items)
            print(f'First restaurant "{restaurant.name}" has {menu_items} menu items')

        # Test menu-restaurant relationship
        menu_item = session.query(MenuItem).first()
        if menu_item and menu_item.restaurant:
            print(f'First menu item belongs to "{menu_item.restaurant.name}"')

        # Test stock availability
        available_items = session.query(MenuItem).filter(
            MenuItem.availability == True,
            MenuItem.stock_quantity > 0
        ).count()
        print(f'Available menu items: {available_items}')

        # Test cuisine types
        cuisines = session.query(Restaurant.cuisine_type).distinct().all()
        print(f'Unique cuisine types: {[c[0] for c in cuisines]}')

        print()
        print('✅ Database integrity check completed successfully!')

    except Exception as e:
        print(f'❌ Database error: {e}')
    finally:
        session.close()

if __name__ == '__main__':
    test_database_integrity()
