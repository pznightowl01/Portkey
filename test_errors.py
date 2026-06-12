import requests

def test_error_handling():
    """Test error handling scenarios."""

    base_url = 'http://127.0.0.1:5000'

    print('🚨 Testing Error Handling')
    print('=' * 30)

    # Test invalid chatbot request
    try:
        response = requests.post(f'{base_url}/api/chatbot',
                               json={},  # Empty JSON
                               timeout=5)
        print(f'Empty JSON request: {response.status_code}')
        if response.status_code != 200:
            data = response.json()
            print(f'  Error: {data.get("error")}')
    except Exception as e:
        print(f'Empty JSON request: ERROR - {e}')

    # Test invalid restaurant ID
    try:
        response = requests.get(f'{base_url}/restaurant/99999', timeout=5)
        print(f'Invalid restaurant ID: {response.status_code}')
    except Exception as e:
        print(f'Invalid restaurant ID: ERROR - {e}')

    # Test chatbot with invalid data
    try:
        response = requests.post(f'{base_url}/api/chatbot',
                               json={'invalid_key': 'test'},
                               timeout=5)
        print(f'Invalid chatbot data: {response.status_code}')
        if response.status_code == 200:
            data = response.json()
            print(f'  Intent: {data.get("intent")}')
    except Exception as e:
        print(f'Invalid chatbot data: ERROR - {e}')

    print()
    print('✅ Error handling testing completed!')

if __name__ == '__main__':
    test_error_handling()
