"""
Hedwig - ML-powered Chatbot for Portkey Food Delivery System
Handles restaurant queries, menu recommendations, order assistance, and customer support.
Enhanced with better pattern matching, conversation flow, and human-like interactions.
"""

import re
import random
import time
from datetime import datetime
from db import SessionLocal
from models import Restaurant, MenuItem

class Chatbot:
    """Hedwig chatbot for food delivery assistance with enhanced conversation capabilities."""

    def __init__(self):
        """Initialize chatbot with intents, database connection, and conversation memory."""
        self.intents = {
            'greetings': {
                'patterns': [
                    r'\b(hi|hello|hey|good morning|good afternoon|good evening|morning|afternoon|evening)\b',
                    r'\b(howdy|what\'s up|sup|yo|wassup)\b',
                    r'\b(start|begin|initiate)\b',
                    r'\b(hola|ciao|salut|namaste)\b'
                ],
                'responses': [
                    "Hello! Welcome to Portkey! 🏆✨ I'm Hedwig, your magical food assistant. How can I help you today?",
                    "Hi there! I'm Hedwig, ready to help you with your food ordering needs! 🦉 What would you like to know?",
                    "Greetings! Welcome to Portkey's magical food world! I'm Hedwig, here to assist you. What can I do for you? ✨",
                    "Hey! Great to see you at Portkey! I'm Hedwig, your friendly food guide. What are you in the mood for? 🍽️",
                    "Hello! Welcome to the world of delicious food delivery! I'm Hedwig, and I'm here to make your ordering experience magical! 🪄"
                ]
            },
            'restaurant_query': {
                'patterns': [
                    r'\b(restaurant|restaurants|places to eat|where to eat|eatery|eateries)\b',
                    r'\b(what.*restaurant|which.*restaurant|show.*restaurant|list.*restaurant)\b',
                    r'\b(available.*restaurant|find.*restaurant)\b',
                    r'\b(dining.*option|food.*place|eat.*place)\b',
                    r'\b(restaurant.*list|restaurant.*directory)\b'
                ],
                'responses': [
                    "We have amazing restaurants in Manipal and Mangalore! Let me show you our fantastic options.",
                    "Here are our incredible restaurants serving delicious food from various cuisines!",
                    "Check out these amazing places to eat from - we have something for every taste!",
                    "Our restaurant collection spans Manipal and Mangalore with diverse culinary delights!",
                    "Let me introduce you to our wonderful restaurants - each one special in its own way!"
                ],
                'follow_up': False
            },
            'menu_query': {
                'patterns': [
                    r'\b(menu|food|dish|item|cuisine)\b.*\b(what|show|see|available|have)\b',
                    r'\b(what.*eat|what.*food|what.*serve|what.*offer)\b',
                    r'\b(show.*menu|see.*menu|view.*menu|check.*menu)\b',
                    r'\b(food.*option|dish.*option|menu.*item)\b',
                    r'\b(what.*special|what.*today|daily.*special)\b',
                    r'\b.*food\b'
                ],
                'responses': [
                    "Let me show you our delicious menu options from various cuisines!",
                    "Here's what we have available to eat - mouthwatering dishes await!",
                    "Check out these tasty dishes we offer - something for every palate!",
                    "Our menu features incredible dishes from different cuisines. Let me show you!",
                    "From appetizers to desserts, we have amazing food options for you!"
                ]
            },
            'recommendation': {
                'patterns': [
                    r'\b(recommend|suggest|best|favorite|popular|top)\b',
                    r'\b(what.*good|what.*try|what.*best|what.*favorite)\b',
                    r'\b(help.*choose|what.*order|what.*pick)\b',
                    r'\b(good.*dish|great.*food|amazing.*food)\b',
                    r'\b(customer.*favorite|people.*like|most.*ordered)\b'
                ],
                'responses': [
                    "I'd be happy to recommend some delicious options based on what you're craving!",
                    "Let me suggest some of our most popular and highly-rated dishes!",
                    "Here are some customer favorites that always get rave reviews!",
                    "Based on what our customers love most, here are some fantastic recommendations!",
                    "I know just what you might enjoy! Let me share some popular choices!"
                ]
            },
            'payment_info': {
                'patterns': [
                    r'\b(how.*pay|how.*payment|payment.*how|what.*payment|payment.*method)\b',
                    r'\b(secure.*payment|safe.*payment|payment.*security)\b',
                    r'\b(accept.*payment|supported.*payment)\b',
                    r'\b(payment|pay|cost|price|money|fee|charge|billing)\b'
                ],
                'responses': [
                    "Ordering is simple and secure! Just add items to your cart and place your order directly.",
                    "No payment gateway needed for this demo! Just click 'Place Order' and your food will be prepared.",
                    "Payment processing is simplified for easy ordering. Your order will be confirmed instantly!",
                    "We make ordering easy - no complex payment steps. Just place your order and enjoy!",
                    "Simple ordering process - add to cart, place order, and your delicious food will be ready soon! 🍽️"
                ]
            },
            'order_help': {
                'patterns': [
                    r'\b(order|ordering|place.*order|make.*order)\b',
                    r'\b(buy|purchase|get.*food|deliver.*food)\b',
                    r'\b(cart|add.*cart|shopping.*cart)\b',
                    r'\b(step.*order|order.*step|ordering.*guide)\b'
                ],
                'responses': [
                    "Ordering is super easy! Just browse restaurants, add items to your cart, and checkout with Razorpay.",
                    "To place an order: 1) Choose a restaurant 2) Add items to cart 3) Proceed to checkout 4) Pay securely!",
                    "Here's how to order: Select your favorite dishes, add them to cart, and complete payment through our secure gateway.",
                    "Getting food delivered is simple: Browse → Add to Cart → Checkout → Pay → Enjoy! It's that easy!",
                    "Let me guide you through ordering: Pick a restaurant, select dishes, add to cart, and complete secure payment!"
                ]
            },
            'location_query': {
                'patterns': [
                    r'\b(where|location|address|area|place)\b.*\b(restaurant|eat|food|deliver|located|locate|you|service)\b',
                    r'\b(where.*you.*located|where.*located|location.*where)\b',
                    r'\b(manipal|mangalore|location|area|locate|located)\b',
                    r'\b(deliver|delivery.*area|service.*area|coverage.*area)\b',
                    r'\b(restaurant.*location|where.*restaurant)\b',
                    r'\b(delivery.*zone|service.*zone)\b',
                    r'\b(where.*located|where.*you.*located)\b',
                    r'\b(where.*located)\b'
                ],
                'responses': [
                    "We serve delicious food in both Manipal and Mangalore! Each restaurant shows its exact location.",
                    "Our restaurants are located in Manipal and Mangalore. Check each restaurant's page for the exact address!",
                    "We have restaurants in both Manipal and Mangalore areas. Delivery available to these locations!",
                    "You can find us in Manipal and Mangalore - two amazing cities with incredible food scenes!",
                    "Our delivery service covers Manipal and Mangalore. Each restaurant page has detailed location info!"
                ]
            },
            'hours_query': {
                'patterns': [
                    r'\b(hour|hours|time|open|close|when|timing|schedule)\b.*\b(open|close|operating|work)\b',
                    r'\b(what.*time|operating.*hour|business.*hour|working.*hour)\b',
                    r'\b(open.*now|closed.*now|open.*today|close.*today)\b',
                    r'\b(restaurant.*hour|kitchen.*hour|shop.*hour)\b',
                    r'\b(breakfast|lunch|dinner).*time\b',
                    r'\b(what.*hour|your.*hour)\b'
                ],
                'responses': [
                    "Most restaurants are open from 11 AM to 11 PM, but hours vary. Check each restaurant's page for exact timings!",
                    "Operating hours typically range from 11 AM to 11 PM, but please check individual restaurant pages for specific schedules.",
                    "Restaurant hours vary, but most are open from morning to evening. See each restaurant's details for exact operating times.",
                    "Our restaurants generally operate from 11 AM to 11 PM, but some have different hours. Always check the specific restaurant page!",
                    "Timings vary by restaurant, but most serve from 11 AM to 11 PM. The exact hours are listed on each restaurant's page!"
                ]
            },
            'feedback': {
                'patterns': [
                    r'\b(feedback|review|rate|rating|comment)\b',
                    r'\b(complaint|issue|problem|wrong|bad)\b',
                    r'\b(suggestion|improve|better|enhancement)\b',
                    r'\b(support|help|assistance|contact)\b',
                    r'\b(report.*issue|technical.*problem)\b'
                ],
                'responses': [
                    "We value your feedback! Please share your experience or any suggestions you have.",
                    "Your feedback helps us improve! What would you like to share about your experience?",
                    "We'd love to hear from you! Please tell us about your experience or any concerns.",
                    "Customer feedback is important to us. How can we make your experience better?",
                    "Thank you for reaching out! We're here to help with any feedback or concerns you have."
                ]
            },
            'specials': {
                'patterns': [
                    r'\b(special|specials|deal|offer|discount|promotion)\b',
                    r'\b(cheap|budget|affordable|value)\b',
                    r'\b(today.*special|daily.*deal|current.*offer)\b',
                    r'\b(save.*money|money.*saving|best.*price)\b',
                    r'\b(combo|meal.*deal|package.*deal)\b',
                    r'\b(any.*special)\b'
                ],
                'responses': [
                    "We often have great deals and specials! Check individual restaurant pages for current offers.",
                    "Keep an eye on our restaurants for amazing deals and combo offers!",
                    "Our restaurants frequently run specials and promotions. Browse to see what's available!",
                    "Great food at great prices! Check each restaurant for their current deals and specials.",
                    "We love offering value to our customers! Look for specials on restaurant pages."
                ]
            },
            'goodbye': {
                'patterns': [
                    r'\b(bye|goodbye|see you|thank|thanks|appreciate)\b',
                    r'\b(exit|quit|end|finish|done)\b',
                    r'\b(later|catch.*you|talk.*later)\b',
                    r'\b(have.*good.*day|enjoy.*day)\b'
                ],
                'responses': [
                    "Thank you for chatting with me! Enjoy your meal from Portkey! 🦉✨",
                    "Goodbye! Hope to see you again soon for more delicious food! 🏆",
                    "Thanks for using Portkey! Have a magical day and enjoy your food! ✨",
                    "It was great chatting with you! Come back anytime for more food adventures! 🍽️",
                    "Thanks for choosing Portkey! Have an amazing meal and see you soon! 🌟"
                ]
            },
            'fallback': {
                'patterns': [r'.*'],
                'responses': [
                    "I'm not sure I understand. Could you please rephrase your question? I'm here to help with restaurants, menus, orders, and payments! 🦉",
                    "Hmm, I'm still learning! Try asking about our restaurants, menu items, or how to place an order. ✨",
                    "I didn't quite catch that. Ask me about food recommendations, restaurant info, or ordering help! 🏆",
                    "I'm here to help with food ordering! Try asking about restaurants, menus, recommendations, or how to order.",
                    "Let me help you with your food needs! Ask about restaurants, menus, ordering, or payments. What would you like to know?"
                ]
            }
        }

        # Conversation memory for context awareness
        self.conversation_memory = {}
        self.max_memory_items = 5

    def get_restaurants_info(self):
        """Get formatted list of restaurants from database."""
        try:
            db = SessionLocal()
            restaurants = db.query(Restaurant).all()
            db.close()

            if not restaurants:
                return "Sorry, no restaurants are currently available."

            response = "🏪 **Our Restaurants:**\n\n"
            for restaurant in restaurants:
                response += f"🍽️ **{restaurant.name}**\n"
                response += f"   📍 {restaurant.address}\n"
                response += f"   📞 {restaurant.contact}\n"
                response += f"   🕐 {restaurant.operating_hours}\n"
                response += f"   🍜 Cuisine: {restaurant.cuisine_type}\n\n"

            return response
        except Exception as e:
            return "Sorry, I'm having trouble accessing restaurant information right now. Please try again later."

    def get_menu_sample(self):
        """Get sample of popular menu items."""
        try:
            from sqlalchemy.orm import joinedload
            db = SessionLocal()
            # Get some popular items from different categories with restaurant info
            items = db.query(MenuItem).options(joinedload(MenuItem.restaurant)).filter(
                MenuItem.availability == True,
                MenuItem.stock_quantity > 0
            ).limit(8).all()
            db.close()

            if not items:
                return "Sorry, menu items are currently unavailable."

            response = "🍕 **Popular Menu Items:**\n\n"
            for item in items:
                price_inr = float(item.price) * 83.0  # Convert to INR
                response += f"🍽️ **{item.name}**\n"
                response += f"   📝 {item.description}\n"
                response += f"   💰 ₹{price_inr:.0f} ({item.category})\n"
                response += f"   🏪 {item.restaurant.name}\n\n"

            return response
        except Exception as e:
            return "Sorry, I'm having trouble accessing menu information right now."

    def get_recommendations(self):
        """Get food recommendations."""
        recommendations = [
            "🍛 Try the Butter Chicken from Dollops - it's absolutely delicious!",
            "🍜 The Hakka Noodles from Dollops are a customer favorite!",
            "🍕 Margherita Pizza from Hadiqa is perfect for pizza lovers!",
            "🐟 Don't miss the Mangalore Fish Curry from Machali - authentic coastal cuisine!",
            "🍗 Chicken Ghee Roast from Madhuvan's is a must-try Mangalorean specialty!",
            "🥘 For vegetarian options, try the Masala Dosa from Pai Tiffins!",
            "🍰 Gulab Jamun from Dollops makes a perfect dessert!",
            "☕ Filter Coffee from Pai Tiffins is the best way to end your meal!"
        ]
        return random.choice(recommendations) + "\n\nBrowse our restaurants to see the full menu! 🏪"

    def match_intent(self, message):
        """Match user message to intent using regex patterns."""
        message = message.lower().strip()

        for intent_name, intent_data in self.intents.items():
            for pattern in intent_data['patterns']:
                if re.search(pattern, message, re.IGNORECASE):
                    return intent_name, intent_data

        return 'fallback', self.intents['fallback']

    def get_response(self, user_message, user_id=None):
        """Generate response based on user message with context awareness."""
        try:
            # Clean and normalize message
            user_message = user_message.strip()
            if not user_message:
                return {
                    'response': "I didn't receive any message. How can I help you with food ordering today? 🦉",
                    'intent': 'empty_message',
                    'success': True
                }

            # Match intent
            intent, intent_data = self.match_intent(user_message)

            # Get base response
            response = random.choice(intent_data['responses'])

            # Add context-aware elements
            response = self.add_context_awareness(response, intent, user_id)

            # Add specific information based on intent
            if intent == 'restaurant_query':
                # Check if follow_up is disabled for this intent
                if intent_data.get('follow_up', True):
                    response += "\n\n" + self.get_restaurants_info()
                else:
                    # Provide a concise response without overwhelming details
                    response += "\n\nWe have 10 amazing restaurants across Manipal and Mangalore! You can browse them on our homepage or ask me about specific cuisines. 🏪"

            elif intent == 'menu_query':
                response += "\n\n" + self.get_menu_sample()

            elif intent == 'recommendation':
                response += "\n\n" + self.get_recommendations()

            elif intent == 'order_help':
                response += "\n\n💡 **Quick Order Steps:**\n"
                response += "1. Browse restaurants on homepage\n"
                response += "2. Click 'View Menu' on any restaurant\n"
                response += "3. Add items to cart with desired quantity\n"
                response += "4. Click cart icon to review order\n"
                response += "5. Click 'Place Order Now' button\n"
                response += "6. Your order will be confirmed instantly!\n\n"
                response += "Your delicious food will be prepared soon! 🎉"

            elif intent == 'payment_info':
                response += "\n\n💳 **Accepted Payment Methods:**\n"
                response += "• PhonePe (UPI)\n"
                response += "• Google Pay (UPI)\n"
                response += "• Credit/Debit Cards (Visa, Mastercard, RuPay)\n"
                response += "• Net Banking (all major banks)\n\n"
                response += "All payments are processed securely in Indian Rupees (₹)! 🛡️"

            elif intent == 'location_query':
                response += "\n\n📍 **Service Areas:**\n"
                response += "• Manipal (multiple restaurants)\n"
                response += "• Mangalore (coastal specialties)\n\n"
                response += "Each restaurant page shows exact address and contact info!"

            elif intent == 'hours_query':
                response += "\n\n🕐 **Typical Hours:**\n"
                response += "• Breakfast places: 7 AM - 10 PM\n"
                response += "• Regular restaurants: 11 AM - 11 PM\n"
                response += "• Some places have lunch/dinner buffets\n\n"
                response += "Check individual restaurant pages for exact timings!"

            elif intent == 'feedback':
                response += "\n\n📧 **Contact Information:**\n"
                response += "• Email: support@portkey.com\n"
                response += "• Phone: +91-XXXXXXXXXX\n"
                response += "• Website: www.portkey.com/support\n\n"
                response += "We appreciate your feedback and will get back to you soon! 🙏"

            elif intent == 'specials':
                response += "\n\n🎯 **Current Specials:**\n"
                response += "• Check individual restaurant pages for daily deals\n"
                response += "• Combo offers and discounts available\n"
                response += "• Student and bulk order discounts\n\n"
                response += "Specials change frequently - browse now to see what's available! ⭐"

            # Update conversation memory
            self.update_conversation_memory(user_id, intent, user_message)

            # Return as JSON for API
            return {
                'response': response,
                'intent': intent,
                'success': True
            }

        except Exception as e:
            print(f"Chatbot error: {str(e)}")  # For debugging
            return {
                'response': "Sorry, I'm experiencing some technical difficulties. Please try again in a moment! 🦉",
                'intent': 'error',
                'success': False,
                'error': str(e)
            }

    def add_context_awareness(self, response, intent, user_id):
        """Add context-aware elements to responses."""
        if not user_id:
            return response

        # Get recent conversation context
        recent_intents = self.get_recent_intents(user_id, 3)

        # Add follow-up suggestions based on context
        if intent == 'greetings' and 'restaurant_query' in recent_intents:
            response += " I remember you were looking at restaurants earlier. Would you like me to show them again?"
        elif intent == 'menu_query' and 'recommendation' in recent_intents:
            response += " Since you asked for recommendations before, I can also show you our full menu!"
        elif intent == 'order_help' and 'payment_info' in recent_intents:
            response += " I see you were asking about payments. The ordering process is simple and secure!"

        return response

    def update_conversation_memory(self, user_id, intent, message):
        """Update conversation memory for context awareness."""
        if not user_id:
            return

        if user_id not in self.conversation_memory:
            self.conversation_memory[user_id] = []

        # Add new interaction
        self.conversation_memory[user_id].append({
            'intent': intent,
            'message': message[:100],  # Truncate long messages
            'timestamp': datetime.now()
        })

        # Keep only recent interactions
        if len(self.conversation_memory[user_id]) > self.max_memory_items:
            self.conversation_memory[user_id] = self.conversation_memory[user_id][-self.max_memory_items:]

    def get_recent_intents(self, user_id, count=3):
        """Get recent intents from conversation memory."""
        if user_id not in self.conversation_memory:
            return []

        recent = self.conversation_memory[user_id][-count:]
        return [item['intent'] for item in recent]

# Create global chatbot instance
chatbot = Chatbot()
