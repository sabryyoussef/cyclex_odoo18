# Corrected Endpoint Matrix v3

**Generated:** November 15, 2025  
**Purpose:** Updated mapping based on current implementation analysis

---

## Current Status Summary

After analyzing the actual controller implementations and Postman collections, here are the corrected mappings:

---

## Authentication Endpoints

| # | Collection | Postman Path | Postman Method | Odoo Path | Odoo Method | Status | Notes |
|---|------------|--------------|----------------|-----------|-------------|--------|-------|
| 01 | Login | `/api/cyclex/auth/login` | POST | `/api/cyclex/login` | POST | ⚠️ **PATH MISMATCH** | Extra `/auth` segment in Postman |
| 02 | Sign Up | `/api/cyclex/auth/register` | POST | `/api/cyclex/register` | POST | ⚠️ **PATH MISMATCH** | Extra `/auth` segment in Postman |
| 03 | Verify OTP | `/auth/verify-otp` | POST | `/api/cyclex/verify` | POST | ⚠️ **PATH MISMATCH** | Missing `/api/cyclex` prefix |
| 04 | Resend OTP | `/auth/resend-otp` | POST | `/api/cyclex/resend-code` | POST | ⚠️ **PATH MISMATCH** | Missing `/api/cyclex` prefix |

**Key Issues:**
- Collections 01-02: Have been partially updated but include extra `/auth` segment
- Collections 03-04: Still missing `/api/cyclex` prefix
- Parameter mismatch: Collection 03 uses `otp` but controller expects `verification_code`

---

## Profile Endpoints

| # | Collection | Postman Path | Postman Method | Odoo Path | Odoo Method | Status | Notes |
|---|------------|--------------|----------------|-----------|-------------|--------|-------|
| 23 | Profile | `/user/profile` | GET | `/api/cyclex/profile` | POST | ⚠️ **PATH + METHOD MISMATCH** | Controller uses POST, not GET |
| 24 | Update Profile | `/user/profile` | PUT | `/api/cyclex/update-profile` | POST | ⚠️ **PATH + METHOD MISMATCH** | Different path and method |

**Key Issues:**
- Profile endpoint in controller uses POST method with `auth='user'`
- Postman collections expect GET method
- Update profile uses different path structure

---

## Wallet Endpoints

| # | Collection | Postman Path | Postman Method | Odoo Path | Odoo Method | Status | Notes |
|---|------------|--------------|----------------|-----------|-------------|--------|-------|
| 25 | Profile Wallet | `/wallet` | GET | `/api/cyclex/wallet/balance` | POST | ⚠️ **PATH + METHOD MISMATCH** | Controller uses POST method |
| 26 | Wallet Transactions | `/wallet/transactions` | GET | `/api/cyclex/wallet/transactions` | POST | ⚠️ **METHOD MISMATCH** | Controller uses POST method |

**Key Issues:**
- All wallet endpoints in controller use POST method, not GET
- This is likely for security/authentication reasons

---

## Critical Corrections Needed

### 1. Fix Postman Collection Paths

**Collections 01-02 (Login/Signup):**
```
Current: /api/cyclex/auth/login
Correct: /api/cyclex/login

Current: /api/cyclex/auth/register  
Correct: /api/cyclex/register
```

**Collections 03-04 (Verify/Resend):**
```
Current: /auth/verify-otp
Correct: /api/cyclex/verify

Current: /auth/resend-otp
Correct: /api/cyclex/resend-code
```

### 2. Fix HTTP Methods in Postman

**All authenticated endpoints should use POST:**
- Profile: GET → POST
- Wallet Balance: GET → POST  
- Wallet Transactions: GET → POST

### 3. Fix Parameter Names

**Collection 03 (Verify OTP):**
```json
// Current
{
  "phone": "01000000000",
  "otp": "123456"
}

// Correct
{
  "phone": "01000000000", 
  "verification_code": "123456"
}
```

---

## Implementation Notes

### Authentication Pattern
The controller implements a pattern where:
- Public endpoints (login, register, verify) use `auth='public'`
- Authenticated endpoints (profile, wallet) use `auth='user'` with POST method
- This provides better security for authenticated operations

### Response Format
All endpoints return consistent format:
```json
{
  "success": true/false,
  "message": "Status message",
  "data": { ... },
  "error_code": "ERROR_CODE" // on failure
}
```

### Session Management
- Login creates an Odoo session
- Subsequent requests use session authentication
- No explicit token management needed

---

## Recommended Actions

### Priority 1: Fix Postman Collections
1. Update paths in collections 01-04
2. Change methods to POST for authenticated endpoints
3. Fix parameter names in collection 03

### Priority 2: Update Documentation
1. Correct the endpoint matrix
2. Update API documentation with correct methods
3. Document the POST-based authentication pattern

### Priority 3: Test Updated Collections
1. Verify all corrected endpoints work
2. Test session persistence
3. Validate response formats

---

**Status:** Ready for implementation  
**Next Step:** Apply corrections to Postman collections
