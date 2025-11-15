#!/bin/bash
# CycleX API Test Script using cURL
# Tests endpoints with proper JSON-RPC 2.0 format

BASE_URL="http://localhost:8025"
API_PREFIX="/api/cyclex"

echo "=========================================="
echo "CycleX API Endpoint Tests"
echo "=========================================="
echo ""

# Test 1: Health Check
echo "1. Testing Health Check..."
curl -X POST "${BASE_URL}${API_PREFIX}/health" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc": "2.0", "method": "call", "params": {}, "id": 1}' \
  -s | python3 -m json.tool 2>/dev/null || echo "Failed"
echo ""
echo "---"
echo ""

# Test 2: Get Categories
echo "2. Testing Get Categories..."
curl -X POST "${BASE_URL}${API_PREFIX}/categories" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc": "2.0", "method": "call", "params": {"language": "en"}, "id": 1}' \
  -s | python3 -m json.tool 2>/dev/null | head -20
echo ""
echo "---"
echo ""

# Test 3: Get Products
echo "3. Testing Get Products..."
curl -X POST "${BASE_URL}${API_PREFIX}/products" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc": "2.0", "method": "call", "params": {"language": "en"}, "id": 1}' \
  -s | python3 -m json.tool 2>/dev/null | head -30
echo ""
echo "---"
echo ""

# Test 4: Get Products by Category
echo "4. Testing Get Products by Category (Plastic Bottles - ID: 8)..."
curl -X POST "${BASE_URL}${API_PREFIX}/products" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc": "2.0", "method": "call", "params": {"category_id": 8, "language": "en"}, "id": 1}' \
  -s | python3 -m json.tool 2>/dev/null | head -30
echo ""
echo "---"
echo ""

# Test 5: Login (will fail without valid credentials, but tests endpoint)
echo "5. Testing Login (expecting error without valid user)..."
curl -X POST "${BASE_URL}${API_PREFIX}/login" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc": "2.0", "method": "call", "params": {"phone": "01000000000", "password": "test123"}, "id": 1}' \
  -s | python3 -m json.tool 2>/dev/null
echo ""
echo "---"
echo ""

# Test 6: Register (will fail if phone exists, but tests endpoint)
echo "6. Testing Register (expecting error if phone exists)..."
curl -X POST "${BASE_URL}${API_PREFIX}/register" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc": "2.0", "method": "call", "params": {"name": "Test User", "phone": "01000000000", "password": "Test123456", "confirm_password": "Test123456", "user_type": "customer", "language": "en"}, "id": 1}' \
  -s | python3 -m json.tool 2>/dev/null
echo ""
echo "=========================================="
echo "Tests Complete"
echo "=========================================="

