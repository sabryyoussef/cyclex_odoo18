#!/bin/bash

# CycleX API Test Script
# This script demonstrates how to test the HTTP API endpoints

BASE_URL="http://localhost:8069"
CONTENT_TYPE="Content-Type: application/json"

echo "🚀 CycleX API Test Script"
echo "=========================="

# Test 1: Health Check
echo "1. Testing Health Check..."
curl -X POST "$BASE_URL/api/cyclex/health" \
  -H "$CONTENT_TYPE" \
  -d '{}' \
  | jq '.'

echo -e "\n"

# Test 2: Register Customer
echo "2. Testing Customer Registration..."
REGISTER_RESPONSE=$(curl -s -X POST "$BASE_URL/api/cyclex/auth/register" \
  -H "$CONTENT_TYPE" \
  -d '{
    "name": "Test Customer",
    "phone": "01000000001",
    "password": "test123",
    "confirm_password": "test123",
    "user_type": "customer",
    "language": "en"
  }')

echo "$REGISTER_RESPONSE" | jq '.'

# Extract verification code (for testing - remove in production)
VERIFICATION_CODE=$(echo "$REGISTER_RESPONSE" | jq -r '.data.verification_code // "123456"')
echo "Verification Code: $VERIFICATION_CODE"

echo -e "\n"

# Test 3: Verify Phone
echo "3. Testing Phone Verification..."
VERIFY_RESPONSE=$(curl -s -X POST "$BASE_URL/api/cyclex/auth/verify-otp" \
  -H "$CONTENT_TYPE" \
  -d "{
    \"phone\": \"01000000001\",
    \"verification_code\": \"$VERIFICATION_CODE\"
  }")

echo "$VERIFY_RESPONSE" | jq '.'

echo -e "\n"

# Test 4: Login
echo "4. Testing Login..."
LOGIN_RESPONSE=$(curl -s -X POST "$BASE_URL/api/cyclex/auth/login" \
  -H "$CONTENT_TYPE" \
  -c cookies.txt \
  -d '{
    "phone": "01000000001",
    "password": "test123"
  }')

echo "$LOGIN_RESPONSE" | jq '.'

# Extract session ID from cookies
SESSION_ID=$(grep session_id cookies.txt | cut -f7)
echo "Session ID: $SESSION_ID"

echo -e "\n"

# Test 5: Get Categories (authenticated)
echo "5. Testing Get Categories..."
curl -X POST "$BASE_URL/api/cyclex/catalog/categories" \
  -H "$CONTENT_TYPE" \
  -H "Cookie: session_id=$SESSION_ID" \
  -d '{
    "language": "en"
  }' \
  | jq '.'

echo -e "\n"

# Test 6: Get Profile (authenticated)
echo "6. Testing Get Profile..."
curl -X POST "$BASE_URL/api/cyclex/user/profile" \
  -H "$CONTENT_TYPE" \
  -H "Cookie: session_id=$SESSION_ID" \
  -d '{}' \
  | jq '.'

echo -e "\n"

# Test 7: Get Wallet Balance (authenticated)
echo "7. Testing Get Wallet Balance..."
curl -X POST "$BASE_URL/api/cyclex/wallet" \
  -H "$CONTENT_TYPE" \
  -H "Cookie: session_id=$SESSION_ID" \
  -d '{}' \
  | jq '.'

echo -e "\n"

# Cleanup
rm -f cookies.txt

echo "✅ API Test Complete!"
echo ""
echo "📋 Next Steps:"
echo "1. Import the Postman collections from this directory"
echo "2. Import the environment template: CycleX-Environment-Template.postman_environment.json"
echo "3. Update the base_url in the environment to match your server"
echo "4. Run the collections in order: 01-login → 02-signup → 03-verify-otp → etc."
echo ""
echo "🔧 Troubleshooting:"
echo "- Ensure Odoo server is running on the specified base_url"
echo "- Check that the cyclex module is installed and updated"
echo "- Verify that all controllers are properly loaded"
