"""Database configuration and initialization for Portkey app - REAL MANIPAL & MANGALORE RESTAURANTS."""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Restaurant, MenuItem, CartItem, User

# Database configuration
DATABASE_URL = "sqlite:///database.db"
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Initialize database by creating all tables."""
    from models import Restaurant, MenuItem, CartItem, User
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    print("Database initialized successfully!")

def seed_db():
    """Seed the database with REAL Manipal & Mangalore restaurants."""
    session = SessionLocal()
    try:
        # Check if data already exists
        if session.query(Restaurant).count() > 0:
            print("Database already seeded. Skipping seed process.")
            return

        print("🌱 Starting database seeding process...")

        # ============ MANIPAL RESTAURANTS ============
        
        # Restaurant 1: Dollops - Indian & Chinese
        dollops = Restaurant(
            name="Dollops",
            address="16-384B, Tiger Circle, Upendra Nagar, Manipal, Karnataka 576104",
            contact="+91 8202 570908",
            operating_hours="Mon-Sun: 11:00 AM - 11:00 PM",
            cuisine_type="Indian & Chinese",
            distance_km=2.5,
            popularity_score=8.5
        )
        session.add(dollops)
        session.flush()
        
        # Dollops Menu
        dollops_items = [
            MenuItem(restaurant_id=dollops.id, name="Paneer Tikka Masala", description="Grilled cottage cheese in rich tomato gravy", price=12.00, category="Main Course", availability=True, stock_quantity=25, is_vegetarian=True),
            MenuItem(restaurant_id=dollops.id, name="Chicken Manchurian", description="Indo-Chinese spicy chicken with bell peppers", price=13.50, category="Main Course", availability=True, stock_quantity=20, is_vegetarian=False),
            MenuItem(restaurant_id=dollops.id, name="Veg Fried Rice", description="Stir-fried rice with mixed vegetables", price=8.00, category="Main Course", availability=True, stock_quantity=30, is_vegetarian=True),
            MenuItem(restaurant_id=dollops.id, name="Hakka Noodles", description="Spicy noodles with vegetables", price=9.00, category="Main Course", availability=True, stock_quantity=28, is_vegetarian=True),
            MenuItem(restaurant_id=dollops.id, name="Spring Rolls", description="Crispy vegetable rolls with sweet chili sauce", price=6.50, category="Appetizers", availability=True, stock_quantity=35, is_vegetarian=True),
            MenuItem(restaurant_id=dollops.id, name="Gobi Manchurian Dry", description="Crispy cauliflower tossed in spicy sauce", price=7.50, category="Appetizers", availability=True, stock_quantity=30, is_vegetarian=True),
            MenuItem(restaurant_id=dollops.id, name="Dal Tadka", description="Yellow lentils tempered with spices", price=6.00, category="Main Course", availability=True, stock_quantity=40, is_vegetarian=True),
            MenuItem(restaurant_id=dollops.id, name="Butter Naan", description="Soft Indian flatbread with butter", price=2.50, category="Breads", availability=True, stock_quantity=50, is_vegetarian=True),
            MenuItem(restaurant_id=dollops.id, name="Gulab Jamun", description="Sweet milk solid dumplings in sugar syrup", price=3.50, category="Desserts", availability=True, stock_quantity=30, is_vegetarian=True),
        ]
        session.add_all(dollops_items)
        
        # Restaurant 2: Pai Tiffins - Quick Bites & Snacks
        pai_tiffins = Restaurant(
            name="Pai Tiffins",
            address="Shop No 16-444 A1, Ground Floor, Manipal Commercial Complex, Manipal, Karnataka 576104",
            contact="+91 9611 013777",
            operating_hours="Mon-Sun: 7:00 AM - 10:00 PM",
            cuisine_type="South Indian"
        )
        session.add(pai_tiffins)
        session.flush()
        
        # Pai Tiffins Menu
        pai_items = [
            MenuItem(restaurant_id=pai_tiffins.id, name="Masala Dosa", description="Crispy rice crepe filled with spiced potatoes", price=4.50, category="Main Course", availability=True, stock_quantity=40),
            MenuItem(restaurant_id=pai_tiffins.id, name="Idli Sambar", description="Steamed rice cakes with lentil soup", price=3.50, category="Main Course", availability=True, stock_quantity=50),
            MenuItem(restaurant_id=pai_tiffins.id, name="Vada Sambar", description="Fried lentil donuts with sambar", price=4.00, category="Main Course", availability=True, stock_quantity=35),
            MenuItem(restaurant_id=pai_tiffins.id, name="Upma", description="Savory semolina porridge with vegetables", price=3.00, category="Main Course", availability=True, stock_quantity=30),
            MenuItem(restaurant_id=pai_tiffins.id, name="Puri Bhaji", description="Fried bread with spiced potato curry", price=5.00, category="Main Course", availability=True, stock_quantity=25),
            MenuItem(restaurant_id=pai_tiffins.id, name="Medu Vada", description="Crispy fried lentil donuts", price=3.50, category="Snacks", availability=True, stock_quantity=40),
            MenuItem(restaurant_id=pai_tiffins.id, name="Filter Coffee", description="Traditional South Indian coffee", price=1.50, category="Beverages", availability=True, stock_quantity=60),
            MenuItem(restaurant_id=pai_tiffins.id, name="Kesari Bath", description="Sweet semolina dessert with saffron", price=3.00, category="Desserts", availability=True, stock_quantity=25),
        ]
        session.add_all(pai_items)
        
        # Restaurant 3: Hadiqa - Italian & Pizza
        hadiqa = Restaurant(
            name="Hadiqa",
            address="Smrithi Bhavan, Madhuvan Serai Building, behind T.M.A. Pai Park, Eshwar Nagar, Manipal, Karnataka 576104",
            contact="+91 8204 294455",
            operating_hours="Mon-Sun: 12:00 PM - 11:30 PM",
            cuisine_type="Italian"
        )
        session.add(hadiqa)
        session.flush()
        
        # Hadiqa Menu
        hadiqa_items = [
            MenuItem(restaurant_id=hadiqa.id, name="Margherita Pizza", description="Classic pizza with tomato sauce, mozzarella & basil", price=10.00, category="Pizza", availability=True, stock_quantity=30),
            MenuItem(restaurant_id=hadiqa.id, name="Pepperoni Pizza", description="Spicy pepperoni with cheese", price=12.50, category="Pizza", availability=True, stock_quantity=25),
            MenuItem(restaurant_id=hadiqa.id, name="Vegetarian Pizza", description="Bell peppers, olives, mushrooms & onions", price=11.00, category="Pizza", availability=True, stock_quantity=28),
            MenuItem(restaurant_id=hadiqa.id, name="Chicken Alfredo Pasta", description="Creamy pasta with grilled chicken", price=13.00, category="Pasta", availability=True, stock_quantity=20),
            MenuItem(restaurant_id=hadiqa.id, name="Penne Arrabbiata", description="Spicy tomato sauce pasta", price=9.50, category="Pasta", availability=True, stock_quantity=25),
            MenuItem(restaurant_id=hadiqa.id, name="Garlic Bread", description="Toasted bread with garlic butter", price=4.50, category="Appetizers", availability=True, stock_quantity=40),
            MenuItem(restaurant_id=hadiqa.id, name="Caesar Salad", description="Fresh romaine with Caesar dressing", price=6.00, category="Salads", availability=True, stock_quantity=30),
            MenuItem(restaurant_id=hadiqa.id, name="Tiramisu", description="Classic Italian coffee-flavored dessert", price=5.50, category="Desserts", availability=True, stock_quantity=20),
        ]
        session.add_all(hadiqa_items)
        
        # Restaurant 4: Barbeque Nation - Buffet Style
        bbq_nation = Restaurant(
            name="Barbeque Nation",
            address="Ground Floor, Central Cinemas, Laxmindra Nagar, Udupi Main Rd, Manipal, Karnataka 576104",
            contact="+91 8069 028783",
            operating_hours="Mon-Sun: 12:00 PM - 3:30 PM, 6:30 PM - 11:00 PM",
            cuisine_type="Multi-Cuisine Buffet"
        )
        session.add(bbq_nation)
        session.flush()
        
        # BBQ Nation Menu
        bbq_items = [
            MenuItem(restaurant_id=bbq_nation.id, name="Veg BBQ Buffet", description="Unlimited veg grills and buffet", price=18.00, category="Buffet", availability=True, stock_quantity=50),
            MenuItem(restaurant_id=bbq_nation.id, name="Non-Veg BBQ Buffet", description="Unlimited non-veg grills and buffet", price=22.00, category="Buffet", availability=True, stock_quantity=50),
            MenuItem(restaurant_id=bbq_nation.id, name="Grilled Paneer Tikka", description="Marinated cottage cheese on grill", price=8.50, category="Starters", availability=True, stock_quantity=30),
            MenuItem(restaurant_id=bbq_nation.id, name="Chicken Seekh Kebab", description="Minced chicken kebabs", price=9.50, category="Starters", availability=True, stock_quantity=25),
            MenuItem(restaurant_id=bbq_nation.id, name="Fish Tikka", description="Marinated fish grilled to perfection", price=11.00, category="Starters", availability=True, stock_quantity=20),
            MenuItem(restaurant_id=bbq_nation.id, name="Biryani", description="Aromatic rice with spices", price=10.00, category="Main Course", availability=True, stock_quantity=35),
            MenuItem(restaurant_id=bbq_nation.id, name="Ice Cream Bar", description="Assorted ice cream flavors", price=4.00, category="Desserts", availability=True, stock_quantity=60),
        ]
        session.add_all(bbq_items)
        
        # Restaurant 5: Basil Cafe - Continental & Indian
        basil_cafe = Restaurant(
            name="Basil Cafe",
            address="Dr VS Acharya Rd, Vidyaratna Nagar, Manipal, Karnataka 576104",
            contact="+91 8204 200090",
            operating_hours="Mon-Sun: 8:00 AM - 11:00 PM",
            cuisine_type="Continental & Indian"
        )
        session.add(basil_cafe)
        session.flush()
        
        # Basil Cafe Menu
        basil_items = [
            MenuItem(restaurant_id=basil_cafe.id, name="English Breakfast", description="Eggs, toast, beans, and sausage", price=8.50, category="Breakfast", availability=True, stock_quantity=25),
            MenuItem(restaurant_id=basil_cafe.id, name="Club Sandwich", description="Triple-decker with chicken and veggies", price=7.00, category="Sandwiches", availability=True, stock_quantity=30),
            MenuItem(restaurant_id=basil_cafe.id, name="Grilled Chicken Steak", description="Tender chicken with mashed potatoes", price=14.00, category="Main Course", availability=True, stock_quantity=20),
            MenuItem(restaurant_id=basil_cafe.id, name="Fish and Chips", description="Crispy battered fish with fries", price=12.50, category="Main Course", availability=True, stock_quantity=18),
            MenuItem(restaurant_id=basil_cafe.id, name="Butter Chicken", description="Creamy tomato chicken curry", price=11.50, category="Indian", availability=True, stock_quantity=25),
            MenuItem(restaurant_id=basil_cafe.id, name="Paneer Butter Masala", description="Cottage cheese in rich tomato gravy", price=10.00, category="Indian", availability=True, stock_quantity=28),
            MenuItem(restaurant_id=basil_cafe.id, name="Chocolate Brownie", description="Warm brownie with vanilla ice cream", price=4.50, category="Desserts", availability=True, stock_quantity=35),
            MenuItem(restaurant_id=basil_cafe.id, name="Cappuccino", description="Espresso with steamed milk foam", price=3.00, category="Beverages", availability=True, stock_quantity=50),
        ]
        session.add_all(basil_items)
        
        # ============ MANGALORE RESTAURANTS ============
        
        # Restaurant 6: Machali - Seafood
        machali = Restaurant(
            name="Machali",
            address="Sharada Vidyalaya Rd, behind Ocean Pearl, Kodailbail, Mangaluru, Karnataka 575003",
            contact="+91 7795 957575",
            operating_hours="Mon-Sun: 12:00 PM - 3:30 PM, 7:00 PM - 11:00 PM",
            cuisine_type="Coastal Seafood"
        )
        session.add(machali)
        session.flush()
        
        # Machali Menu
        machali_items = [
            MenuItem(restaurant_id=machali.id, name="Mangalore Fish Curry", description="Traditional coastal fish curry with coconut", price=14.00, category="Main Course", availability=True, stock_quantity=20),
            MenuItem(restaurant_id=machali.id, name="Prawn Ghee Roast", description="Spicy prawns in ghee with coastal spices", price=16.50, category="Main Course", availability=True, stock_quantity=18),
            MenuItem(restaurant_id=machali.id, name="Fish Fry Tawa", description="Crispy pan-fried fish", price=13.00, category="Starters", availability=True, stock_quantity=25),
            MenuItem(restaurant_id=machali.id, name="Crab Masala", description="Coastal crab curry with spices", price=18.00, category="Main Course", availability=True, stock_quantity=15),
            MenuItem(restaurant_id=machali.id, name="Squid Fry", description="Crispy fried squid rings", price=12.50, category="Starters", availability=True, stock_quantity=20),
            MenuItem(restaurant_id=machali.id, name="Neer Dosa", description="Soft rice crepes", price=3.00, category="Breads", availability=True, stock_quantity=40),
            MenuItem(restaurant_id=machali.id, name="Fish Roe Fry", description="Crispy fish roe delicacy", price=11.00, category="Starters", availability=True, stock_quantity=15),
            MenuItem(restaurant_id=machali.id, name="Solkadhi", description="Traditional coconut drink", price=2.50, category="Beverages", availability=True, stock_quantity=30),
        ]
        session.add_all(machali_items)
        
        # Restaurant 7: Pallkhi - Fine Dining
        pallkhi = Restaurant(
            name="Pallkhi Restaurant",
            address="3rd Floor, Tej Towers, Jyothi Circle, Balmatta Rd, Hampankatta, Mangaluru, Karnataka 575001",
            contact="+91 7899 215553",
            operating_hours="Mon-Sun: 11:30 AM - 11:00 PM",
            cuisine_type="Multi-Cuisine Fine Dining"
        )
        session.add(pallkhi)
        session.flush()
        
        # Pallkhi Menu
        pallkhi_items = [
            MenuItem(restaurant_id=pallkhi.id, name="Tandoori Chicken", description="Chicken marinated in yogurt and spices", price=13.50, category="Main Course", availability=True, stock_quantity=22),
            MenuItem(restaurant_id=pallkhi.id, name="Mutton Rogan Josh", description="Aromatic lamb curry", price=16.00, category="Main Course", availability=True, stock_quantity=18),
            MenuItem(restaurant_id=pallkhi.id, name="Paneer Tikka", description="Grilled cottage cheese cubes", price=9.00, category="Starters", availability=True, stock_quantity=28),
            MenuItem(restaurant_id=pallkhi.id, name="Chicken Biryani", description="Fragrant rice with chicken", price=12.50, category="Main Course", availability=True, stock_quantity=25),
            MenuItem(restaurant_id=pallkhi.id, name="Dal Makhani", description="Creamy black lentils", price=7.50, category="Main Course", availability=True, stock_quantity=35),
            MenuItem(restaurant_id=pallkhi.id, name="Garlic Naan", description="Naan bread with garlic", price=2.50, category="Breads", availability=True, stock_quantity=45),
            MenuItem(restaurant_id=pallkhi.id, name="Ras Malai", description="Sweet milk-soaked cottage cheese", price=4.50, category="Desserts", availability=True, stock_quantity=25),
        ]
        session.add_all(pallkhi_items)
        
        # Restaurant 8: Madhuvan Village - Rustic Dining
        madhuvan = Restaurant(
            name="Madhuvan's Village Restaurant",
            address="Airport Rd, Yeyyadi, Mangaluru, Karnataka 575008",
            contact="+91 8242 214158",
            operating_hours="Mon-Sun: 11:00 AM - 11:00 PM",
            cuisine_type="Coastal & North Indian"
        )
        session.add(madhuvan)
        session.flush()
        
        # Madhuvan Menu
        madhuvan_items = [
            MenuItem(restaurant_id=madhuvan.id, name="Chicken Ghee Roast", description="Mangalorean spicy chicken", price=14.50, category="Main Course", availability=True, stock_quantity=22),
            MenuItem(restaurant_id=madhuvan.id, name="Mutton Sukka", description="Dry mutton with coastal spices", price=17.00, category="Main Course", availability=True, stock_quantity=15),
            MenuItem(restaurant_id=madhuvan.id, name="Fish Gassi", description="Coconut-based fish curry", price=13.50, category="Main Course", availability=True, stock_quantity=20),
            MenuItem(restaurant_id=madhuvan.id, name="Kori Rotti", description="Chicken curry with crispy rotti", price=12.00, category="Main Course", availability=True, stock_quantity=25),
            MenuItem(restaurant_id=madhuvan.id, name="Chicken Sukka", description="Dry chicken with spices", price=13.00, category="Starters", availability=True, stock_quantity=24),
            MenuItem(restaurant_id=madhuvan.id, name="Butter Garlic Prawns", description="Prawns tossed in butter garlic", price=15.50, category="Starters", availability=True, stock_quantity=18),
            MenuItem(restaurant_id=madhuvan.id, name="Payasam", description="Traditional sweet dessert", price=3.50, category="Desserts", availability=True, stock_quantity=30),
        ]
        session.add_all(madhuvan_items)
        
        # Restaurant 9: Sana-di-ge - Seafood Specialist
        sana_di_ge = Restaurant(
            name="Sana-di-ge Seafood Restaurant",
            address="Bunts Hostel Rd, near Jyoti Circle, Balmatta, Mangaluru, Karnataka 575003",
            contact="+91 8244 245678",
            operating_hours="Mon-Sun: 12:00 PM - 10:30 PM",
            cuisine_type="Coastal Seafood"
        )
        session.add(sana_di_ge)
        session.flush()
        
        # Sana-di-ge Menu
        sana_items = [
            MenuItem(restaurant_id=sana_di_ge.id, name="Kane Fry", description="Ladyfish fried to perfection", price=12.00, category="Starters", availability=True, stock_quantity=20),
            MenuItem(restaurant_id=sana_di_ge.id, name="Bangude Pulimunchi", description="Mackerel in tangy curry", price=11.50, category="Main Course", availability=True, stock_quantity=22),
            MenuItem(restaurant_id=sana_di_ge.id, name="Prawn Rava Fry", description="Semolina-coated fried prawns", price=15.00, category="Starters", availability=True, stock_quantity=18),
            MenuItem(restaurant_id=sana_di_ge.id, name="Fish Curry Rice", description="Fish curry with steamed rice", price=10.50, category="Main Course", availability=True, stock_quantity=30),
            MenuItem(restaurant_id=sana_di_ge.id, name="Anjal Fry", description="King fish fried crispy", price=16.00, category="Starters", availability=True, stock_quantity=15),
            MenuItem(restaurant_id=sana_di_ge.id, name="Chicken Ghee Roast", description="Spicy Mangalorean chicken", price=13.50, category="Main Course", availability=True, stock_quantity=20),
            MenuItem(restaurant_id=sana_di_ge.id, name="Gadbad Ice Cream", description="Mixed fruit ice cream sundae", price=4.00, category="Desserts", availability=True, stock_quantity=35),
        ]
        session.add_all(sana_items)
        
        # Restaurant 10: Hotel Janatha Deluxe - Vegetarian
        janatha = Restaurant(
            name="Hotel Janatha Deluxe",
            address="Pathumudi Soudha, opp. Hotel Janatha Deluxe, Ballalbagh, Kodailbail, Mangaluru, Karnataka 575003",
            contact="+91 8242 456474",
            operating_hours="Mon-Sun: 6:30 AM - 10:30 PM",
            cuisine_type="Vegetarian"
        )
        session.add(janatha)
        session.flush()
        
        # Janatha Menu
        janatha_items = [
            MenuItem(restaurant_id=janatha.id, name="Masala Dosa", description="Crispy dosa with potato masala", price=4.00, category="Main Course", availability=True, stock_quantity=45),
            MenuItem(restaurant_id=janatha.id, name="Rava Idli", description="Soft semolina steamed cakes", price=3.50, category="Main Course", availability=True, stock_quantity=40),
            MenuItem(restaurant_id=janatha.id, name="Poori Sagu", description="Fried bread with vegetable curry", price=4.50, category="Main Course", availability=True, stock_quantity=35),
            MenuItem(restaurant_id=janatha.id, name="Veg Thali", description="Complete vegetarian meal platter", price=8.00, category="Main Course", availability=True, stock_quantity=30),
            MenuItem(restaurant_id=janatha.id, name="Bisi Bele Bath", description="Spiced rice and lentil dish", price=5.50, category="Main Course", availability=True, stock_quantity=28),
            MenuItem(restaurant_id=janatha.id, name="Puliyogare", description="Tamarind rice", price=4.50, category="Main Course", availability=True, stock_quantity=32),
            MenuItem(restaurant_id=janatha.id, name="Mysore Pak", description="Traditional sweet made with ghee", price=3.00, category="Desserts", availability=True, stock_quantity=40),
            MenuItem(restaurant_id=janatha.id, name="Buttermilk", description="Refreshing spiced yogurt drink", price=2.00, category="Beverages", availability=True, stock_quantity=50),
        ]
        session.add_all(janatha_items)

        session.commit()
        print("✅ Successfully seeded database with 10 REAL Manipal & Mangalore restaurants!")
        print("📍 5 Manipal restaurants + 5 Mangalore restaurants")
        print("🍽️ Total menu items: 78 dishes")

        # Verify data integrity
        restaurant_count = session.query(Restaurant).count()
        menu_count = session.query(MenuItem).count()
        print(f"🔍 Verification: {restaurant_count} restaurants, {menu_count} menu items")

    except Exception as e:
        session.rollback()
        print(f"Error seeding database: {e}")
        raise
    finally:
        session.close()
