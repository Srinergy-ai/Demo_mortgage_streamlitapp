import requests
import json

# REPLACE WITH YOUR NEW API KEY
API_KEY = "sk-2SaD6g6b_BwAn6E4ENaoSpaJVby01xRDxOGnYI3l8Bo"
URL = "http://20.186.92.51:7860/api/v1/run/2d675e5c-32e2-4f32-a47b-c454b48c6965"

def test_api():
    headers = {
        "Content-Type": "application/json",
        "x-api-key": API_KEY
    }
    
    payload = {
        "input_value": "hello",
        "output_type": "chat",
        "input_type": "chat",
        "session_id": "test-123"
    }
    
    print("Testing Langflow API...")
    print(f"URL: {URL}")
    print(f"API Key: {API_KEY[:10]}...{API_KEY[-5:]}")  # Show partial key
    
    try:
        response = requests.post(URL, json=payload, headers=headers, timeout=30)
        print(f"\nStatus Code: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ SUCCESS! API is working.")
            data = response.json()
            print("\nResponse Preview:")
            print(json.dumps(data, indent=2)[:500])
        else:
            print(f"❌ FAILED! Error: {response.status_code}")
            print(f"Response: {response.text}")
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Connection Error: {str(e)}")

if __name__ == "__main__":
    test_api()