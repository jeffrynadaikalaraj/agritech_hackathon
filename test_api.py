"""
AgriFlow API Test Script
Tests the main endpoints before going live
"""
import requests
import json

BASE_URL = "http://localhost:8000"

print("🌾 AgriFlow API Test Suite")
print("=" * 50)

# --- TEST 1: Health Check ---
print("\n1️⃣ Testing Health Check...")
try:
    response = requests.get(f"{BASE_URL}/health")
    print(f"✅ Status: {response.status_code}")
    print(f"Response: {response.json()}")
except Exception as e:
    print(f"❌ Error: {e}")

# --- TEST 2: Root Endpoint ---
print("\n2️⃣ Testing Root Endpoint...")
try:
    response = requests.get(f"{BASE_URL}/")
    print(f"✅ Status: {response.status_code}")
    print(f"Message: {response.json()['message']}")
    print(f"Available endpoints: {list(response.json()['endpoints'].keys())}")
except Exception as e:
    print(f"❌ Error: {e}")

# --- TEST 3: Mandi Prices ---
print("\n3️⃣ Testing Mandi Prices Endpoint...")
try:
    response = requests.get(f"{BASE_URL}/mandi-prices/Madurai")
    print(f"✅ Status: {response.status_code}")
    data = response.json()
    print(f"District: {data['district']}")
    print(f"Prices: {data['prices']}")
except Exception as e:
    print(f"❌ Error: {e}")

# --- TEST 4: Mandi Webhook (Simulate Sale) ---
print("\n4️⃣ Testing Mandi Webhook...")
try:
    mandi_data = {
        "farmer_mobile": "9176543210",
        "commodity": "Rice",
        "quantity": 5.0,
        "sale_amount": 16000,
        "mandi_id": "ENAM-TN-2025-TEST"
    }
    response = requests.post(f"{BASE_URL}/webhook/mandi", json=mandi_data)
    print(f"✅ Status: {response.status_code}")
    result = response.json()
    print(f"Result: {result['status']}")
    print(f"Message: {result.get('message', 'No message')}")
except Exception as e:
    print(f"❌ Error: {e}")

# --- TEST 5: API Test Endpoint ---
print("\n5️⃣ Testing API Test Endpoint...")
try:
    response = requests.get(f"{BASE_URL}/api/test")
    print(f"✅ Status: {response.status_code}")
    print(f"Response: {response.json()}")
except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "=" * 50)
print("✅ All tests completed!")
print("\n📋 Next Steps:")
print("1. Set up Twilio WhatsApp sandbox")
print("2. Configure ngrok: ngrok http 8000")
print("3. Set webhook URL in Twilio console")
print("4. Send WhatsApp message to test bot")
print("\n🔗 API Docs: http://localhost:8000/docs")
