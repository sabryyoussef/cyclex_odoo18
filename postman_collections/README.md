# CycleX API - Postman Collections 📮

**Complete API Testing Suite for CycleX Recycling Mobile Application**

---

## 📦 What's Included

### Files in this Directory:

1. **`CycleX_API_Collection.json`** - Complete API collection (22 endpoints)
2. **`CycleX_Environment.json`** - Environment variables template
3. **`README.md`** - This file (setup instructions)

---

## 🚀 Quick Start (5 Minutes)

### Step 1: Import Collection into Postman

1. **Open Postman** (Download from https://www.postman.com/downloads/ if needed)

2. **Import Collection:**
   - Click **"Import"** button (top left)
   - Drag and drop `CycleX_API_Collection.json`
   - OR click **"Upload Files"** and select the file
   - Click **"Import"**

3. **Import Environment:**
   - Click **"Import"** button again
   - Drag and drop `CycleX_Environment.json`
   - OR click **"Upload Files"** and select the file
   - Click **"Import"**

4. **Select Environment:**
   - Top right corner: Select **"CycleX - Development"** from dropdown
   - Click the 👁️ icon to view/edit environment variables

### Step 2: Configure Base URL

Update the `base_url` environment variable:

```
Default: http://localhost:10018
Your server: http://YOUR_IP:10018  (e.g., http://192.168.1.100:10018)
```

**To update:**
1. Click 👁️ icon (top right)
2. Find `base_url`
3. Change value to your Odoo server address
4. Click **"Save"**

### Step 3: Test Your First Endpoint

1. **Expand:** `1. Authentication` folder
2. **Click:** `1.3 Login`
3. **Update** phone/password in the JSON body if needed
4. **Click:** `Send`
5. **Verify:** You get a `200 OK` response with user data

**You're ready to go! 🎉**

---

## 📋 Collection Structure

The collection contains **22 endpoints** organized in **7 categories**:

### 1. Authentication (4 endpoints)
```
1.1 Register User       - POST /api/cyclex/register
1.2 Verify Phone        - POST /api/cyclex/verify
1.3 Login               - POST /api/cyclex/login
1.4 Resend Code         - POST /api/cyclex/resend-code
```

### 2. Categories & Products (2 endpoints)
```
2.1 Get Categories      - POST /api/cyclex/categories
2.2 Get Products        - POST /api/cyclex/products
```

### 3. Recycling Requests (4 endpoints)
```
3.1 Create Request      - POST /api/cyclex/request/create
3.2 My Requests         - POST /api/cyclex/request/my-requests
3.3 Request Details     - POST /api/cyclex/request/details
3.4 Rate Request        - POST /api/cyclex/request/rate
```

### 4. Collector Actions (5 endpoints)
```
4.1 Available Orders    - POST /api/cyclex/collector/available-orders
4.2 Accept Order        - POST /api/cyclex/collector/accept-order
4.3 Reject Order        - POST /api/cyclex/collector/reject-order
4.4 Scan QR Code        - POST /api/cyclex/collector/scan-qr
4.5 My Completed Orders - POST /api/cyclex/collector/my-orders
```

### 5. Wallet (4 endpoints)
```
5.1 Get Balance         - POST /api/cyclex/wallet/balance
5.2 Get Transactions    - POST /api/cyclex/wallet/transactions
5.3 Request Credit      - POST /api/cyclex/wallet/credit (Admin only)
5.4 Request Withdrawal  - POST /api/cyclex/wallet/debit
```

### 6. Profile (3 endpoints)
```
6.1 Get Profile         - POST /api/cyclex/profile
6.2 Update Profile      - POST /api/cyclex/profile/update
6.3 Update FCM Token    - POST /api/cyclex/profile/update-fcm-token
```

### 7. Commission (1 endpoint)
```
7.1 My Commission       - POST /api/cyclex/collector/my-commission
```

**Total: 22 endpoints** ✅

---

## 🔐 Authentication & Sessions

### How Authentication Works:

CycleX API uses **session-based authentication** with cookies:

1. **Login/Register:** Call `/api/cyclex/login` or `/api/cyclex/register`
2. **Session Cookie:** Postman automatically stores the `auth_token` cookie
3. **Authenticated Requests:** All subsequent requests use this cookie
4. **No Manual Headers:** No need to manually add Authorization headers

### Testing Authentication Flow:

#### As Customer:
```
1. Register User (1.1) → Creates account
2. Verify Phone (1.2) → Activates account (use code "123456" for testing)
3. Login (1.3)        → Authenticates and stores session
4. Get Profile (6.1)  → Verifies you're logged in
```

#### As Collector:
```
1. Register with user_type: "collector"
2. Admin must verify collector in Odoo backend
3. Login
4. Test collector endpoints (4.x)
```

---

## 🧪 Testing Workflows

### Complete Customer Journey:

```
1. Register User (1.1)
   ↓
2. Verify Phone (1.2) - Use code: 123456
   ↓
3. Login (1.3)
   ↓
4. Get Categories (2.1)
   ↓
5. Get Products (2.2) - Use category_id from step 4
   ↓
6. Create Request (3.1) - Use product_id from step 5
   ↓
7. My Requests (3.2) - See your request
   ↓
8. Request Details (3.3) - Get QR code
   ↓
9. [Collector scans QR and completes]
   ↓
10. Get Balance (5.1) - Check credited amount
    ↓
11. Rate Request (3.4) - Rate the service
```

### Complete Collector Journey:

```
1. Register as Collector
   ↓
2. [Admin verifies in Odoo]
   ↓
3. Login
   ↓
4. Available Orders (4.1)
   ↓
5. Accept Order (4.2)
   ↓
6. [Go to customer location]
   ↓
7. Scan QR Code (4.4) - Completes order
   ↓
8. My Completed Orders (4.5)
   ↓
9. My Commission (7.1) - Check earnings
```

---

## 🔧 Environment Variables

### Pre-configured Variables:

| Variable | Default Value | Description |
|----------|--------------|-------------|
| `base_url` | http://localhost:10018 | Odoo server URL |
| `customer_phone` | +201234567890 | Test customer phone |
| `customer_password` | TestPass123 | Test customer password |
| `collector_phone` | +201111111111 | Test collector phone |
| `collector_password` | TestPass123 | Test collector password |
| `category_id` | 1 | Sample category ID |
| `product_id` | 1 | Sample product ID |
| `auth_token` | (auto) | Session token (auto-stored) |
| `user_id` | (auto) | Current user ID |
| `request_id` | (auto) | Last created request ID |

### Using Variables in Requests:

Variables are used with `{{variable_name}}` syntax:
```json
{
    "phone": "{{customer_phone}}",
    "password": "{{customer_password}}"
}
```

### Updating Variables:

1. **View Variables:** Click 👁️ icon (top right)
2. **Edit Values:** Click on the environment name
3. **Save:** Click "Save" after changes

---

## 📝 Common Test Scenarios

### Scenario 1: Create Test Customer

**Endpoint:** 1.1 Register User

**Body:**
```json
{
    "jsonrpc": "2.0",
    "method": "call",
    "params": {
        "name": "Ahmed Hassan",
        "phone": "+201234567890",
        "password": "TestPass123",
        "email": "ahmed@example.com",
        "user_type": "customer",
        "language": "ar"
    },
    "id": 1
}
```

**Expected Response:**
```json
{
    "jsonrpc": "2.0",
    "id": 1,
    "result": {
        "success": true,
        "message": "Registration successful",
        "data": {
            "user_id": 5,
            "phone": "+201234567890",
            "verification_required": true
        }
    }
}
```

---

### Scenario 2: Create Recycling Request

**Endpoint:** 3.1 Create Request

**Prerequisites:**
- Must be logged in as customer
- Have valid `product_id`

**Body:**
```json
{
    "jsonrpc": "2.0",
    "method": "call",
    "params": {
        "product_id": 1,
        "quantity": 15.5,
        "unit": "kg",
        "pickup_date": "2025-10-25",
        "pickup_time": "morning",
        "location_latitude": 30.0444,
        "location_longitude": 31.2357,
        "address": "123 شارع التحرير، القاهرة",
        "notes": "Please call before arriving"
    },
    "id": 7
}
```

**Expected Response:**
```json
{
    "jsonrpc": "2.0",
    "id": 7,
    "result": {
        "success": true,
        "message": "Request created successfully",
        "data": {
            "request_id": 10,
            "request_number": "REQ-00010",
            "status": "pending",
            "calculated_price": 155.00,
            "qr_code": "CYCLEX-REQ-00010-abc123...",
            "qr_code_image": "base64_png_image..."
        }
    }
}
```

---

### Scenario 3: Collector Accepts and Completes Order

**Step 1: Login as Collector**
- Endpoint: 1.3 Login
- Use collector credentials

**Step 2: Get Available Orders**
- Endpoint: 4.1 Available Orders
- See pending orders in your area

**Step 3: Accept Order**
- Endpoint: 4.2 Accept Order
- Body: `{"request_id": 10}`

**Step 4: Scan QR Code**
- Endpoint: 4.4 Scan QR Code
- Body: `{"qr_code": "CYCLEX-REQ-00010-abc123..."}`
- This completes the order

**Step 5: Check Commission**
- Endpoint: 7.1 My Commission
- See earnings from completed order

---

## ⚠️ Troubleshooting

### Problem: Connection Refused

**Error:**
```
Error: connect ECONNREFUSED 127.0.0.1:10018
```

**Solution:**
1. Check if Odoo is running
2. Verify the port (default: 10018)
3. Update `base_url` in environment variables
4. If using remote server, use server IP: `http://192.168.1.100:10018`

---

### Problem: Unauthorized / Not Logged In

**Error:**
```json
{
    "error": {
        "code": 401,
        "message": "Unauthorized"
    }
}
```

**Solution:**
1. Run `1.3 Login` first
2. Check if session cookie is enabled in Postman:
   - Settings → General → "Automatically follow redirects"
   - Settings → General → "Enable cookie jar"
3. Make sure you're using the same environment

---

### Problem: Invalid Phone Format

**Error:**
```json
{
    "error": {
        "code": 1001,
        "message": "Invalid Egyptian phone number format"
    }
}
```

**Solution:**
- Use format: `+20XXXXXXXXXX` (12 digits)
- Example: `+201234567890`
- Must start with +20 (Egypt country code)
- Next digit must be 1 (mobile)
- Third digit: 0, 1, 2, or 5

---

### Problem: Image Too Large

**Error:**
```json
{
    "error": {
        "code": 1004,
        "message": "Image size (6.5 MB) exceeds maximum allowed size of 5 MB"
    }
}
```

**Solution:**
- Compress image before converting to base64
- Maximum allowed: 5 MB
- Recommended: Use 1-2 MB images

---

### Problem: QR Code Invalid

**Error:**
```json
{
    "error": {
        "code": 2003,
        "message": "Invalid QR code"
    }
}
```

**Solution:**
- Copy the exact `qr_code` value from request details
- Format: `CYCLEX-REQ-XXXXX-uuid`
- Don't modify or truncate the UUID

---

## 📊 Response Codes

### Success Codes:
- `200` - Success
- `201` - Created

### Error Codes:

| Code | Category | Description |
|------|----------|-------------|
| `1001-1099` | Validation | Invalid input data |
| `2001-2099` | Business Logic | Business rule violations |
| `3001-3099` | Database | Database errors |
| `4001-4099` | External | SMS/Firebase errors |
| `401` | Auth | Unauthorized |
| `403` | Auth | Forbidden |
| `404` | Resource | Not found |
| `500` | Server | Internal error |

---

## 🔄 JSON-RPC 2.0 Format

All requests use **JSON-RPC 2.0** protocol:

### Request Structure:
```json
{
    "jsonrpc": "2.0",
    "method": "call",
    "params": {
        "param1": "value1",
        "param2": "value2"
    },
    "id": 1
}
```

### Success Response:
```json
{
    "jsonrpc": "2.0",
    "id": 1,
    "result": {
        "success": true,
        "message": "Operation successful",
        "data": { ... }
    }
}
```

### Error Response:
```json
{
    "jsonrpc": "2.0",
    "id": 1,
    "result": {
        "success": false,
        "error": {
            "code": 1001,
            "message": "Error description"
        }
    }
}
```

---

## 🎯 Testing Tips

### 1. Use Collection Runner

Run all endpoints automatically:
1. Click on "CycleX API" collection
2. Click "Run" button
3. Select endpoints to test
4. Click "Run CycleX API"

### 2. Save Responses as Examples

After successful test:
1. Click "Save Response"
2. Click "Save as example"
3. Future runs show expected vs actual

### 3. Use Pre-request Scripts

Auto-update variables:
```javascript
// In Pre-request Script tab:
pm.environment.set("pickup_date", "2025-10-25");
```

### 4. Use Tests Tab

Validate responses:
```javascript
// In Tests tab:
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Response has success true", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.result.success).to.eql(true);
});
```

---

## 📚 Additional Resources

### Documentation Files:
- **`API_DOCUMENTATION.md`** - Complete API reference
- **`MOBILE_INTEGRATION_GUIDE.md`** - Mobile app integration guide
- **`planning/CycleX_Development_Plan.md`** - Full development plan

### Odoo Backend:
- **URL:** http://localhost:10018
- **Database:** cyclex_db
- **Default Admin:**
  - Email: admin@cyclex.com
  - Password: admin

### Test Accounts (Create these in Odoo):
```
Customer 1:
  Phone: +201234567890
  Password: TestPass123

Collector 1:
  Phone: +201111111111
  Password: TestPass123
  (Must be verified by admin)
```

---

## 🚀 Quick Testing Commands

### Using cURL (Alternative to Postman):

```bash
# Login
curl -X POST http://localhost:10018/api/cyclex/login \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "call",
    "params": {
      "phone": "+201234567890",
      "password": "TestPass123"
    },
    "id": 1
  }'

# Get Categories
curl -X POST http://localhost:10018/api/cyclex/categories \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "call",
    "params": {},
    "id": 1
  }'
```

---

## 📞 Support

### Issues with API:
1. Check Odoo logs: `/tmp/odoo_phase5_update.log`
2. Verify module is installed: Odoo → Apps → CycleX
3. Check endpoint URLs match documentation

### Issues with Postman:
1. Update to latest version
2. Clear cookies: Settings → Clear all cookies
3. Re-import collection

### Questions:
- Refer to `API_DOCUMENTATION.md` for detailed endpoint specs
- Check `MOBILE_INTEGRATION_GUIDE.md` for integration examples

---

## ✅ Checklist Before Testing

- [ ] Odoo server is running on port 10018
- [ ] CycleX module is installed and upgraded
- [ ] Collection imported into Postman
- [ ] Environment imported and selected
- [ ] `base_url` updated to your server address
- [ ] Test accounts created in Odoo (optional)
- [ ] Categories and products exist in database

---

## 🎉 You're All Set!

**Happy Testing! 🚀**

Start with the authentication endpoints and work your way through the collection.

If you encounter any issues, refer to the Troubleshooting section or check the logs.

---

**Last Updated:** October 17, 2025  
**Version:** 1.0  
**Endpoints:** 22  
**Format:** JSON-RPC 2.0

