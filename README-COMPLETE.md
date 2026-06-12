# Project PORTKEY - Food Ordering Platform

A comprehensive food ordering platform with Flask frontend, Spring Boot backend (optional), ML-powered chatbot, and Razorpay payment gateway integration (INR ₹).

## 🌟 Features

### Core Features
- **User Authentication**: Secure login and registration system
- **Restaurant Browsing**: Browse multiple restaurants by cuisine type (Italian, Chinese, Indian, Mexican, American)
- **Menu Management**: View detailed menus with real-time stock tracking
- **Shopping Cart**: Add, update, and remove items with quantity management
- **Payment Gateway**: Razorpay integration for secure payments in Indian Rupees (₹)
- **ML Chatbot**: NLP-powered chatbot for customer support and food recommendations

### Technical Features
- Flask-based web application with SQLAlchemy ORM
- SQLite database for data persistence
- Spring Boot backend integration capability (optional)
- Real-time inventory management
- Session-based cart for guest users
- Responsive UI with Tailwind CSS
- RESTful API architecture

## 📁 Project Structure

```
portkey/
├── app.py                      # Enhanced Flask app with Razorpay (INR) integration
├── models.py                   # Database models (User, Restaurant, MenuItem, CartItem)
├── db.py                       # Database initialization and seeding
├── chatbot.py                  # ML chatbot module with NLP
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables (create from .env.example)
├── setup.py                    # Database setup script
├── database.db                 # SQLite database (auto-generated)
│
├── templates/                  # Jinja2 HTML templates
│   ├── base.html              # Base template with navigation
│   ├── index.html             # Homepage with restaurants
│   ├── restaurant.html        # Restaurant menu page
│   ├── cart.html              # Shopping cart with Razorpay
│   ├── login.html             # User login
│   ├── register.html          # User registration
│   ├── chatbot.html           # Chatbot interface
│   └── thank_you.html         # Order confirmation
│
├── static/                     # Static files
│   ├── css/
│   │   └── style.css          # Custom styles
│   └── js/
│       ├── chatbot.js         # Chatbot client logic
│       └── payment.js         # Razorpay payment handling
│
└── backend/                    # Spring Boot backend (optional)
    ├── src/
    │   └── main/
    │       ├── java/
    │       │   └── com/portkey/
    │       │       └── PortkeyApplication.java
    │       └── resources/
    │           ├── application.properties
    │           ├── application-h2.properties
    │           └── application-mysql.properties
    └── pom.xml
```

## 🚀 Quick Start (5 Minutes)

### Prerequisites
1. **Python 3.8+** installed
2. **pip** package manager
3. **Razorpay Account** (free signup at https://razorpay.com/)
4. **(Optional)** Java 11+ and Maven for Spring Boot backend

### Installation Steps

#### Step 1: Setup Virtual Environment

**Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

#### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

#### Step 3: Configure Environment Variables

1. Copy the provided `.env.example` to `.env`:
```bash
# Windows
copy .env.example .env

# Mac/Linux
cp .env.example .env
```

2. Edit `.env` with your credentials:
```
SECRET_KEY=your_random_secret_key_minimum_32_characters
RAZORPAY_KEY_ID=rzp_test_your_key_id_here
RAZORPAY_KEY_SECRET=your_secret_key_here
PORT=5000
```

**Getting Razorpay Keys:**
1. Sign up at https://razorpay.com/
2. Login to Dashboard: https://dashboard.razorpay.com/
3. Switch to "Test Mode" (top menu)
4. Navigate to Settings → API Keys
5. Click "Generate Test Key"
6. Copy Key ID and Secret to `.env`

#### Step 4: Initialize Database

```bash
python setup.py
```

This creates SQLite database with:
- 5 sample restaurants
- 45+ menu items
- User authentication tables
- Cart management tables

#### Step 5: Run the Application

```bash
python app.py
```

Or using Flask CLI:
```bash
flask --app app.py run
```

**Access the application:**
- Homepage: http://localhost:5000
- Chatbot: http://localhost:5000/chatbot-page

## 💳 Razorpay Payment Gateway (INR)

### Configuration Details

**Currency**: Indian Rupees (₹)
**Conversion Rate**: 1 USD = ₹83 (configurable in `app.py`)

All prices stored in database are in USD but displayed and processed in INR.

### Test Mode Payment

**Test Cards:**
- Card: 4111 1111 1111 1111
- CVV: Any 3 digits
- Expiry: Any future date
- OTP: 123456

**Supported Methods:**
- Credit/Debit Cards (Visa, Mastercard, RuPay)
- UPI (Google Pay, PhonePe, Paytm, etc.)
- Net Banking
- Wallets (Paytm, PhonePe, Mobikwik)

### Going Live (Production)

1. Complete KYC verification on Razorpay Dashboard
2. Switch to "Live Mode" in Dashboard
3. Generate Live API Keys
4. Update `.env` with live keys:
```
RAZORPAY_KEY_ID=rzp_live_your_live_key
RAZORPAY_KEY_SECRET=your_live_secret
```
5. Deploy application with HTTPS enabled

## 🤖 ML Chatbot Integration

### Features

The NLP-powered chatbot can assist with:
- Restaurant information and cuisine types
- Menu queries and item details
- Order placement guidance
- Payment methods and pricing
- Food recommendations
- Stock availability
- General customer support

### Using the Chatbot

**Web Interface:**
Visit: http://localhost:5000/chatbot-page

**API Endpoint:**
```bash
POST /api/chatbot
Content-Type: application/json

{
  "message": "Which restaurants are available?"
}
```

**Response:**
```json
{
  "response": "We have Italian, Chinese, Indian, Mexican, and American cuisines available.",
  "intent": "restaurant_query",
  "confidence": 0.85
}
```

### Customizing Chatbot

Edit `chatbot.py` to add new intents:

```python
'new_intent': {
    'patterns': [r'pattern1', r'pattern2'],
    'responses': [
        "Response 1",
        "Response 2"
    ]
}
```

## 🔗 Spring Boot Backend Integration (Optional)

If your friend provided a Spring Boot backend:

### Step 1: Start Spring Boot

```bash
cd backend
mvn clean install
mvn spring-boot:run
```

Default port: **8080**

### Step 2: Configure Flask

Update `.env`:
```
SPRING_BOOT_API_URL=http://localhost:8080/api
```

### Step 3: Backend API Endpoints

The Spring Boot backend provides:
- `GET /api/restaurants` - List all restaurants
- `GET /api/menu-items` - List menu items
- `POST /api/orders` - Create orders
- `GET /api/users` - User management

### Integration Code

Add to `app.py` to call Spring Boot APIs:

```python
import requests

BACKEND_URL = os.getenv('SPRING_BOOT_API_URL')

def get_restaurants_from_backend():
    response = requests.get(f'{BACKEND_URL}/restaurants')
    return response.json()
```

## 📱 Usage Guide

### For Customers

1. **Browse Restaurants**
   - Open homepage
   - View 5 restaurants with different cuisines

2. **View Menu**
   - Click "View Menu" on any restaurant
   - See prices in ₹ (INR)
   - Check stock availability

3. **Add to Cart**
   - Select quantity (1-20 items)
   - Click "Add to Cart"
   - Cart updates automatically

4. **Checkout**
   - Click cart icon
   - Review items
   - Click "Pay via Razorpay"
   - Complete payment with test card

5. **Order Confirmation**
   - Payment verified automatically
   - Order placed
   - Cart cleared

6. **Use Chatbot**
   - Click chatbot link
   - Ask questions
   - Get instant help

### For Developers

#### Add New Restaurant

Edit `db.py`:

```python
new_restaurant = Restaurant(
    name="Your Restaurant",
    address="123 Street",
    contact="(555) 123-4567",
    operating_hours="Mon-Sun: 10AM-10PM",
    cuisine_type="Your Cuisine"
)
session.add(new_restaurant)
```

#### Change Currency Rate

Edit `app.py`:

```python
USD_TO_INR = 83.0  # Update this value
```

#### Add Menu Items

```python
new_item = MenuItem(
    restaurant_id=restaurant_id,
    name="Item Name",
    description="Description",
    price=15.99,  # USD
    category="Main",
    availability=True,
    stock_quantity=50
)
```

## 📋 File Descriptions

### Core Files

**app.py** (Enhanced with Razorpay INR)
- Main Flask application
- All routes and API endpoints
- Razorpay order creation
- Payment verification
- INR currency conversion

**chatbot.py** (ML Chatbot)
- NLP-based intent matching
- Pattern recognition
- Response generation
- Confidence scoring

**models.py** (Database Models)
- User (authentication)
- Restaurant
- MenuItem (with stock tracking)
- CartItem

**db.py** (Database Setup)
- Database initialization
- Sample data seeding
- 5 restaurants with 9 items each

**setup.py** (Quick Setup)
- One-command database initialization
- Calls init_db() and seed_db()

### Frontend Files

**templates/chatbot.html**
- Chatbot interface
- Real-time messaging
- Quick query buttons

**static/js/payment.js**
- Razorpay checkout integration
- Payment verification
- Error handling

**templates/cart.html** (Updated for INR)
- Shopping cart display
- Razorpay payment button
- Prices in ₹ (INR)

### Configuration Files

**requirements.txt**
- Flask 3.0+
- SQLAlchemy 2.0+
- razorpay 1.4+
- flask-cors
- python-dotenv

**.env.example**
- Template for environment variables
- Razorpay configuration
- Port and secret keys

## 🔒 Security Notes

1. **Never commit `.env`** - Contains sensitive API keys
2. **Use Test Mode** during development
3. **Verify signatures** server-side (implemented)
4. **Change SECRET_KEY** before deployment
5. **Enable HTTPS** in production
6. **Rate limit** chatbot API
7. **Validate** all user inputs

## 🐛 Troubleshooting

### "Module razorpay not found"
```bash
pip install razorpay
```

### "Database not initialized"
```bash
rm database.db
python setup.py
```

### "Port 5000 already in use"
Edit `.env`:
```
PORT=5001
```

### "Razorpay connection error"
- Check internet connection
- Verify API keys in `.env`
- Ensure Test Mode is enabled
- Keys should start with `rzp_test_`

### "Payment verification failed"
- Check RAZORPAY_KEY_SECRET is correct
- Verify signature matching logic
- Enable debug mode: `app.run(debug=True)`

### "Chatbot not responding"
- Check `/api/chatbot` endpoint
- Verify chatbot.py is in same directory
- Check Flask logs for errors

## 📊 Database Schema

### Users
- id (PK), username, email, password_hash, created_at

### Restaurants
- id (PK), name, address, contact, operating_hours, cuisine_type

### Menu Items
- id (PK), restaurant_id (FK), name, description
- price (USD), category, availability, stock_quantity

### Cart Items
- id (PK), session_id, user_id (FK)
- menu_item_id (FK), quantity, unit_price

## 🎨 Customization

### Change Theme Colors

Edit templates (Tailwind classes):
```html
<!-- Primary color: orange-600 -->
<div class="bg-orange-600">

<!-- Change to blue -->
<div class="bg-blue-600">
```

### Add New Page

1. Create template in `templates/`
2. Add route in `app.py`:
```python
@app.route('/your-page')
def your_page():
    return render_template('your_page.html')
```

## 📞 API Documentation

### Flask Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Homepage with restaurants |
| GET | `/restaurant/<id>` | Restaurant menu |
| POST | `/cart/add` | Add item to cart |
| GET | `/cart` | View cart (INR) |
| POST | `/create-order` | Create Razorpay order |
| POST | `/verify-payment` | Verify payment signature |
| POST | `/api/chatbot` | Chatbot API |
| GET | `/chatbot-page` | Chatbot interface |
| GET/POST | `/login` | User login |
| GET/POST | `/register` | User registration |
| GET | `/logout` | User logout |

## 🚀 Deployment

### Heroku Deployment

1. Create `Procfile`:
```
web: python app.py
```

2. Deploy:
```bash
heroku create portkey-app
git push heroku main
```

3. Set environment variables:
```bash
heroku config:set RAZORPAY_KEY_ID=your_key
heroku config:set RAZORPAY_KEY_SECRET=your_secret
```

### Docker Deployment

Create `Dockerfile`:
```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```

Build and run:
```bash
docker build -t portkey .
docker run -p 5000:5000 portkey
```

## 📚 Additional Resources

- **Flask Documentation**: https://flask.palletsprojects.com/
- **Razorpay API Docs**: https://razorpay.com/docs/
- **SQLAlchemy ORM**: https://www.sqlalchemy.org/
- **Tailwind CSS**: https://tailwindcss.com/

## 🤝 Contributing

This is an educational project. To extend:
1. Fork the repository
2. Create feature branch
3. Make changes
4. Test thoroughly
5. Document changes

## 📄 License

Educational/Lab Project - Free to use and modify for learning purposes

## 👨‍💻 Authors

- **Frontend & Integration**: Your Name
- **Backend (Spring Boot)**: Your Friend
- **Project**: PORTKEY Team

## 🙏 Acknowledgments

- Flask Framework
- Razorpay Payment Gateway
- SQLAlchemy ORM
- Tailwind CSS
- Python Community

---

**🍕 Happy Coding! Made with ❤️ by PORTKEY Team 🚀**

For support or questions, refer to the troubleshooting section or check official documentation.
