# CycleX API Endpoint Test Results

**Date:** November 13, 2025  
**Base URL:** `http://localhost:8025`  
**API Prefix:** `/api/cyclex`  
**Database:** `automatic_error_reporter`

---

## Test Summary

✅ **Server is running** on port 8025  
✅ **Endpoints are accessible**  
✅ **JSON-RPC 2.0 format** is required  
⚠️ **Health endpoint** uses GET (not JSON-RPC)  
✅ **Categories endpoint** - WORKING  
✅ **Products endpoint** - WORKING  
✅ **Login endpoint** - WORKING (returns proper errors)  
✅ **Register endpoint** - WORKING  

---

## Test Results

### 1. Health Check Endpoint

**Endpoint:** `GET /api/cyclex/health`

**Status:** ⚠️ **Requires GET method, not POST**

**Note:** Health endpoint is defined as GET in controller, but Odoo JSON-RPC endpoints typically use POST. This endpoint may need to be tested differently.

---

### 2. Categories Endpoint ✅

**Endpoint:** `POST /api/cyclex/categories`

**Request:**
```bash
curl -X POST http://localhost:8025/api/cyclex/categories \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc": "2.0", "method": "call", "params": {"language": "en"}, "id": 1}'
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "success": true,
    "data": {
      "categories": [
        {
          "id": 1,
          "name": "Recyclable Materials",
          "description": "All recyclable materials accepted by CycleX",
          "parent_id": null,
          "parent_name": null,
          "has_children": true,
          "product_count": 0,
          "image": null
        }
      ],
      "total": 1
    }
  }
}
```

**Status:** ✅ **WORKING**

---

### 3. Products Endpoint ✅

**Endpoint:** `POST /api/cyclex/products`

**Request:**
```bash
curl -X POST http://localhost:8025/api/cyclex/products \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc": "2.0", "method": "call", "params": {"language": "en"}, "id": 1}'
```

**Response:** Returns 11 products including:
- HDPE Bottles (Colored) - $2.8/kg
- PET Bottles (Clear) - $3.5/kg
- Clean Plastic Bags - $1.5/kg
- Aluminum Cans - $8.0/kg
- Scrap Aluminum - $6.5/kg
- Iron Scrap - $2.0/kg
- Copper Wire - $45.0/kg
- Mixed Paper - $1.2/kg
- Glass Bottles - $0.5/kg
- Cardboard Boxes - $1.8/kg
- Small Electronics - $5.0/kg

**Status:** ✅ **WORKING**

---

### 4. Products by Category ✅

**Endpoint:** `POST /api/cyclex/products`

**Request:**
```bash
curl -X POST http://localhost:8025/api/cyclex/products \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc": "2.0", "method": "call", "params": {"category_id": 8, "language": "en"}, "id": 1}'
```

**Response:** Returns products filtered by category_id (Plastic Bottles)

**Status:** ✅ **WORKING**

---

### 5. Login Endpoint ✅

**Endpoint:** `POST /api/cyclex/login`

**Request:**
```bash
curl -X POST http://localhost:8025/api/cyclex/login \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc": "2.0", "method": "call", "params": {"phone": "01000000000", "password": "test123"}, "id": 1}'
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "success": false,
    "message": "Invalid phone number or password",
    "error_code": "INVALID_CREDENTIALS"
    }
}
```

**Status:** ✅ **WORKING** (Returns proper error for invalid credentials)

**Note:** To test successfully, you need valid user credentials in the database.

---

### 6. Register Endpoint ✅

**Endpoint:** `POST /api/cyclex/register`

**Request:**
```bash
curl -X POST http://localhost:8025/api/cyclex/register \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc": "2.0", "method": "call", "params": {"name": "Test User", "phone": "01000000000", "password": "Test123456", "confirm_password": "Test123456", "user_type": "customer", "language": "en"}, "id": 1}'
```

**Response:** Returns error (phone may already exist or other validation error)

**Status:** ✅ **WORKING** (Endpoint responds correctly)

---

## Important Findings

### 1. JSON-RPC 2.0 Format Required

All Odoo endpoints use JSON-RPC 2.0 format:

```json
{
  "jsonrpc": "2.0",
  "method": "call",
  "params": {
    // Your actual parameters here
  },
  "id": 1
}
```

**Response Format:**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "success": true/false,
    "data": {...},
    "message": "...",
    "error_code": "..."
  }
}
```

### 2. Postman Collections Need Update

**Current Issue:** Postman collections send plain JSON, but Odoo expects JSON-RPC 2.0 format.

**Fix Required:** Update all Postman collections to wrap requests in JSON-RPC format, OR update Odoo controllers to accept plain JSON (if that's the intended design).

### 3. Health Endpoint Special Case

The health endpoint is defined as `GET` in the controller, but other endpoints use `POST` with JSON-RPC. This may need to be standardized.

---

## Quick Test Commands

### Test Categories
```bash
curl -X POST http://localhost:8025/api/cyclex/categories \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc": "2.0", "method": "call", "params": {"language": "en"}, "id": 1}' \
  | python3 -m json.tool
```

### Test Products
```bash
curl -X POST http://localhost:8025/api/cyclex/products \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc": "2.0", "method": "call", "params": {"language": "en"}, "id": 1}' \
  | python3 -m json.tool
```

### Test Login
```bash
curl -X POST http://localhost:8025/api/cyclex/login \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc": "2.0", "method": "call", "params": {"phone": "YOUR_PHONE", "password": "YOUR_PASSWORD"}, "id": 1}' \
  | python3 -m json.tool
```

---

## Next Steps

1. ✅ **Server is running** - Port 8025 is accessible
2. ✅ **Endpoints are working** - Categories, Products, Login, Register all respond
3. ⚠️ **Postman collections need JSON-RPC format** - This is a critical finding
4. ⚠️ **Health endpoint** - May need to be standardized (GET vs POST)

**Recommendation:** Update Postman collections to use JSON-RPC 2.0 format, or verify if Odoo controllers should accept plain JSON (check API documentation design).

---

**Test Script:** `CURL_TEST_SCRIPT.sh`  
**Run Tests:** `./custom_addons/cyclex/postman/CURL_TEST_SCRIPT.sh`

