import requests

def test_chatbot_api():
    """Test chatbot API endpoints."""

    base_url = 'http://127.0.0.1:5000'

    test_cases = [
        {'message': 'hello', 'expected_intent': 'greetings'},
        {'message': 'show me restaurants', 'expected_intent': 'restaurant_query'},
        {'message': 'what food do you have', 'expected_intent': 'menu_query'},
        {'message': 'how do I order', 'expected_intent': 'order_help'},
        {'message': 'how do I pay', 'expected_intent': 'payment_info'},
        {'message': 'where are you located', 'expected_intent': 'location_query'},
        {'message': 'what are your hours', 'expected_intent': 'hours_query'},
        {'message': 'I have feedback', 'expected_intent': 'feedback'},
        {'message': 'any specials today', 'expected_intent': 'specials'},
        {'message': 'recommend something', 'expected_intent': 'recommendation'},
        {'message': 'bye', 'expected_intent': 'goodbye'},
        {'message': '', 'expected_intent': 'empty_message'},
    ]

    print("🧪 Testing Chatbot API Endpoints")
    print("=" * 50)

    for i, test_case in enumerate(test_cases, 1):
        try:
            response = requests.post(f'{base_url}/api/chatbot',
                                   json={'message': test_case['message']},
                                   timeout=10)

            print(f"Test {i}: '{test_case['message'][:30]}...'")
            print(f"  Status: {response.status_code}")

            if response.status_code == 200:
                data = response.json()
                intent = data.get('intent')
                success = data.get('success', False)

                print(f"  Intent: {intent}")
                print(f"  Success: {success}")
                print(f"  Response length: {len(data.get('response', ''))}")

                # Check if intent matches expectation
                if intent == test_case['expected_intent']:
                    print("  ✅ Intent match")
                else:
                    print(f"  ❌ Expected: {test_case['expected_intent']}, Got: {intent}")

            else:
                print(f"  ❌ HTTP Error: {response.status_code}")

            print()

        except requests.exceptions.RequestException as e:
            print(f"Test {i}: REQUEST ERROR - {e}")
            print()

    print("API Testing completed!")

if __name__ == '__main__':
    test_chatbot_api()
