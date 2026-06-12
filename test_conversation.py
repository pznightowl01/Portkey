import requests

def test_conversation_flow():
    """Test conversation flow with the chatbot."""

    base_url = 'http://127.0.0.1:5000'

    print('💬 Testing Conversation Flow')
    print('=' * 30)

    conversation = [
        'hello',
        'show me restaurants',
        'what food do you have',
        'recommend something',
        'how do I order',
        'bye'
    ]

    for i, message in enumerate(conversation, 1):
        try:
            response = requests.post(f'{base_url}/api/chatbot',
                                   json={'message': message},
                                   timeout=5)
            if response.status_code == 200:
                data = response.json()
                intent = data.get('intent')
                print(f'{i}. "{message}" -> {intent}')
            else:
                print(f'{i}. "{message}" -> HTTP {response.status_code}')
        except Exception as e:
            print(f'{i}. "{message}" -> ERROR: {e}')

    print()
    print('✅ Conversation flow testing completed!')

if __name__ == '__main__':
    test_conversation_flow()
