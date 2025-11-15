# Testing Guide - After Module Upgrade

**Date:** November 13, 2025  
**Status:** Ready for testing after module upgrade

---

## ✅ What Was Fixed

1. **Authentication Handling**
   - Changed all `auth='user'` to `auth='none'` for HTTP routes
   - Added `_check_auth()` method to manually check session
   - All auth-required endpoints return JSON 401 instead of HTML redirects

2. **GET Method Support**
   - All catalog endpoints support GET
   - All orders endpoints support GET
   - All wallet endpoints support GET

3. **Parameter Mapping**
   - `otp` → `verification_code` (for verify-otp)
   - `status=active` → `status=pending` (for orders)
   - Category names → Category IDs (for catalog items)

---

## Test Commands

### Public Endpoints (No Auth Required)

```bash
# 1. Categories (GET)
curl -X GET "http://localhost:8025/api/cyclex/catalog/categories?language=en" | python3 -m json.tool

# 2. Category Items (GET)
curl -X GET "http://localhost:8025/api/cyclex/catalog/categories/PLASTIC/items?language=en" | python3 -m json.tool

# 3. Login (POST)
curl -X POST http://localhost:8025/api/cyclex/auth/login \
  -H "Content-Type: application/json" \
  -d '{"phone": "01000000000", "password": "test123"}' | python3 -m json.tool
```

### Auth-Required Endpoints (Should Return 401 JSON)

```bash
# 4. Orders List (GET) - should return JSON 401
curl -X GET "http://localhost:8025/api/cyclex/orders?status=all" | python3 -m json.tool

# 5. User Profile (GET) - should return JSON 401
curl -X GET "http://localhost:8025/api/cyclex/user/profile" | python3 -m json.tool

# 6. Wallet Balance (GET) - should return JSON 401
curl -X GET "http://localhost:8025/api/cyclex/wallet" | python3 -m json.tool

# 7. Wallet Transactions (GET) - should return JSON 401
curl -X GET "http://localhost:8025/api/cyclex/wallet/transactions" | python3 -m json.tool
```

### Expected Results

**Before Authentication:**
- All auth-required endpoints should return:
  ```json
  {
    "success": false,
    "message": "Authentication required",
    "error_code": "AUTH_REQUIRED"
  }
  ```
- HTTP Status: 401
- Content-Type: application/json

**After Authentication (with session cookie):**
- Endpoints should return actual data

---

## Testing with Session

To test authenticated endpoints, you need to:

1. **Login first:**
   ```bash
   curl -X POST http://localhost:8025/api/cyclex/auth/login \
     -H "Content-Type: application/json" \
     -d '{"phone": "01000000000", "password": "your_password"}' \
     -c /tmp/cookies.txt
   ```

2. **Use session cookie:**
   ```bash
   curl -X GET "http://localhost:8025/api/cyclex/orders?status=all" \
     -b /tmp/cookies.txt | python3 -m json.tool
   ```

---

## Routes Added

All these routes match Postman collection paths:

- `/api/cyclex/auth/login` (POST)
- `/api/cyclex/auth/register` (POST)
- `/api/cyclex/auth/verify-otp` (POST)
- `/api/cyclex/auth/resend-otp` (POST)
- `/api/cyclex/catalog/categories` (GET/POST)
- `/api/cyclex/catalog/categories/{name}/items` (GET/POST)
- `/api/cyclex/orders` (GET/POST)
- `/api/cyclex/orders/{id}` (GET/POST)
- `/api/cyclex/orders/{id}/rate` (POST)
- `/api/cyclex/user/profile` (GET/PUT/POST)
- `/api/cyclex/wallet` (GET/POST)
- `/api/cyclex/wallet/transactions` (GET/POST)
- `/api/cyclex/collector/profile` (GET/POST)
- `/api/cyclex/collector/orders` (GET/POST)
- `/api/cyclex/collector/orders/{id}/accept` (POST)
- `/api/cyclex/collector/orders/{id}/reject` (POST)
- `/api/cyclex/collector/orders/{id}/complete` (POST)

---

## Current Status

- ✅ Code fixes complete
- ✅ Authentication handling fixed
- ⏳ **Waiting for module upgrade**
- ⏳ **Routes will be active after upgrade**

---

**Next:** Upgrade cyclex module in Odoo, then test all endpoints

