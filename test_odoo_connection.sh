#!/bin/bash
# Quick test script to verify Odoo connection

echo "🔍 Testing Odoo Connection..."
echo ""

# Test 1: Odoo Web
echo "1. Testing Odoo Web (http://localhost:8025)..."
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8025/web 2>/dev/null)
if [ "$HTTP_CODE" = "200" ] || [ "$HTTP_CODE" = "302" ]; then
    echo "   ✅ Odoo web is accessible (HTTP $HTTP_CODE)"
else
    echo "   ❌ Odoo web not accessible (HTTP $HTTP_CODE)"
fi

# Test 2: API Health Check
echo ""
echo "2. Testing API Health Check..."
API_RESPONSE=$(curl -s http://localhost:8025/api/cyclex/health-check 2>/dev/null)
if echo "$API_RESPONSE" | grep -q "success\|status"; then
    echo "   ✅ API is responding"
    echo "$API_RESPONSE" | python3 -m json.tool 2>/dev/null | head -5
else
    echo "   ❌ API not responding"
    echo "   Response: $API_RESPONSE"
fi

# Test 3: Categories Endpoint
echo ""
echo "3. Testing Categories Endpoint..."
CAT_RESPONSE=$(curl -s "http://localhost:8025/api/cyclex/catalog/categories?language=en" 2>/dev/null)
if echo "$CAT_RESPONSE" | grep -q "categories\|success"; then
    echo "   ✅ Categories endpoint working"
else
    echo "   ⚠️  Categories endpoint may have issues"
fi

echo ""
echo "📝 To test from Streamlit:"
echo "   1. Set USE_DEMO_DATA = False in streamlit_app.py"
echo "   2. Restart Streamlit"
echo "   3. Open http://localhost:8501"
