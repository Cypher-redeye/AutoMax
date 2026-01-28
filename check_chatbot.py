import requests
import json
import sys

def test_chatbot():
    url = "http://127.0.0.1:8000/chatbot/predict/"
    payload = {"message": "Hello"}
    headers = {"Content-Type": "application/json"}

    print(f"Testing Chatbot API at {url}...")
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=5)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Response: {data}")
            if 'answer' in data:
                print("✅ Test PASSED: Chatbot replied.")
            else:
                print("❌ Test FAILED: Invalid response format.")
        else:
            print("❌ Test FAILED: Non-200 status code.")
            print(response.text)
    except requests.exceptions.ConnectionError:
        print("❌ Test FAILED: Connection refused. Is the server running?")
    except Exception as e:
        print(f"❌ Test FAILED: Error {e}")

if __name__ == "__main__":
    test_chatbot()
