# CycleX Backend Workflows Documentation 🔄

**Complete workflow documentation for all business processes**

**Version:** 1.0  
**Date:** October 2025

---

## 🎯 Overview

This document details all business workflows in the CycleX system, including:
1. User Registration & Verification
2. Request Creation & Management
3. Order Assignment & Completion
4. Wallet & Financial Transactions
5. Commission Calculation
6. Withdrawal Approval
7. Automated Processes (Cron Jobs)

---

## 1️⃣ User Registration & Verification Workflow

###  Customer Registration

**Trigger:** Customer clicks "Register" in mobile app

**Flow:**

```
┌─────────────────────────────────────────────────────────┐
│ Step 1: User Submits Registration                       │
└─────────────────────────────────────────────────────────┘
Mobile App → POST /api/cyclex/register
{
    "name": "Ahmed Hassan",
    "phone": "+201234567890",
    "password": "TestPass123",
    "user_type": "customer"
}
         ↓
┌─────────────────────────────────────────────────────────┐
│ Step 2: Backend Validates Data                          │
└─────────────────────────────────────────────────────────┘
- Check phone format (Egyptian) ✅
- Check phone not duplicate ✅
- Check password strength ✅
- Validate all required fields ✅
         ↓
┌─────────────────────────────────────────────────────────┐
│ Step 3: Create User Record                              │
└─────────────────────────────────────────────────────────┘
res.partner created:
- name: "Ahmed Hassan"
- phone: "+201234567890"
- is_cyclex_user: True
- cyclex_user_type: "customer"
- phone_verified: False
         ↓
┌─────────────────────────────────────────────────────────┐
│ Step 4: Generate Verification Code                      │
└─────────────────────────────────────────────────────────┘
- Generate 6-digit code: "123456"
- Set expiry: Now + 10 minutes
- Save to partner.verification_code
         ↓
┌─────────────────────────────────────────────────────────┐
│ Step 5: Send SMS (Phase 7)                              │
└─────────────────────────────────────────────────────────┘
SMS Misr API → Send verification code
Message: "رمز التحقق الخاص بك: 123456"
(Currently placeholder - implemented in Phase 7)
         ↓
┌─────────────────────────────────────────────────────────┐
│ Step 6: Create Wallet                                   │
└─────────────────────────────────────────────────────────┘
cyclex.wallet auto-created:
- partner_id: Ahmed
- current_balance: 0.00
- currency: EGP
         ↓
┌─────────────────────────────────────────────────────────┐
│ Step 7: Return Success                                  │
└─────────────────────────────────────────────────────────┘
{
    "success": true,
    "data": {
        "user_id": 5,
        "verification_required": true
    }
}
         ↓
┌─────────────────────────────────────────────────────────┐
│ Step 8: User Verifies Phone                             │
└─────────────────────────────────────────────────────────┘
Mobile App → POST /api/cyclex/verify
{
    "phone": "+201234567890",
    "code": "123456"
}
         ↓
Backend validates code:
- Matches verification_code ✅
- Not expired (< 10 min) ✅
- Set phone_verified = True ✅
         ↓
User can now login! ✅
```

**Duration:** ~2 minutes  
**Status:** User active and verified

---

### Collector Registration

**Same as customer PLUS:**

```
Additional Step (After Verification):
         ↓
┌─────────────────────────────────────────────────────────┐
│ Admin Verification Required                             │
└─────────────────────────────────────────────────────────┘
collector_verified: False
Status: Pending admin approval
         ↓
Admin reviews application in Odoo backend
         ↓
Admin sets:
- collector_verified = True ✅
- commission_rate = 15%
- working_area_ids = [Nasr City, Heliopolis]
         ↓
Collector notified (Phase 7)
         ↓
Collector can now accept orders! ✅
```

**Duration:** ~1-3 business days (admin review)

---

## 2️⃣ Request Creation Workflow

### Customer Creates Recycling Request

**Trigger:** Customer clicks "Create Request" in app

**Flow:**

```
┌─────────────────────────────────────────────────────────┐
│ Step 1: Customer Selects Product                        │
└─────────────────────────────────────────────────────────┘
App shows categories → Customer selects "Plastic"
App shows products → Customer selects "Plastic Bottles"
Price shown: 3.50 EGP/kg
         ↓
┌─────────────────────────────────────────────────────────┐
│ Step 2: Customer Fills Details                          │
└─────────────────────────────────────────────────────────┘
- Quantity: 15.5 kg
- Pickup Date: 2025-10-25
- Pickup Time: Morning
- Address: Full address
- GPS Location: (captured automatically)
- Photo: Take/upload photo (optional)
- Notes: "Please call before arriving"
         ↓
┌─────────────────────────────────────────────────────────┐
│ Step 3: App Submits Request                             │
└─────────────────────────────────────────────────────────┘
POST /api/cyclex/request/create
{
    "product_id": 1,
    "quantity": 15.5,
    "unit": "kg",
    "pickup_date": "2025-10-25",
    "pickup_time": "morning",
    "location_latitude": 30.0444,
    "location_longitude": 31.2357,
    "address": "15 El Nasr Street, Nasr City",
    "notes": "Please call before arriving",
    "image": "base64_encoded_image"
}
         ↓
┌─────────────────────────────────────────────────────────┐
│ Step 4: Backend Processes Request                       │
└─────────────────────────────────────────────────────────┘
Validations:
- Image size ≤ 5MB ✅
- Pickup date ≥ today ✅
- Product exists ✅
- Quantity > 0 ✅
         ↓
Calculate Price:
- 15.5 kg × 3.50 EGP/kg = 54.25 EGP
         ↓
Generate QR Code:
- Format: "CYCLEX-REQ-00001-abc123-def456-..."
- Generate QR image (PNG)
         ↓
Create Request Record:
- name: "REQ-00001" (auto-sequence)
- customer_id: Ahmed
- product_id: Plastic Bottles
- quantity: 15.5
- calculated_price: 54.25
- status: "pending"
- qr_code: Generated
- qr_code_image: PNG base64
         ↓
┌─────────────────────────────────────────────────────────┐
│ Step 5: Return Response                                 │
└─────────────────────────────────────────────────────────┘
{
    "success": true,
    "data": {
        "request_id": 1,
        "request_number": "REQ-00001",
        "calculated_price": 54.25,
        "qr_code": "CYCLEX-REQ-00001-...",
        "qr_code_image": "base64_png_..."
    }
}
         ↓
Customer app shows:
- "Request created successfully"
- Shows QR code to display when collector arrives
- Shows expected payment: 54.25 EGP
```

**Duration:** ~2 seconds  
**Status:** Request pending, waiting for collector

---

## 3️⃣ Order Assignment Workflow

### Collector Accepts Order

**Trigger:** Collector clicks "Accept" on available order

**Flow:**

```
┌─────────────────────────────────────────────────────────┐
│ Step 1: Collector Views Available Orders                │
└─────────────────────────────────────────────────────────┘
POST /api/cyclex/collector/available-orders
         ↓
Backend filters orders:
- status = "pending" ✅
- location in collector's working_area_ids ✅
         ↓
Returns orders in: Nasr City, Heliopolis (Mahmoud's areas)
         ↓
┌─────────────────────────────────────────────────────────┐
│ Step 2: Collector Selects Order                         │
└─────────────────────────────────────────────────────────┘
Mahmoud sees:
- REQ-00001: 15.5kg Plastic Bottles, 54.25 EGP
- Location: Nasr City (his area ✅)
- Pickup: Tomorrow morning
         ↓
Mahmoud clicks "Accept"
         ↓
┌─────────────────────────────────────────────────────────┐
│ Step 3: App Submits Accept Request                      │
└─────────────────────────────────────────────────────────┘
POST /api/cyclex/collector/accept-order
{
    "request_id": 1
}
         ↓
┌─────────────────────────────────────────────────────────┐
│ Step 4: Backend Validates                               │
└─────────────────────────────────────────────────────────┘
Checks:
- User is verified collector ✅
- Order is still pending ✅
- Collector has < 5 pending orders ✅
- Order in collector's working areas ✅
         ↓
┌─────────────────────────────────────────────────────────┐
│ Step 5: Update Request                                  │
└─────────────────────────────────────────────────────────┘
cyclex.request updated:
- status: "pending" → "assigned"
- collector_id: Mahmoud
- write_date: Now (starts 3-day countdown)
         ↓
┌─────────────────────────────────────────────────────────┐
│ Step 6: Notifications Sent (Phase 7)                    │
└─────────────────────────────────────────────────────────┘
Firebase FCM:
- To Customer: "Collector Mahmoud accepted your order"
- To Collector: "Order assigned to you"
         ↓
┌─────────────────────────────────────────────────────────┐
│ Step 7: Return Success                                  │
└─────────────────────────────────────────────────────────┘
{
    "success": true,
    "message": "Order accepted successfully"
}
```

**Duration:** ~1 second  
**Status:** Order assigned, collector on the way

---

## 4️⃣ Order Completion Workflow

### Collector Scans QR Code

**Trigger:** Collector arrives at customer location, customer shows QR code

**Flow:**

```
┌─────────────────────────────────────────────────────────┐
│ Step 1: Collector Opens QR Scanner                      │
└─────────────────────────────────────────────────────────┘
Mobile app activates camera
Customer displays QR code on their phone
         ↓
┌─────────────────────────────────────────────────────────┐
│ Step 2: Scan QR Code                                    │
└─────────────────────────────────────────────────────────┘
Camera scans QR code
Extracts string: "CYCLEX-REQ-00001-abc123-def456-..."
         ↓
┌─────────────────────────────────────────────────────────┐
│ Step 3: Send to Backend                                 │
└─────────────────────────────────────────────────────────┘
POST /api/cyclex/collector/scan-qr
{
    "qr_code": "CYCLEX-REQ-00001-abc123-def456-..."
}
         ↓
┌─────────────────────────────────────────────────────────┐
│ Step 4: Backend Validates QR Code                       │
└─────────────────────────────────────────────────────────┘
Checks:
- QR code exists in database ✅
- Request is assigned to THIS collector ✅
- Request not already collected ✅
- Request not cancelled ✅
         ↓
Finds request: REQ-00001
Customer: Ahmed Hassan
Price: 54.25 EGP
         ↓
┌─────────────────────────────────────────────────────────┐
│ Step 5: Update Request Status                           │
└─────────────────────────────────────────────────────────┘
cyclex.request updated:
- status: "assigned" → "collected"
- collection_date: Now
         ↓
┌─────────────────────────────────────────────────────────┐
│ Step 6: Credit Customer Wallet (AUTOMATIC)              │
└─────────────────────────────────────────────────────────┘
cyclex.wallet.transaction created:
- wallet_id: Ahmed's wallet
- amount: 54.25 EGP
- transaction_type: "credit"
- description: "Payment for recycling request REQ-00001"
- request_id: 1
         ↓
Ahmed's wallet.current_balance:
- Before: 0.00 EGP
- After: 54.25 EGP ✅
         ↓
┌─────────────────────────────────────────────────────────┐
│ Step 7: Create Collector Commission (AUTOMATIC)         │
└─────────────────────────────────────────────────────────┘
cyclex.commission created:
- request_id: REQ-00001
- collector_id: Mahmoud
- amount: 54.25 EGP
- commission_rate: 15%
- commission_amount: 8.14 EGP (54.25 × 0.15)
- status: "earned"
         ↓
┌─────────────────────────────────────────────────────────┐
│ Step 8: Send Notifications (Phase 7)                    │
└─────────────────────────────────────────────────────────┘
Firebase FCM:
- To Customer: "Order completed! 54.25 EGP added to wallet"
- To Collector: "Order completed! You earned 8.14 EGP"
         ↓
┌─────────────────────────────────────────────────────────┐
│ Step 9: Return Success                                  │
└─────────────────────────────────────────────────────────┘
{
    "success": true,
    "data": {
        "request_number": "REQ-00001",
        "customer_payment": 54.25,
        "your_commission": 8.14,
        "status": "collected"
    }
}
         ↓
Both apps updated:
- Customer can now rate the service
- Collector sees completed order in history
```

**Duration:** ~2-3 seconds  
**Status:** Order complete, both parties paid

---

## 5️⃣ Withdrawal Request Workflow

### Customer Requests Wallet Withdrawal

**Trigger:** Customer clicks "Withdraw" in app

**Flow:**

```
┌─────────────────────────────────────────────────────────┐
│ Step 1: Customer Requests Withdrawal                    │
└─────────────────────────────────────────────────────────┘
POST /api/cyclex/wallet/debit
{
    "amount": 50.00,
    "description": "Withdrawal request"
}
         ↓
┌─────────────────────────────────────────────────────────┐
│ Step 2: Backend Validates                               │
└─────────────────────────────────────────────────────────┘
Checks:
- Amount ≥ 10 EGP (minimum) ✅
- Amount ≤ wallet balance ✅
- Wallet exists ✅
         ↓
Current balance: 100.00 EGP
Requested: 50.00 EGP ✅
         ↓
┌─────────────────────────────────────────────────────────┐
│ Step 3: Create Withdrawal Transaction                   │
└─────────────────────────────────────────────────────────┘
cyclex.wallet.transaction created:
- wallet_id: Ahmed's wallet
- amount: 50.00 EGP
- transaction_type: "debit"
- description: "Withdrawal request"
- withdrawal_status: "pending"
         ↓
┌─────────────────────────────────────────────────────────┐
│ Step 4: Deduct from Balance (Immediately)               │
└─────────────────────────────────────────────────────────┘
Wallet balance updated:
- Before: 100.00 EGP
- After: 50.00 EGP (deducted immediately)
         ↓
┌─────────────────────────────────────────────────────────┐
│ Step 5: Notify Admin (Cron Job - Daily)                 │
└─────────────────────────────────────────────────────────┘
Daily cron job runs:
- Finds all pending withdrawals
- Logs count and total amount
- Admin sees in pending withdrawals menu
         ↓
┌─────────────────────────────────────────────────────────┐
│ Step 6: Admin Reviews (Manual)                          │
└─────────────────────────────────────────────────────────┘
Admin goes to: CycleX → Financial → Pending Withdrawals
Reviews:
- Customer: Ahmed Hassan
- Amount: 50.00 EGP
- Current Balance: 50.00 EGP (after deduction)
- Request Date: 2025-10-17 14:30
         ↓
Admin decides:
     ┌──────┴──────┐
     ▼             ▼
  APPROVE      REJECT
     │             │
     ▼             ▼
┌──────────┐  ┌──────────┐
│ Approved │  │ Rejected │
└──────────┘  └──────────┘
     │             │
     ▼             ▼
Status:        Status:
approved       rejected
     │             │
     ▼             ▼
Process        Balance
payment        restored
externally     to 100 EGP
     │             │
     ▼             ▼
Mark as        Customer
completed      notified
```

**Duration:** 1-3 business days  
**Status:** Withdrawal processed or rejected

---

## 6️⃣ Commission Calculation Workflow

### Automatic Commission on Order Completion

**Trigger:** Request status changes to "collected"

**Flow:**

```
Order Status: assigned → collected
         ↓
┌─────────────────────────────────────────────────────────┐
│ Trigger: Automatic Process                              │
└─────────────────────────────────────────────────────────┘
Python code in cyclex.request model:
@api.model
def create(self, vals):
    # After request created and collected
    if vals.get('status') == 'collected':
        self._create_commission()
         ↓
┌─────────────────────────────────────────────────────────┐
│ Step 1: Get Request Data                                │
└─────────────────────────────────────────────────────────┘
Request: REQ-00001
Price: 54.25 EGP
Collector: Mahmoud (commission_rate: 15%)
         ↓
┌─────────────────────────────────────────────────────────┐
│ Step 2: Calculate Commission                            │
└─────────────────────────────────────────────────────────┘
Formula: commission = price × rate / 100
Calculation: 54.25 × 15 / 100 = 8.14 EGP
         ↓
┌─────────────────────────────────────────────────────────┐
│ Step 3: Create Commission Record                        │
└─────────────────────────────────────────────────────────┘
cyclex.commission created:
- request_id: 1
- collector_id: Mahmoud
- amount: 54.25 EGP (full request price)
- commission_rate: 15%
- commission_amount: 8.14 EGP (computed)
- status: "earned"
- currency: EGP
         ↓
┌─────────────────────────────────────────────────────────┐
│ Step 4: Collector Can View                              │
└─────────────────────────────────────────────────────────┘
Mahmoud's app shows:
- My Commissions
- REQ-00001: +8.14 EGP
- Total Earned Today: 8.14 EGP
```

**Duration:** Instant (on order completion)  
**Status:** Commission recorded, visible to collector

---

## 7️⃣ Auto-Revert Workflow (Cron Job)

### Automatic Order Reversion for Overdue Assignments

**Trigger:** Scheduled action runs every 6 hours

**Business Rule:** Orders assigned for 3+ days auto-revert to pending

**Flow:**

```
┌─────────────────────────────────────────────────────────┐
│ Scheduled Action Runs (Every 6 Hours)                   │
└─────────────────────────────────────────────────────────┘
Cron: CycleX: Auto-Revert Overdue Orders
         ↓
┌─────────────────────────────────────────────────────────┐
│ Step 1: Find Overdue Orders                             │
└─────────────────────────────────────────────────────────┘
SQL Query:
SELECT * FROM cyclex_request
WHERE status = 'assigned'
  AND write_date < NOW() - INTERVAL '3 days'
         ↓
Found: REQ-00005
- Assigned to: Collector X
- Assigned on: 2025-10-13 (4 days ago)
- Still not collected
         ↓
┌─────────────────────────────────────────────────────────┐
│ Step 2: Revert Each Order                               │
└─────────────────────────────────────────────────────────┘
For each overdue order:
- status: "assigned" → "pending"
- collector_id: Removed (set to False)
- write_date: Updated to now
         ↓
┌─────────────────────────────────────────────────────────┐
│ Step 3: Log Activity                                    │
└─────────────────────────────────────────────────────────┘
Message posted in request chatter:
"Order auto-reverted to pending due to 3-day deadline exceeded.
Previous collector: Collector X"
         ↓
┌─────────────────────────────────────────────────────────┐
│ Step 4: Notify Parties (Phase 7)                        │
└─────────────────────────────────────────────────────────┘
Firebase FCM:
- To Customer: "Order returned to available - new collector will be assigned"
- To Collector: "Order removed due to 3-day deadline"
         ↓
┌─────────────────────────────────────────────────────────┐
│ Step 5: Log Results                                     │
└─────────────────────────────────────────────────────────┘
System log:
"Auto-reverted 3 overdue orders"
         ↓
Order now available for other collectors
```

**Runs:** Every 6 hours  
**Purpose:** Ensure orders don't get stuck with inactive collectors

---

## 8️⃣ Withdrawal Approval Workflow

### Admin Approves or Rejects Withdrawal

**Trigger:** Admin reviews pending withdrawals

**Flow:**

```
┌─────────────────────────────────────────────────────────┐
│ Step 1: Admin Sees Notification                         │
└─────────────────────────────────────────────────────────┘
Daily cron job logs:
"Found 5 pending withdrawal requests totaling 2,300 EGP"
         ↓
Admin goes to: Pending Withdrawals menu
         ↓
┌─────────────────────────────────────────────────────────┐
│ Step 2: Admin Reviews Request                           │
└─────────────────────────────────────────────────────────┘
Transaction details:
- Customer: Ahmed Hassan
- Amount: 50.00 EGP
- Request Date: 2025-10-17 14:30
- Current Balance: 50.00 EGP (after deduction)
- Description: "Withdrawal request"
         ↓
Admin checks:
- Customer is legitimate ✅
- Amount is reasonable ✅
- No fraud indicators ✅
         ↓
Admin decides: APPROVE
         ↓
┌─────────────────────────────────────────────────────────┐
│ Step 3: Approve Withdrawal                              │
└─────────────────────────────────────────────────────────┘
Admin clicks "Approve" button
         ↓
Backend updates transaction:
- withdrawal_status: "pending" → "approved"
- approved_by: Admin user
- approval_date: Now
         ↓
┌─────────────────────────────────────────────────────────┐
│ Step 4: Process Payment (External)                      │
└─────────────────────────────────────────────────────────┘
Admin processes payment outside Odoo:
- Bank transfer, or
- Cash pickup, or
- Mobile wallet transfer
         ↓
┌─────────────────────────────────────────────────────────┐
│ Step 5: Mark as Completed (Optional)                    │
└─────────────────────────────────────────────────────────┘
Admin can update:
- withdrawal_status: "approved" → "completed"
- payment_date: When paid
         ↓
┌─────────────────────────────────────────────────────────┐
│ Step 6: Customer Notified                               │
└─────────────────────────────────────────────────────────┘
Firebase FCM (Phase 7):
"Your withdrawal of 50.00 EGP has been approved and processed"
```

**Duration:** 1-3 business days  
**Status:** Money transferred to customer

---

### Alternative: Reject Withdrawal

```
Admin decides: REJECT
         ↓
┌─────────────────────────────────────────────────────────┐
│ Step 3: Reject Withdrawal                               │
└─────────────────────────────────────────────────────────┘
Admin clicks "Reject" button
Dialog appears: "Enter rejection reason"
Admin types: "Insufficient documentation"
         ↓
┌─────────────────────────────────────────────────────────┐
│ Step 4: Reverse Transaction                             │
└─────────────────────────────────────────────────────────┘
Backend:
- withdrawal_status: "pending" → "rejected"
- rejection_reason: "Insufficient documentation"
         ↓
Create REVERSAL transaction:
- transaction_type: "credit"
- amount: 50.00 EGP
- description: "Withdrawal rejection reversal"
         ↓
Wallet balance restored:
- Before: 50.00 EGP
- After: 100.00 EGP ✅ (back to original)
         ↓
┌─────────────────────────────────────────────────────────┐
│ Step 5: Customer Notified                               │
└─────────────────────────────────────────────────────────┘
Firebase FCM:
"Withdrawal request rejected: Insufficient documentation"
```

**Duration:** ~1 minute  
**Status:** Balance restored, customer can try again

---

## 9️⃣ Error Handling Workflows

### Failed QR Code Scan

**Scenario:** Collector scans invalid QR code

**Flow:**

```
Collector scans: "random-invalid-code"
         ↓
POST /api/cyclex/collector/scan-qr
{
    "qr_code": "random-invalid-code"
}
         ↓
Backend searches:
SELECT * FROM cyclex_request WHERE qr_code = 'random-invalid-code'
         ↓
No match found
         ↓
Return error:
{
    "success": false,
    "error": {
        "code": 2003,
        "message": "Invalid QR code"
    }
}
         ↓
App displays: "Invalid QR code. Please try again."
Collector can retry ✅
```

---

### Duplicate Order Acceptance

**Scenario:** Collector tries to accept already-assigned order

**Flow:**

```
Collector A accepts order
         ↓
Order assigned to Collector A
         ↓
Collector B tries to accept same order
         ↓
Backend checks:
- Order status is still "pending"? ❌ (now "assigned")
         ↓
Return error:
{
    "success": false,
    "error": {
        "code": 2004,
        "message": "Request is already assigned to another collector"
    }
}
         ↓
Collector B sees: "Order no longer available"
```

---

### Insufficient Balance for Withdrawal

**Scenario:** Balance changes between request and processing

**Flow:**

```
Customer balance: 100 EGP
Customer requests: 50 EGP withdrawal ✅
Balance becomes: 50 EGP
         ↓
Customer requests another: 75 EGP withdrawal ❌
         ↓
Backend validates:
- Requested: 75 EGP
- Balance: 50 EGP
- 75 > 50 ❌
         ↓
Return error:
{
    "success": false,
    "error": {
        "code": 3002,
        "message": "Insufficient balance. Current: 50.00 EGP"
    }
}
```

---

## 🔟 Notification Workflow (Phase 7)

### When Firebase FCM is Implemented

**Order Assignment:**
```
Order assigned
    ↓
cyclex.notification service called
    ↓
Firebase FCM API:
POST https://fcm.googleapis.com/fcm/send
{
    "to": "customer_fcm_token",
    "notification": {
        "title": "Collector Assigned",
        "body": "Mahmoud accepted your order",
        "click_action": "OPEN_REQUEST_DETAILS"
    }
}
    ↓
Customer's phone receives push notification
    ↓
Customer taps notification
    ↓
App opens request details screen
```

---

## 📊 Workflow Summary Table

| Workflow | Trigger | Duration | Auto/Manual | Phase |
|----------|---------|----------|-------------|-------|
| **Customer Registration** | App signup | 2 min | Auto | ✅ Active |
| **Collector Registration** | App signup + admin | 1-3 days | Manual | ✅ Active |
| **Request Creation** | Customer creates | 2 sec | Auto | ✅ Active |
| **Order Assignment** | Collector accepts | 1 sec | Auto | ✅ Active |
| **Order Completion** | QR scan | 3 sec | Auto | ✅ Active |
| **Wallet Credit** | Order completed | Instant | Auto | ✅ Active |
| **Commission Creation** | Order completed | Instant | Auto | ✅ Active |
| **Withdrawal Request** | Customer requests | 1 sec | Auto | ✅ Active |
| **Withdrawal Approval** | Admin reviews | 1-3 days | Manual | ✅ Active |
| **Auto-Revert Orders** | Cron (6hrs) | Instant | Auto | ✅ Active |
| **SMS Verification** | Registration | 1 min | Auto | 🔜 Phase 7 |
| **Push Notifications** | Various triggers | Instant | Auto | 🔜 Phase 7 |

---

## 🎯 Workflow Optimization Tips

### For Faster Order Processing:

1. **Verify collectors quickly** (within 24 hours)
2. **Monitor pending orders** daily
3. **Balance working areas** (assign collectors evenly)
4. **Quick withdrawal approvals** (same day if possible)

### For Better Customer Experience:

1. **Approve withdrawals quickly**
2. **Respond to low ratings** (check comments)
3. **Monitor completion times**
4. **Keep product prices updated**

### For System Health:

1. **Monitor cron jobs** (check logs)
2. **Archive old data** (6+ months)
3. **Review error logs** weekly
4. **Check database performance**

---

## 📚 Related Documentation

- **Database Schema:** `docs/DATABASE_SCHEMA.md`
- **User Permissions:** `docs/USER_ROLES_PERMISSIONS.md`
- **API Workflows:** `API_DOCUMENTATION.md`
- **Testing:** `docs/testing/BACKEND_TESTING_GUIDE.md`

---

**Last Updated:** October 17, 2025  
**Maintained By:** CycleX Technical Team

