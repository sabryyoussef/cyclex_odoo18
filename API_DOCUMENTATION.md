# CycleX API Documentation

**Base URL:** `http://localhost:10018`  
**Format:** JSON  
**Version:** 1.0.0

---

## Authentication

All authenticated endpoints require a valid Odoo session. Use the `/api/cyclex/login` endpoint to authenticate.

---

## 1. Authentication APIs

### 1.1 Health Check
**Endpoint:** `GET /api/cyclex/health`  
**Auth:** Public  
**Description:** Verify API is running

**Response:**
```json
{
  "status": "ok",
  "message": "CycleX API is running",
  "version": "1.0.0"
}
```

---

### 1.2 Login
**Endpoint:** `POST /api/cyclex/login`  
**Auth:** Public  
**Description:** User login with phone number and password

**Request Body:**
```json
{
  "phone": "01234567890",
  "password": "password123",
  "fcm_token": "optional_fcm_token"
}
```

**Success Response:**
```json
{
  "success": true,
  "message": "Login successful",
  "data": {
    "user_id": 123,
    "name": "John Doe",
    "phone": "01234567890",
    "email": "john@example.com",
    "user_type": "customer",
    "language": "en",
    "account_status": "active",
    "verified": true,
    "total_requests": 5,
    "total_earnings": 1500.00
  }
}
```

**Error Codes:**
- `MISSING_PARAMS` - Missing required parameters
- `INVALID_CREDENTIALS` - Wrong phone/password
- `PHONE_NOT_VERIFIED` - Phone not verified
- `ACCOUNT_SUSPENDED` - Account suspended/banned

---

### 1.3 Register
**Endpoint:** `POST /api/cyclex/register`  
**Auth:** Public  
**Description:** Register new user (customer or collector)

**Request Body (Customer):**
```json
{
  "name": "John Doe",
  "phone": "01234567890",
  "password": "password123",
  "confirm_password": "password123",
  "user_type": "customer",
  "fcm_token": "optional_token",
  "language": "en"
}
```

**Request Body (Collector):**
```json
{
  "name": "John Collector",
  "phone": "01234567890",
  "password": "password123",
  "confirm_password": "password123",
  "user_type": "collector",
  "id_number": "12345678901234",
  "vehicle_type": "car",
  "working_area_ids": [1, 2, 3],
  "fcm_token": "optional_token",
  "language": "ar"
}
```

**Success Response:**
```json
{
  "success": true,
  "message": "Registration successful. Please verify your phone number.",
  "data": {
    "user_id": 124,
    "phone": "01234567890",
    "name": "John Doe",
    "user_type": "customer",
    "verification_code": "123456",
    "verification_sent": true
  }
}
```

**Error Codes:**
- `MISSING_PARAMS` - Missing required fields
- `PASSWORD_MISMATCH` - Passwords don't match
- `WEAK_PASSWORD` - Password < 6 characters
- `PHONE_EXISTS` - Phone already registered
- `INVALID_USER_TYPE` - Invalid user type

---

### 1.4 Verify Phone
**Endpoint:** `POST /api/cyclex/verify`  
**Auth:** Public  
**Description:** Verify phone number with SMS code

**Request Body:**
```json
{
  "phone": "01234567890",
  "verification_code": "123456"
}
```

**Success Response:**
```json
{
  "success": true,
  "message": "Phone verified successfully",
  "data": {
    "user_id": 124,
    "name": "John Doe",
    "phone": "01234567890",
    "user_type": "customer",
    "account_status": "active",
    "verified": true
  }
}
```

**Error Codes:**
- `MISSING_PARAMS` - Missing phone or code
- `USER_NOT_FOUND` - User not found
- `ALREADY_VERIFIED` - Phone already verified
- `INVALID_CODE` - Invalid or expired code

---

### 1.5 Resend Verification Code
**Endpoint:** `POST /api/cyclex/resend-code`  
**Auth:** Public  
**Description:** Resend verification code via SMS

**Request Body:**
```json
{
  "phone": "01234567890"
}
```

**Success Response:**
```json
{
  "success": true,
  "message": "Verification code sent successfully",
  "data": {
    "verification_code": "654321",
    "phone": "01234567890"
  }
}
```

---

### 1.6 Get Profile
**Endpoint:** `GET /api/cyclex/profile`  
**Auth:** Required  
**Description:** Get current user profile

**Success Response:**
```json
{
  "success": true,
  "data": {
    "user_id": 123,
    "name": "John Doe",
    "phone": "01234567890",
    "email": "john@example.com",
    "user_type": "customer",
    "language": "en",
    "account_status": "active",
    "verified": true,
    "gps_latitude": 30.0444,
    "gps_longitude": 31.2357,
    "total_requests": 5,
    "total_earnings": 1500.00
  }
}
```

---

### 1.7 Update Profile
**Endpoint:** `POST /api/cyclex/update-profile`  
**Auth:** Required  
**Description:** Update user profile

**Request Body:**
```json
{
  "name": "John Doe Updated",
  "email": "newemail@example.com",
  "language": "ar",
  "fcm_token": "new_token",
  "gps_latitude": 30.0444,
  "gps_longitude": 31.2357
}
```

**Success Response:**
```json
{
  "success": true,
  "message": "Profile updated successfully",
  "data": {
    "user_id": 123,
    "name": "John Doe Updated"
  }
}
```

---

## 2. Categories & Products APIs

### 2.1 Get Categories
**Endpoint:** `GET /api/cyclex/categories`  
**Auth:** Public  
**Description:** Get list of categories (hierarchical)

**Query Parameters:**
- `parent_id` (optional): Filter by parent category
- `language` (optional): 'en' or 'ar'

**Success Response:**
```json
{
  "success": true,
  "data": {
    "categories": [
      {
        "id": 1,
        "name": "Plastic",
        "description": "Plastic recyclables",
        "parent_id": null,
        "parent_name": null,
        "has_children": true,
        "product_count": 5,
        "image": "base64_encoded_image"
      }
    ],
    "total": 10
  }
}
```

---

### 2.2 Get Products
**Endpoint:** `GET /api/cyclex/products`  
**Auth:** Public  
**Description:** Get list of products

**Query Parameters:**
- `category_id` (optional): Filter by category
- `search` (optional): Search by name
- `language` (optional): 'en' or 'ar'

**Success Response:**
```json
{
  "success": true,
  "data": {
    "products": [
      {
        "id": 1,
        "name": "Plastic Bottles",
        "description": "Empty plastic bottles",
        "category_id": 1,
        "category_name": "Plastic",
        "price_per_kg": 5.00,
        "currency": "EGP",
        "currency_symbol": "E£",
        "image": "base64_encoded_image"
      }
    ],
    "total": 15
  }
}
```

---

### 2.3 Get Product Details
**Endpoint:** `GET /api/cyclex/product/<int:product_id>`  
**Auth:** Public  
**Description:** Get detailed product information

**Success Response:**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "name": "Plastic Bottles",
    "description": "Empty plastic bottles",
    "category_id": 1,
    "category_name": "Plastic",
    "price_per_kg": 5.00,
    "currency": "EGP",
    "currency_symbol": "E£",
    "image": "base64_encoded_image",
    "request_count": 150
  }
}
```

---

## 3. Request/Order APIs

### 3.1 Create Request
**Endpoint:** `POST /api/cyclex/request/create`  
**Auth:** Required (Customer)  
**Description:** Create a new recycling request

**Request Body:**
```json
{
  "category_id": 1,
  "product_id": 5,
  "quantity": 10,
  "weight": 5.5,
  "pickup_date": "2025-10-20",
  "photo_1": "base64_encoded_photo",
  "photo_2": "base64_encoded_photo",
  "gps_latitude": 30.0444,
  "gps_longitude": 31.2357
}
```

**Success Response:**
```json
{
  "success": true,
  "message": "Request created successfully",
  "data": {
    "request_id": 456,
    "request_number": "CX00456",
    "status": "pending",
    "calculated_price": 27.50,
    "currency_symbol": "E£",
    "qr_code": "CX00456-XXXXX",
    "pickup_date": "2025-10-20",
    "product_name": "Plastic Bottles",
    "category_name": "Plastic"
  }
}
```

---

### 3.2 List Requests
**Endpoint:** `GET /api/cyclex/request/list`  
**Auth:** Required  
**Description:** Get user's request history

**Query Parameters:**
- `status` (optional): Filter by status
- `limit` (optional): Number of results (default: 20)
- `offset` (optional): Pagination offset

**Success Response:**
```json
{
  "success": true,
  "data": {
    "requests": [
      {
        "id": 456,
        "request_number": "CX00456",
        "status": "pending",
        "product_name": "Plastic Bottles",
        "category_name": "Plastic",
        "quantity": 10,
        "weight": 5.5,
        "calculated_price": 27.50,
        "currency_symbol": "E£",
        "pickup_date": "2025-10-20",
        "create_date": "2025-10-17 21:30:00",
        "collector_name": null,
        "rating": null
      }
    ],
    "total": 5,
    "limit": 20,
    "offset": 0
  }
}
```

---

### 3.3 Get Request Details
**Endpoint:** `GET /api/cyclex/request/details/<int:request_id>`  
**Auth:** Required  
**Description:** Get full request details including QR code

**Success Response:**
```json
{
  "success": true,
  "data": {
    "id": 456,
    "request_number": "CX00456",
    "status": "assigned",
    "customer_name": "John Doe",
    "customer_phone": "01234567890",
    "collector_name": "Collector Name",
    "collector_phone": "01987654321",
    "category_id": 1,
    "category_name": "Plastic",
    "product_id": 5,
    "product_name": "Plastic Bottles",
    "quantity": 10,
    "weight": 5.5,
    "calculated_price": 27.50,
    "currency_symbol": "E£",
    "pickup_date": "2025-10-20",
    "create_date": "2025-10-17 21:30:00",
    "completion_date": null,
    "qr_code": "CX00456-XXXXX",
    "rating": null,
    "comments": "",
    "photo_1": "base64_encoded_photo",
    "photo_2": "base64_encoded_photo",
    "customer_address": {
      "street": "123 Main St",
      "city": "Cairo",
      "latitude": 30.0444,
      "longitude": 31.2357
    }
  }
}
```

---

### 3.4 Cancel Request
**Endpoint:** `POST /api/cyclex/request/cancel/<int:request_id>`  
**Auth:** Required (Customer)  
**Description:** Cancel a pending request

**Success Response:**
```json
{
  "success": true,
  "message": "Request cancelled successfully",
  "data": {
    "request_id": 456,
    "status": "cancelled"
  }
}
```

---

## 4. Collector APIs

### 4.1 Get Available Orders
**Endpoint:** `GET /api/cyclex/collector/available-orders`  
**Auth:** Required (Collector)  
**Description:** Get orders available in collector's working areas

**Query Parameters:**
- `limit` (optional): Number of results (default: 20)
- `offset` (optional): Pagination offset

**Success Response:**
```json
{
  "success": true,
  "data": {
    "orders": [
      {
        "id": 456,
        "request_number": "CX00456",
        "product_name": "Plastic Bottles",
        "category_name": "Plastic",
        "weight": 5.5,
        "calculated_price": 27.50,
        "currency_symbol": "E£",
        "pickup_date": "2025-10-20",
        "customer_name": "John Doe",
        "customer_phone": "01234567890",
        "customer_address": {
          "street": "123 Main St",
          "city": "Cairo",
          "latitude": 30.0444,
          "longitude": 31.2357
        },
        "distance": null
      }
    ],
    "total": 10,
    "limit": 20,
    "offset": 0
  }
}
```

---

### 4.2 Accept Order
**Endpoint:** `POST /api/cyclex/collector/accept-order/<int:request_id>`  
**Auth:** Required (Collector)  
**Description:** Accept an order assignment (3-day deadline)

**Success Response:**
```json
{
  "success": true,
  "message": "Order accepted successfully",
  "data": {
    "request_id": 456,
    "status": "assigned",
    "deadline": "2025-10-20"
  }
}
```

---

### 4.3 Reject Order
**Endpoint:** `POST /api/cyclex/collector/reject-order/<int:request_id>`  
**Auth:** Required (Collector)  
**Description:** Reject an order assignment

**Success Response:**
```json
{
  "success": true,
  "message": "Order rejected successfully"
}
```

---

### 4.4 Scan QR Code
**Endpoint:** `POST /api/cyclex/collector/scan-qr`  
**Auth:** Required (Collector)  
**Description:** Scan and validate customer's QR code

**Request Body:**
```json
{
  "qr_code": "CX00456-XXXXX"
}
```

**Success Response:**
```json
{
  "success": true,
  "message": "QR code valid",
  "data": {
    "request_id": 456,
    "request_number": "CX00456",
    "customer_name": "John Doe",
    "product_name": "Plastic Bottles",
    "weight": 5.5,
    "calculated_price": 27.50,
    "currency_symbol": "E£",
    "status": "assigned"
  }
}
```

**Error Codes:**
- `INVALID_QR` - QR code not found
- `NOT_ASSIGNED` - Order not assigned to this collector

---

### 4.5 Complete Order
**Endpoint:** `POST /api/cyclex/collector/complete-order/<int:request_id>`  
**Auth:** Required (Collector)  
**Description:** Mark order as collected (triggers payment and commission)

**Success Response:**
```json
{
  "success": true,
  "message": "Order completed successfully",
  "data": {
    "request_id": 456,
    "status": "collected",
    "payment_amount": 27.50,
    "commission_earned": 1.38
  }
}
```

---

## 5. Wallet APIs

### 5.1 Get Balance
**Endpoint:** `GET /api/cyclex/wallet/balance`  
**Auth:** Required (Customer)  
**Description:** Get current wallet balance

**Success Response:**
```json
{
  "success": true,
  "data": {
    "balance": 1500.00,
    "total_earned": 2500.00,
    "total_withdrawn": 1000.00,
    "withdrawal_threshold": 1000.00,
    "can_withdraw": true,
    "currency": "EGP",
    "currency_symbol": "E£",
    "status": "active"
  }
}
```

---

### 5.2 Get Transactions
**Endpoint:** `GET /api/cyclex/wallet/transactions`  
**Auth:** Required (Customer)  
**Description:** Get wallet transaction history

**Query Parameters:**
- `transaction_type` (optional): 'credit' or 'debit'
- `limit` (optional): Number of results (default: 20)
- `offset` (optional): Pagination offset

**Success Response:**
```json
{
  "success": true,
  "data": {
    "transactions": [
      {
        "id": 789,
        "amount": 27.50,
        "type": "credit",
        "description": "Payment for request CX00456",
        "date": "2025-10-17 21:45:00",
        "request_number": "CX00456"
      }
    ],
    "total": 25,
    "limit": 20,
    "offset": 0
  }
}
```

---

### 5.3 Request Withdrawal
**Endpoint:** `POST /api/cyclex/wallet/withdraw`  
**Auth:** Required (Customer)  
**Description:** Request withdrawal from wallet (requires admin approval)

**Request Body:**
```json
{
  "amount": 1500.00
}
```

**Success Response:**
```json
{
  "success": true,
  "message": "Withdrawal request submitted successfully. Pending approval.",
  "data": {
    "transaction_id": 790,
    "amount": 1500.00,
    "remaining_balance": 0.00
  }
}
```

**Error Codes:**
- `INVALID_AMOUNT` - Amount <= 0
- `BELOW_THRESHOLD` - Below minimum threshold
- `INSUFFICIENT_BALANCE` - Not enough balance

---

## 6. Rating & Feedback APIs

### 6.1 Rate Order
**Endpoint:** `POST /api/cyclex/order/rate/<int:request_id>`  
**Auth:** Required (Customer)  
**Description:** Rate and provide feedback for completed order

**Request Body:**
```json
{
  "rating": "5",
  "comments": "Excellent service, very professional!"
}
```

**Success Response:**
```json
{
  "success": true,
  "message": "Rating submitted successfully",
  "data": {
    "request_id": 456,
    "rating": "5",
    "collector_name": "Collector Name"
  }
}
```

**Error Codes:**
- `INVALID_RATING` - Rating not between 1-5
- `INVALID_STATUS` - Order not collected yet
- `ALREADY_RATED` - Order already rated
- `ACCESS_DENIED` - Not your order

---

## Error Response Format

All error responses follow this format:

```json
{
  "success": false,
  "message": "Error description",
  "error_code": "ERROR_CODE"
}
```

### Common Error Codes

- `MISSING_PARAMS` - Required parameters missing
- `VALIDATION_ERROR` - Input validation failed
- `SERVER_ERROR` - Internal server error
- `NOT_FOUND` - Resource not found
- `ACCESS_DENIED` - Permission denied
- `INVALID_USER_TYPE` - Wrong user type for this action

---

## Status Codes

### Request/Order Status
- `draft` - Draft (not yet submitted)
- `pending` - Pending collector acceptance
- `assigned` - Assigned to collector
- `collected` - Collected and completed
- `cancelled` - Cancelled by customer

### Account Status
- `inactive` - Not verified yet
- `active` - Active and verified
- `suspended` - Temporarily suspended
- `banned` - Permanently banned

### Collector Approval Status
- `pending` - Pending admin approval
- `approved` - Approved and active
- `rejected` - Rejected by admin
- `suspended` - Temporarily suspended

---

## Testing

### Test with cURL

```bash
# Health check
curl -X POST http://localhost:10018/api/cyclex/health \
  -H "Content-Type: application/json" \
  -d '{}'

# Register
curl -X POST http://localhost:10018/api/cyclex/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "phone": "01234567890",
    "password": "test123",
    "confirm_password": "test123",
    "user_type": "customer"
  }'

# Login
curl -X POST http://localhost:10018/api/cyclex/login \
  -H "Content-Type: application/json" \
  -d '{
    "phone": "01234567890",
    "password": "test123"
  }'
```

---

## Notes

- All dates are in format: YYYY-MM-DD
- All datetimes are in format: YYYY-MM-DD HH:MM:SS
- Images are Base64 encoded
- Currency amounts are in float format
- Phone numbers can include country code or not
- Coordinates use decimal degrees format

---

**Last Updated:** October 17, 2025  
**Version:** 1.0.0

