# Odoo Endpoints Reference

**Generated:** November 13, 2025  
**Source:** CycleX Odoo 18 Module  
**Total Endpoints:** 24

---

## Endpoint Inventory

### 1. Health Check

**Endpoint:** `GET /api/cyclex/health`  
**Controller:** `CycleXController` (`main.py`)  
**Auth:** Public  
**Method:** GET  
**CSRF:** Disabled

**Response:**
```json
{
  "status": "ok",
  "message": "CycleX API is running",
  "version": "1.0.0"
}
```

---

### 2. Authentication Endpoints

#### 2.1 Login
**Endpoint:** `POST /api/cyclex/login`  
**Controller:** `CyclexAuthController` (`auth_controller.py`)  
**Auth:** Public  
**Method:** POST  
**CSRF:** Disabled

**Request Body:**
```json
{
  "phone": "01234567890",
  "password": "password123",
  "fcm_token": "optional_fcm_token"
}
```

**Response:**
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
- `MISSING_PARAMS`
- `INVALID_CREDENTIALS`
- `PHONE_NOT_VERIFIED`
- `ACCOUNT_SUSPENDED`

---

#### 2.2 Register
**Endpoint:** `POST /api/cyclex/register`  
**Controller:** `CyclexAuthController` (`auth_controller.py`)  
**Auth:** Public  
**Method:** POST  
**CSRF:** Disabled

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

**Response:**
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
- `MISSING_PARAMS`
- `PASSWORD_MISMATCH`
- `WEAK_PASSWORD`
- `PHONE_EXISTS`
- `INVALID_USER_TYPE`

---

#### 2.3 Verify Phone
**Endpoint:** `POST /api/cyclex/verify`  
**Controller:** `CyclexAuthController` (`auth_controller.py`)  
**Auth:** Public  
**Method:** POST  
**CSRF:** Disabled

**Request Body:**
```json
{
  "phone": "01234567890",
  "verification_code": "123456"
}
```

**Response:**
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
- `MISSING_PARAMS`
- `USER_NOT_FOUND`
- `ALREADY_VERIFIED`
- `INVALID_CODE`

---

#### 2.4 Resend Verification Code
**Endpoint:** `POST /api/cyclex/resend-code`  
**Controller:** `CyclexAuthController` (`auth_controller.py`)  
**Auth:** Public  
**Method:** POST  
**CSRF:** Disabled

**Request Body:**
```json
{
  "phone": "01234567890"
}
```

**Response:**
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

#### 2.5 Get Profile
**Endpoint:** `GET /api/cyclex/profile`  
**Controller:** `CyclexAuthController` (`auth_controller.py`)  
**Auth:** Required (user)  
**Method:** GET  
**CSRF:** Disabled

**Response:**
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

#### 2.6 Update Profile
**Endpoint:** `POST /api/cyclex/update-profile`  
**Controller:** `CyclexAuthController` (`auth_controller.py`)  
**Auth:** Required (user)  
**Method:** POST  
**CSRF:** Disabled

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

**Response:**
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

### 3. Categories & Products Endpoints

#### 3.1 Get Categories
**Endpoint:** `GET /api/cyclex/categories`  
**Controller:** `CyclexCategoryProductController` (`category_product_controller.py`)  
**Auth:** Public  
**Method:** GET  
**CSRF:** Disabled

**Query Parameters:**
- `parent_id` (optional): Filter by parent category
- `language` (optional): 'en' or 'ar'

**Response:**
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

#### 3.2 Get Products
**Endpoint:** `GET /api/cyclex/products`  
**Controller:** `CyclexCategoryProductController` (`category_product_controller.py`)  
**Auth:** Public  
**Method:** GET  
**CSRF:** Disabled

**Query Parameters:**
- `category_id` (optional): Filter by category
- `search` (optional): Search by name
- `language` (optional): 'en' or 'ar'

**Response:**
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

#### 3.3 Get Product Details
**Endpoint:** `GET /api/cyclex/product/<int:product_id>`  
**Controller:** `CyclexCategoryProductController` (`category_product_controller.py`)  
**Auth:** Public  
**Method:** GET  
**CSRF:** Disabled

**Path Parameters:**
- `product_id` (required): Product ID

**Response:**
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

### 4. Request/Order Endpoints

#### 4.1 Create Request
**Endpoint:** `POST /api/cyclex/request/create`  
**Controller:** `CyclexRequestController` (`request_controller.py`)  
**Auth:** Required (user, customer)  
**Method:** POST  
**CSRF:** Disabled

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

**Response:**
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
    "qr_code_image": "base64_encoded_image",
    "pickup_date": "2025-10-20",
    "product_name": "Plastic Bottles",
    "category_name": "Plastic"
  }
}
```

---

#### 4.2 List Requests
**Endpoint:** `GET /api/cyclex/request/list`  
**Controller:** `CyclexRequestController` (`request_controller.py`)  
**Auth:** Required (user)  
**Method:** GET  
**CSRF:** Disabled

**Query Parameters:**
- `status` (optional): Filter by status
- `limit` (optional): Number of results (default: 20)
- `offset` (optional): Pagination offset

**Response:**
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

#### 4.3 Get Request Details
**Endpoint:** `GET /api/cyclex/request/details/<int:request_id>`  
**Controller:** `CyclexRequestController` (`request_controller.py`)  
**Auth:** Required (user)  
**Method:** GET  
**CSRF:** Disabled

**Path Parameters:**
- `request_id` (required): Request ID

**Response:**
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
    "qr_code_image": "base64_encoded_image",
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

#### 4.4 Cancel Request
**Endpoint:** `POST /api/cyclex/request/cancel/<int:request_id>`  
**Controller:** `CyclexRequestController` (`request_controller.py`)  
**Auth:** Required (user, customer)  
**Method:** POST  
**CSRF:** Disabled

**Path Parameters:**
- `request_id` (required): Request ID

**Response:**
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

### 5. Collector Endpoints

#### 5.1 Collector Register
**Endpoint:** `POST /api/cyclex/collector/register`  
**Controller:** `CyclexCollectorController` (`collector_controller.py`)  
**Auth:** Public  
**Method:** POST  
**CSRF:** Disabled

**Note:** This endpoint calls the main register endpoint with `user_type='collector'`

---

#### 5.2 Get Available Orders
**Endpoint:** `GET /api/cyclex/collector/available-orders`  
**Controller:** `CyclexCollectorController` (`collector_controller.py`)  
**Auth:** Required (user, collector)  
**Method:** GET  
**CSRF:** Disabled

**Query Parameters:**
- `limit` (optional): Number of results (default: 20)
- `offset` (optional): Pagination offset

**Response:**
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

#### 5.3 Accept Order
**Endpoint:** `POST /api/cyclex/collector/accept-order/<int:request_id>`  
**Controller:** `CyclexCollectorController` (`collector_controller.py`)  
**Auth:** Required (user, collector)  
**Method:** POST  
**CSRF:** Disabled

**Path Parameters:**
- `request_id` (required): Request ID

**Response:**
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

#### 5.4 Reject Order
**Endpoint:** `POST /api/cyclex/collector/reject-order/<int:request_id>`  
**Controller:** `CyclexCollectorController` (`collector_controller.py`)  
**Auth:** Required (user, collector)  
**Method:** POST  
**CSRF:** Disabled

**Path Parameters:**
- `request_id` (required): Request ID

**Response:**
```json
{
  "success": true,
  "message": "Order rejected successfully"
}
```

---

#### 5.5 Scan QR Code
**Endpoint:** `POST /api/cyclex/collector/scan-qr`  
**Controller:** `CyclexCollectorController` (`collector_controller.py`)  
**Auth:** Required (user, collector)  
**Method:** POST  
**CSRF:** Disabled

**Request Body:**
```json
{
  "qr_code": "CX00456-XXXXX"
}
```

**Response:**
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
- `INVALID_QR`
- `NOT_ASSIGNED`

---

#### 5.6 Complete Order
**Endpoint:** `POST /api/cyclex/collector/complete-order/<int:request_id>`  
**Controller:** `CyclexCollectorController` (`collector_controller.py`)  
**Auth:** Required (user, collector)  
**Method:** POST  
**CSRF:** Disabled

**Path Parameters:**
- `request_id` (required): Request ID

**Response:**
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

### 6. Wallet Endpoints

#### 6.1 Get Balance
**Endpoint:** `GET /api/cyclex/wallet/balance`  
**Controller:** `CyclexWalletController` (`wallet_controller.py`)  
**Auth:** Required (user, customer)  
**Method:** GET  
**CSRF:** Disabled

**Response:**
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

#### 6.2 Get Transactions
**Endpoint:** `GET /api/cyclex/wallet/transactions`  
**Controller:** `CyclexWalletController` (`wallet_controller.py`)  
**Auth:** Required (user, customer)  
**Method:** GET  
**CSRF:** Disabled

**Query Parameters:**
- `transaction_type` (optional): 'credit' or 'debit'
- `limit` (optional): Number of results (default: 20)
- `offset` (optional): Pagination offset

**Response:**
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

#### 6.3 Request Withdrawal
**Endpoint:** `POST /api/cyclex/wallet/withdraw`  
**Controller:** `CyclexWalletController` (`wallet_controller.py`)  
**Auth:** Required (user, customer)  
**Method:** POST  
**CSRF:** Disabled

**Request Body:**
```json
{
  "amount": 1500.00
}
```

**Response:**
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
- `INVALID_AMOUNT`
- `BELOW_THRESHOLD`
- `INSUFFICIENT_BALANCE`

---

### 7. Rating Endpoints

#### 7.1 Rate Order
**Endpoint:** `POST /api/cyclex/order/rate/<int:request_id>`  
**Controller:** `CyclexRatingController` (`rating_controller.py`)  
**Auth:** Required (user, customer)  
**Method:** POST  
**CSRF:** Disabled

**Path Parameters:**
- `request_id` (required): Request ID

**Request Body:**
```json
{
  "rating": "5",
  "comments": "Excellent service, very professional!"
}
```

**Response:**
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
- `INVALID_RATING`
- `INVALID_STATUS`
- `ALREADY_RATED`
- `ACCESS_DENIED`

---

## Summary Statistics

**Total Endpoints:** 24

**By Category:**
- Health: 1
- Authentication: 6
- Categories & Products: 3
- Requests/Orders: 4
- Collector: 6
- Wallet: 3
- Rating: 1

**By Auth Level:**
- Public: 7
- User Required: 17

**By HTTP Method:**
- GET: 10
- POST: 14

---

**Last Updated:** November 13, 2025

