# CycleX API Postman Collections - HTTP Version

This directory contains Postman collections for testing the CycleX API endpoints that have been converted from JSON-RPC to HTTP.

## 🔧 Setup Instructions

### 1. Environment Variables

Create a Postman environment with the following variables:

```json
{
  "base_url": "http://localhost:8069",
  "language": "en",
  "user_id": "",
  "user_name": "",
  "user_type": "",
  "verification_phone": "",
  "session_id": "",
  "collector_id": "",
  "collector_name": "",
  "collector_status": ""
}
```

### 2. Authentication

The API uses Odoo's session-based authentication. After successful login, you'll need to:

1. **Extract Session ID**: From the login response cookies, extract the `session_id` value
2. **Set Environment Variable**: Store it in the `session_id` environment variable
3. **Use in Requests**: Include it in subsequent requests as a Cookie header

## 📋 Collection Overview

### Authentication Flow
- **01-login**: User login (customer/collector)
- **02-signup**: User registration
- **03-verify-otp**: Phone number verification
- **04-resend-otp**: Resend verification code

### Customer Collections
- **08-categories-list**: Get product categories
- **09-13**: Category-specific product listings
- **14-add-new-item**: Create custom recycling request
- **19-my-orders**: List user's orders
- **22-rating-order**: Rate completed orders
- **23-profile**: Get user profile
- **24-update-profile**: Update user profile
- **25-profile-wallet**: Get wallet balance
- **26-wallet-transactions**: Get transaction history

### Collector Collections
- **28-login-collector**: Collector login
- **29-signup-collector**: Collector registration
- **31-collector-home**: Get available orders
- **33-scan-qr**: Scan QR code for order verification
- **34-accept-order**: Accept an order
- **35-reject-order**: Reject an order
- **36-collector-finish-order**: Complete an order

## 🔄 Key Changes from JSON-RPC

### 1. Request Format
**Before (JSON-RPC):**
```json
{
  "jsonrpc": "2.0",
  "method": "call",
  "params": {
    "phone": "01000000000",
    "password": "secret123"
  }
}
```

**After (HTTP):**
```json
{
  "phone": "01000000000",
  "password": "secret123"
}
```

### 2. Response Format
**Before (JSON-RPC):**
```json
{
  "jsonrpc": "2.0",
  "id": null,
  "result": {
    "success": true,
    "data": {...}
  }
}
```

**After (HTTP):**
```json
{
  "success": true,
  "data": {...}
}
```

### 3. HTTP Status Codes
The API now returns proper HTTP status codes:
- `200`: Success
- `201`: Created (registration)
- `400`: Bad Request (validation errors)
- `401`: Unauthorized (invalid credentials)
- `403`: Forbidden (access denied)
- `404`: Not Found
- `409`: Conflict (already exists)
- `500`: Server Error

### 4. Authentication
- **Session-based**: Uses Odoo's built-in session management
- **Cookie header**: `Cookie: session_id={{session_id}}`
- **No Bearer tokens**: Unlike typical REST APIs, this uses session cookies

## 🧪 Testing Workflow

### Customer Flow
1. **Register**: Use `02-signup` to create account
2. **Verify**: Use `03-verify-otp` with verification code
3. **Login**: Use `01-login` to authenticate
4. **Browse**: Use `08-categories-list` to see categories
5. **Create Order**: Use `14-add-new-item` to create recycling request
6. **Track**: Use `19-my-orders` to see order status
7. **Rate**: Use `22-rating-order` after completion

### Collector Flow
1. **Register**: Use `29-signup-collector` to create collector account
2. **Login**: Use `28-login-collector` to authenticate
3. **Browse Orders**: Use `31-collector-home` to see available orders
4. **Accept**: Use `34-accept-order` to accept an order
5. **Scan**: Use `33-scan-qr` to verify pickup
6. **Complete**: Use `36-collector-finish-order` to finish order

## 🔍 Request Examples

### Login Request
```http
POST /api/cyclex/auth/login
Content-Type: application/json

{
  "phone": "01000000000",
  "password": "secret123",
  "fcm_token": "optional_fcm_token"
}
```

### Categories Request
```http
POST /api/cyclex/catalog/categories
Content-Type: application/json

{
  "language": "en",
  "parent_id": null
}
```

### Profile Request (Authenticated)
```http
POST /api/cyclex/user/profile
Content-Type: application/json
Cookie: session_id=your_session_id_here

{}
```

## 🐛 Troubleshooting

### Common Issues

1. **401 Unauthorized**
   - Check if session_id is set correctly
   - Verify login was successful
   - Session may have expired - login again

2. **403 Forbidden**
   - User type mismatch (customer vs collector endpoints)
   - Account not verified or approved
   - Insufficient permissions

3. **400 Bad Request**
   - Missing required parameters
   - Invalid data format
   - Validation errors

4. **CSRF Errors**
   - All routes have `csrf=False` for API usage
   - If you encounter CSRF errors, check route configuration

### Debug Tips

1. **Check Response Body**: Always examine the full response for error details
2. **Verify Headers**: Ensure Content-Type is `application/json`
3. **Session Management**: Monitor session_id in cookies
4. **Environment Variables**: Verify all required variables are set

## 📝 Notes

- All endpoints support both JSON and form data
- The `postman_compatibility_controller.py` provides URL mapping
- Some endpoints may require specific user types (customer/collector)
- Phone verification is required for most operations
- Collector accounts need admin approval before use

## 🔗 Related Files

- `/controllers/postman_compatibility_controller.py`: URL routing
- `/controllers/auth_controller.py`: Authentication logic
- `/controllers/category_product_controller.py`: Catalog endpoints
- `/controllers/wallet_controller.py`: Wallet operations
- `/controllers/collector_controller.py`: Collector operations
- `/controllers/request_controller.py`: Order management