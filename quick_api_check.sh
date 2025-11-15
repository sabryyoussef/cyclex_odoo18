#!/bin/bash
# Quick API Health Check before Streamlit Testing

echo "🔍 CycleX API Health Check"
echo "=========================="
echo ""

BASE_URL="http://localhost:8025/api/cyclex"

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test 1: Health Check
echo "1️⃣  Testing Health Check..."
response=$(curl -s -o /dev/null -w "%{http_code}" ${BASE_URL}/health 2>/dev/null)
if [ "$response" = "200" ]; then
    echo -e "   ${GREEN}✓${NC} Health check: OK"
else
    echo -e "   ${RED}✗${NC} Health check: FAILED (HTTP $response)"
fi

# Test 2: Categories
echo ""
echo "2️⃣  Testing Categories Endpoint..."
response=$(curl -s ${BASE_URL}/catalog/categories 2>/dev/null | python3 -c "import sys, json; data=json.load(sys.stdin); print('success' if data.get('success') else 'failed')" 2>/dev/null)
if [ "$response" = "success" ]; then
    count=$(curl -s ${BASE_URL}/catalog/categories | python3 -c "import sys, json; data=json.load(sys.stdin); print(len(data.get('data', {}).get('categories', [])))" 2>/dev/null)
    echo -e "   ${GREEN}✓${NC} Categories: OK (${count} categories found)"
else
    echo -e "   ${RED}✗${NC} Categories: FAILED"
fi

# Test 3: Products
echo ""
echo "3️⃣  Testing Products Endpoint..."
response=$(curl -s "${BASE_URL}/catalog/products?language=en" 2>/dev/null | python3 -c "import sys, json; data=json.load(sys.stdin); print('success' if data.get('success') else 'failed')" 2>/dev/null)
if [ "$response" = "success" ]; then
    count=$(curl -s "${BASE_URL}/catalog/products?language=en" | python3 -c "import sys, json; data=json.load(sys.stdin); print(len(data.get('data', {}).get('products', [])))" 2>/dev/null)
    echo -e "   ${GREEN}✓${NC} Products: OK (${count} products found)"
else
    echo -e "   ${RED}✗${NC} Products: FAILED"
fi

# Test 4: Registration (with test data)
echo ""
echo "4️⃣  Testing Registration..."
test_phone="01000$(date +%s | tail -c 6)"
response=$(curl -s -X POST ${BASE_URL}/auth/register \
  -H "Content-Type: application/json" \
  -d "{\"name\":\"API Test\",\"phone\":\"${test_phone}\",\"password\":\"Test1234\",\"confirm_password\":\"Test1234\",\"user_type\":\"customer\"}" 2>/dev/null | python3 -c "import sys, json; data=json.load(sys.stdin); print('success' if data.get('success') else 'failed')" 2>/dev/null)
if [ "$response" = "success" ]; then
    echo -e "   ${GREEN}✓${NC} Registration: OK (Phone: ${test_phone})"
else
    echo -e "   ${RED}✗${NC} Registration: FAILED"
fi

# Test 5: OTP Verification
echo ""
echo "5️⃣  Testing OTP Verification..."
response=$(curl -s -X POST ${BASE_URL}/auth/verify-otp \
  -H "Content-Type: application/json" \
  -d "{\"phone\":\"${test_phone}\",\"verification_code\":\"123456\"}" 2>/dev/null | python3 -c "import sys, json; data=json.load(sys.stdin); print('success' if data.get('success') else 'failed')" 2>/dev/null)
if [ "$response" = "success" ]; then
    echo -e "   ${GREEN}✓${NC} OTP Verification: OK"
else
    echo -e "   ${RED}✗${NC} OTP Verification: FAILED"
fi

# Test 6: Login
echo ""
echo "6️⃣  Testing Login..."
response=$(curl -s -X POST ${BASE_URL}/auth/login \
  -H "Content-Type: application/json" \
  -d "{\"phone\":\"${test_phone}\",\"password\":\"Test1234\"}" 2>/dev/null | python3 -c "import sys, json; data=json.load(sys.stdin); print('success' if data.get('success') else 'failed')" 2>/dev/null)
if [ "$response" = "success" ]; then
    echo -e "   ${GREEN}✓${NC} Login: OK"
else
    echo -e "   ${RED}✗${NC} Login: FAILED"
fi

echo ""
echo "=========================="
echo "✅ API Check Complete!"
echo ""
echo "📱 Now open Streamlit: http://localhost:8501"
echo "📋 Follow the test guide: STREAMLIT_COMPLETE_FLOW_TEST.md"

