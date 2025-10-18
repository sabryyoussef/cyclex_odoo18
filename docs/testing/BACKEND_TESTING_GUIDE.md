# CycleX Backend Testing Guide 🧪

**Complete guide for testing all backend functionality in Odoo**

---

## 🎯 Overview

This guide covers testing for:
1. Model constraints and validations
2. Computed fields (balances, ratings, commission)
3. Workflow transitions (pending → assigned → collected)
4. Commission calculations
5. QR code generation and validation
6. Scheduled actions (cron jobs)

---

## 🔧 Testing Environment Setup

### Prerequisites:
- ✅ Odoo 18 running on port 10018
- ✅ CycleX module installed and upgraded
- ✅ Sample data loaded
- ✅ Access to Odoo web interface (http://localhost:10018)

### Test User:
```
Username: admin@cyclex.com
Password: admin
Database: cyclex_db
```

---

## 1️⃣ Model Constraints & Validations Testing

### 1.1 Phone Number Validation

**Test Case:** Egyptian phone number format validation

**Steps:**
1. Go to **CycleX → Customers → Create**
2. Set `Is CycleX User` = True
3. Set `User Type` = Customer

**Test Data:**

| Phone Number | Expected Result |
|--------------|-----------------|
| `+201234567890` | ✅ Valid |
| `+201012345678` | ✅ Valid |
| `+201512345678` | ✅ Valid |
| `+201612345678` | ❌ Invalid (16 not allowed) |
| `+201234567` | ❌ Invalid (too short) |
| `01234567890` | ✅ Valid (auto-formats to +20) |
| `1234567890` | ❌ Invalid (no country code) |
| `+15551234567` | ❌ Invalid (not Egyptian) |

**Expected Error:**
```
Invalid Egyptian phone number format.
Phone must start with +20 or 01 followed by 10 digits.
Example: +201234567890 or 01234567890
```

**Status:** Test in Odoo backend by creating customers

---

### 1.2 Password Strength Validation

**Test Case:** Password requirements validation

**Test via API:** Use Postman `/api/cyclex/register`

**Test Data:**

| Password | Expected Result | Reason |
|----------|-----------------|--------|
| `TestPass123` | ✅ Valid | Has uppercase, lowercase, number, 8+ chars |
| `test123` | ❌ Invalid | No uppercase |
| `TESTPASS123` | ❌ Invalid | No lowercase |
| `TestPassword` | ❌ Invalid | No number |
| `Test123` | ❌ Invalid | Less than 8 characters |
| `Test@Pass123` | ✅ Valid | Special chars allowed |

**Expected Error Examples:**
```
- "Password must be at least 8 characters long"
- "Password must contain at least one uppercase letter"
- "Password must contain at least one lowercase letter"
- "Password must contain at least one number"
```

---

### 1.3 Duplicate Phone Number Validation

**Test Case:** No duplicate phones for CycleX users

**Steps:**
1. Create customer with phone `+201234567890`
2. Try to create another CycleX user with same phone

**Expected Result:**
```
❌ Error: "Phone number already exists for another CycleX user"
```

**Note:** Regular contacts can have duplicate phones, only CycleX users are restricted

---

### 1.4 Working Areas Limit (Collector)

**Test Case:** Collectors can have max 5 working areas

**Steps:**
1. Go to **CycleX → Collectors**
2. Open a collector
3. Try to add 6 working areas

**Expected Result:**
```
❌ Error: "Collectors can only be assigned to a maximum of 5 working areas"
```

**Test Data:**
```python
# Via Odoo shell:
collector = env['res.partner'].browse(5)  # Collector ID
collector.write({
    'working_area_ids': [(6, 0, [1, 2, 3, 4, 5, 6])]  # 6 areas
})
# Should raise ValidationError
```

---

### 1.5 Image Size Validation

**Test Case:** Max 5MB per image

**Test via API:** Use Postman `/api/cyclex/request/create`

**Test Data:**
- Small image (1 MB): ✅ Valid
- Medium image (3 MB): ✅ Valid
- Large image (6 MB): ❌ Invalid

**Expected Error:**
```
{
    "error": {
        "code": 1004,
        "message": "Image size (6.5 MB) exceeds maximum allowed size of 5 MB"
    }
}
```

---

## 2️⃣ Computed Fields Testing

### 2.1 Wallet Balance Computation

**Test Case:** `current_balance` = total credits - total debits

**Test Steps:**

```python
# Via Odoo shell or API
# 1. Get customer wallet
wallet = env['cyclex.wallet'].search([('partner_id.phone', '=', '+201001234567')])
initial_balance = wallet.current_balance  # Should be 0.00

# 2. Add credit (via order completion)
wallet.add_credit(100.00, 'Test credit', request_id=1)
# Expected: current_balance = 100.00

# 3. Add another credit
wallet.add_credit(50.00, 'Another credit', request_id=2)
# Expected: current_balance = 150.00

# 4. Add debit (withdrawal)
wallet.add_debit(30.00, 'Withdrawal')
# Expected: current_balance = 120.00

# 5. Verify computation
print(f"Balance: {wallet.current_balance}")
print(f"Total Credits: {wallet.total_credits}")  # 150.00
print(f"Total Debits: {wallet.total_debits}")    # 30.00
```

**Expected Results:**
- `total_credits` = 150.00
- `total_debits` = 30.00
- `current_balance` = 120.00
- `transaction_count` = 3

---

### 2.2 Request Calculated Price

**Test Case:** `calculated_price` = quantity × product price_per_kg

**Test Data:**

| Product | Price/Unit | Quantity | Expected Price |
|---------|------------|----------|----------------|
| Plastic Bottles | 3.50 EGP/kg | 10 kg | 35.00 EGP |
| Cardboard | 2.50 EGP/kg | 25 kg | 62.50 EGP |
| Aluminum Cans | 8.00 EGP/kg | 5 kg | 40.00 EGP |
| Mobile Phones | 50.00 EGP/unit | 3 units | 150.00 EGP |

**Test via API:**
```json
POST /api/cyclex/request/create
{
    "product_id": 1,
    "quantity": 10,
    "unit": "kg"
}
```

**Expected Response:**
```json
{
    "data": {
        "calculated_price": 35.00
    }
}
```

**Verify in Odoo Backend:**
1. Go to **CycleX → Recycling Requests**
2. Check `Calculated Price` field matches quantity × price

---

### 2.3 Commission Calculation

**Test Case:** Commission = request price × collector commission_rate

**Test Data:**

| Request Price | Commission Rate | Expected Commission |
|--------------|-----------------|---------------------|
| 100.00 EGP | 15% | 15.00 EGP |
| 50.00 EGP | 15% | 7.50 EGP |
| 150.00 EGP | 15% | 22.50 EGP |

**Test Steps:**

1. **Create Request (Customer):**
```json
POST /api/cyclex/request/create
{
    "product_id": 1,
    "quantity": 10,
    "unit": "kg"
}
// Expected price: 35.00 EGP
```

2. **Accept Order (Collector with 15% rate):**
```json
POST /api/cyclex/collector/accept-order
{
    "request_id": 1
}
```

3. **Complete Order (Scan QR):**
```json
POST /api/cyclex/collector/scan-qr
{
    "qr_code": "CYCLEX-REQ-00001-..."
}
```

4. **Verify Commission:**
```python
# In Odoo backend or via API
commission = env['cyclex.commission'].search([('request_id', '=', 1)])
print(f"Request Price: {commission.amount}")  # 35.00
print(f"Commission Rate: {commission.commission_rate}%")  # 15%
print(f"Commission: {commission.commission_amount}")  # 5.25
```

**Expected:**
- `amount` = 35.00 EGP (request price)
- `commission_rate` = 15.00%
- `commission_amount` = 5.25 EGP (35.00 × 0.15)

---

### 2.4 Transaction Count

**Test Case:** Wallet `transaction_count` updates automatically

**Test Steps:**

```python
# Get wallet
wallet = env['cyclex.wallet'].search([('partner_id.phone', '=', '+201001234567')])

# Initial count
print(wallet.transaction_count)  # 0

# Add transactions
wallet.add_credit(100, 'Test 1', request_id=1)
print(wallet.transaction_count)  # 1

wallet.add_credit(50, 'Test 2', request_id=2)
print(wallet.transaction_count)  # 2

wallet.add_debit(20, 'Test 3')
print(wallet.transaction_count)  # 3
```

**Expected:** Count increments with each transaction

---

## 3️⃣ Workflow Transitions Testing

### 3.1 Request Status Workflow

**Complete Workflow:**
```
draft → pending → assigned → collected
                      ↓
                  cancelled
```

**Test Scenario:**

**Step 1: Create Request (draft → pending)**
```json
POST /api/cyclex/request/create
{
    "product_id": 1,
    "quantity": 10,
    "unit": "kg",
    "pickup_date": "2025-10-25",
    "pickup_time": "morning",
    "location_latitude": 30.0444,
    "location_longitude": 31.2357,
    "address": "15 El Nasr Street"
}
```

**Expected:**
- Status: `pending` ✅
- Collector: Empty
- QR Code: Generated

---

**Step 2: Collector Accepts (pending → assigned)**
```json
POST /api/cyclex/collector/accept-order
{
    "request_id": 1
}
```

**Expected:**
- Status: `assigned` ✅
- Collector: Set to current collector
- `write_date` updated (for 3-day deadline)

---

**Step 3: Complete Order (assigned → collected)**
```json
POST /api/cyclex/collector/scan-qr
{
    "qr_code": "CYCLEX-REQ-00001-..."
}
```

**Expected:**
- Status: `collected` ✅
- Collection Date: Set to now
- Customer wallet: +35.00 EGP
- Commission created: 5.25 EGP
- QR Code: Still valid but can't be reused

---

**Step 4: Reject Order (assigned → pending)**
```json
POST /api/cyclex/collector/reject-order
{
    "request_id": 1,
    "reason": "Too far"
}
```

**Expected:**
- Status: Back to `pending` ✅
- Collector: Removed
- Available to other collectors again

---

### 3.2 Withdrawal Workflow

**Workflow:**
```
Request → Pending → Approved → Completed
                        ↓
                    Rejected
```

**Test in Odoo Backend:**

1. **Customer Requests Withdrawal:**
   - Via API: `/api/cyclex/wallet/debit`
   - Status: `pending`
   - Balance deducted immediately

2. **Admin Approves:**
   - Odoo → CycleX → Wallet Transactions
   - Open pending withdrawal
   - Click "Approve" button
   - Status: `approved`
   - `approved_by` = admin
   - `approval_date` = now

3. **Admin Rejects:**
   - Click "Reject" button
   - Enter rejection reason
   - Status: `rejected`
   - Balance restored (transaction reversed)

---

## 4️⃣ Commission Calculations Testing

### 4.1 Standard Commission (15%)

**Formula:** `commission = request_price × 0.15`

**Test Cases:**

```python
# Test via Odoo shell
Request = env['cyclex.request']
Commission = env['cyclex.commission']

# Test 1: Small order
request1 = Request.create({
    'customer_id': 5,
    'product_id': 1,
    'quantity': 10,
    'unit': 'kg',
    # ... other required fields
})
# Calculated price: 10 × 3.50 = 35.00 EGP

# Complete the order
request1.write({'status': 'collected', 'collector_id': 10})

# Check commission
comm1 = Commission.search([('request_id', '=', request1.id)])
assert comm1.commission_amount == 5.25  # 35.00 × 0.15

# Test 2: Large order
request2 = Request.create({
    'customer_id': 5,
    'product_id': 10,  # Mobile phones: 50 EGP/unit
    'quantity': 4,
    'unit': 'unit',
    # ...
})
# Calculated price: 4 × 50 = 200.00 EGP
# Expected commission: 200 × 0.15 = 30.00 EGP

# Test 3: Decimal quantity
request3 = Request.create({
    'customer_id': 5,
    'product_id': 1,
    'quantity': 12.5,
    'unit': 'kg',
    # ...
})
# Calculated price: 12.5 × 3.50 = 43.75 EGP
# Expected commission: 43.75 × 0.15 = 6.56 EGP
```

---

### 4.2 Variable Commission Rates

**Test Case:** Different collectors, different rates

**Steps:**

1. **Set Custom Rate:**
   - Go to **CycleX → Collectors**
   - Open Mahmoud Saad
   - Set `Commission Rate` = 20%

2. **Create & Complete Order:**
   - Customer creates request (100 EGP)
   - Mahmoud accepts
   - Mahmoud completes

3. **Verify Commission:**
   - Expected: 20.00 EGP (100 × 0.20)
   - NOT: 15.00 EGP (default rate)

**SQL Verification:**
```sql
SELECT 
    r.name as request,
    r.calculated_price,
    c.commission_rate,
    c.commission_amount,
    (r.calculated_price * c.commission_rate / 100) as expected_commission
FROM cyclex_commission c
JOIN cyclex_request r ON c.request_id = r.id
WHERE c.id = 1;
```

---

## 5️⃣ QR Code Generation & Validation

### 5.1 QR Code Generation

**Test Case:** QR code auto-generated on request creation

**Test Steps:**

1. **Create Request via API:**
```json
POST /api/cyclex/request/create
{
    "product_id": 1,
    "quantity": 10,
    "unit": "kg",
    "pickup_date": "2025-10-25",
    "pickup_time": "morning",
    "location_latitude": 30.0444,
    "location_longitude": 31.2357,
    "address": "Test address"
}
```

2. **Verify QR Code Generated:**
```json
{
    "data": {
        "qr_code": "CYCLEX-REQ-00001-a1b2c3d4-e5f6-7890-abcd-1234567890ab",
        "qr_code_image": "iVBORw0KGgoAAAANS..." // Base64 PNG
    }
}
```

3. **Verify Format:**
   - Starts with `CYCLEX-REQ-`
   - Contains request number (00001)
   - Contains UUID (36 characters)
   - Total length: ~60 characters

4. **Verify Uniqueness:**
   - Create 10 requests
   - Each should have different UUID
   - No duplicates

---

### 5.2 QR Code Validation

**Test Case:** QR code validation on scan

**Valid QR Codes:**

```json
// Test 1: Valid QR code
POST /api/cyclex/collector/scan-qr
{
    "qr_code": "CYCLEX-REQ-00001-valid-uuid-here"
}
// Expected: ✅ Success, order completed
```

**Invalid QR Codes:**

| QR Code | Expected Error | Code |
|---------|----------------|------|
| `CYCLEX-REQ-00001-invalid` | Invalid QR code | 2003 |
| `random-string` | Invalid QR code | 2003 |
| (Empty) | QR code is required | 1002 |
| Already used QR | Request already collected | 2005 |
| Cancelled request QR | Request is cancelled | 2007 |

---

### 5.3 QR Code Image Display

**Test in Odoo Backend:**

1. Go to **CycleX → Recycling Requests**
2. Open any request
3. Scroll to "QR Code & Rating" section
4. Verify:
   - ✅ QR Code text displayed
   - ✅ QR Code image displayed (200×200 px)
   - ✅ Image is scannable (test with phone)

**Test via API:**
```json
POST /api/cyclex/request/details
{
    "request_id": 1
}
```

**Expected Response:**
```json
{
    "data": {
        "qr_code_image": "base64_encoded_png_here"
    }
}
```

Decode base64 and verify it's valid PNG image.

---

## 6️⃣ Scheduled Actions (Cron Jobs) Testing

### 6.1 Auto-Revert Overdue Orders

**Cron Job:** Runs every 6 hours

**Test Case:** Orders assigned for 3+ days auto-revert to pending

**Manual Test Steps:**

```python
# Via Odoo shell

# 1. Create and assign an order
request = env['cyclex.request'].create({
    'customer_id': 5,
    'product_id': 1,
    'quantity': 10,
    'unit': 'kg',
    'pickup_date': '2025-10-20',
    'pickup_time': 'morning',
    'location_latitude': 30.0444,
    'location_longitude': 31.2357,
    'address': 'Test address',
    'status': 'assigned',
    'collector_id': 10,
})

# 2. Manually set write_date to 4 days ago
from datetime import timedelta
old_date = fields.Datetime.now() - timedelta(days=4)
env.cr.execute(
    "UPDATE cyclex_request SET write_date = %s WHERE id = %s",
    (old_date, request.id)
)
env.cr.commit()

# 3. Manually trigger cron job
env['cyclex.request']._cron_auto_revert_overdue_orders()

# 4. Verify order reverted
request.invalidate_cache()
print(f"Status: {request.status}")  # Expected: 'pending'
print(f"Collector: {request.collector_id}")  # Expected: False (empty)
```

**Expected Results:**
- Status changed to `pending` ✅
- Collector removed ✅
- Message posted in chatter ✅
- Log entry created ✅

---

### 6.2 Pending Withdrawals Notification

**Cron Job:** Runs daily

**Test Case:** Notifies admin about pending withdrawals

**Manual Test Steps:**

```python
# Via Odoo shell

# 1. Create pending withdrawal
wallet = env['cyclex.wallet'].search([('partner_id.phone', '=', '+201001234567')])
wallet.add_credit(100, 'Test credit', request_id=1)
wallet.add_debit(50, 'Withdrawal request')

# 2. Verify transaction is pending
transaction = env['cyclex.wallet.transaction'].search([
    ('wallet_id', '=', wallet.id),
    ('transaction_type', '=', 'debit')
], limit=1)
print(f"Withdrawal Status: {transaction.withdrawal_status}")  # Expected: 'pending'

# 3. Manually trigger cron job
env['cyclex.wallet']._cron_notify_pending_withdrawals()

# 4. Check logs
# Should see: "Found X pending withdrawal requests"
```

**Expected Results:**
- Log message with count of pending withdrawals ✅
- Admin notified (via Odoo message/log) ✅

---

### 6.3 Test Cron Jobs Manually

**Access Cron Jobs:**
1. Go to **Settings → Technical → Automation → Scheduled Actions**
2. Search for "CycleX"
3. Should see:
   - `CycleX: Auto-Revert Overdue Orders` (Every 6 hours)
   - `CycleX: Process Pending Withdrawals` (Daily)

**Run Manually:**
1. Open cron job
2. Click "Run Manually" button
3. Check logs in terminal for execution

**Verify Last Run:**
- Check `Last Execution Date`
- Check `Number of Calls` (increments)

---

## 7️⃣ Model Constraints Summary

### Test All Constraints Checklist:

**Partner (res.partner):**
- [ ] Egyptian phone format validation
- [ ] No duplicate phones for CycleX users
- [ ] Max 5 working areas per collector

**Request (cyclex.request):**
- [ ] Image size max 5MB
- [ ] Pickup date must be future date
- [ ] Quantity must be positive
- [ ] Status transitions valid

**Wallet (cyclex.wallet):**
- [ ] Balance cannot go negative
- [ ] Withdrawal amount ≤ balance
- [ ] Minimum withdrawal 10 EGP

**Commission (cyclex.commission):**
- [ ] Commission amount computed correctly
- [ ] Cannot modify after creation
- [ ] Linked to valid request

---

## 8️⃣ Comprehensive Test Script

### Python Test Script (Odoo Shell)

Save as: `custom_addons/cyclex/tests/test_backend.py`

```python
# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError
from datetime import timedelta
from odoo import fields

class TestCyclexBackend(TransactionCase):
    
    def setUp(self):
        super(TestCyclexBackend, self).setUp()
        self.Partner = self.env['res.partner']
        self.Request = self.env['cyclex.request']
        self.Wallet = self.env['cyclex.wallet']
        self.Commission = self.env['cyclex.commission']
        
        # Create test customer
        self.customer = self.Partner.create({
            'name': 'Test Customer',
            'phone': '+201999999999',
            'is_cyclex_user': True,
            'cyclex_user_type': 'customer',
            'phone_verified': True,
        })
        
        # Create test collector
        self.collector = self.Partner.create({
            'name': 'Test Collector',
            'phone': '+201888888888',
            'is_cyclex_user': True,
            'cyclex_user_type': 'collector',
            'phone_verified': True,
            'collector_verified': True,
            'commission_rate': 15.00,
        })
        
        # Get test product
        self.product = self.env['cyclex.product'].search([], limit=1)
    
    def test_phone_validation(self):
        """Test Egyptian phone number validation"""
        # Valid phone
        partner = self.Partner.create({
            'name': 'Valid Phone',
            'phone': '+201234567890',
            'is_cyclex_user': True,
            'cyclex_user_type': 'customer',
        })
        self.assertTrue(partner.id)
        
        # Invalid phone - should raise error
        with self.assertRaises(ValidationError):
            self.Partner.create({
                'name': 'Invalid Phone',
                'phone': '+201234567',  # Too short
                'is_cyclex_user': True,
                'cyclex_user_type': 'customer',
            })
    
    def test_duplicate_phone(self):
        """Test no duplicate phones for CycleX users"""
        # Create first user
        self.Partner.create({
            'name': 'First User',
            'phone': '+201777777777',
            'is_cyclex_user': True,
            'cyclex_user_type': 'customer',
        })
        
        # Try to create duplicate - should fail
        with self.assertRaises(ValidationError):
            self.Partner.create({
                'name': 'Duplicate User',
                'phone': '+201777777777',
                'is_cyclex_user': True,
                'cyclex_user_type': 'customer',
            })
    
    def test_wallet_balance_computation(self):
        """Test wallet balance = credits - debits"""
        wallet = self.customer.wallet_id
        
        # Initial balance
        self.assertEqual(wallet.current_balance, 0.0)
        
        # Add credits
        wallet.add_credit(100.00, 'Test credit', request_id=1)
        self.assertEqual(wallet.current_balance, 100.0)
        
        wallet.add_credit(50.00, 'Another credit', request_id=2)
        self.assertEqual(wallet.current_balance, 150.0)
        
        # Add debit
        wallet.add_debit(30.00, 'Withdrawal')
        self.assertEqual(wallet.current_balance, 120.0)
        
        # Verify totals
        self.assertEqual(wallet.total_credits, 150.0)
        self.assertEqual(wallet.total_debits, 30.0)
        self.assertEqual(wallet.transaction_count, 3)
    
    def test_calculated_price(self):
        """Test request calculated price = quantity × price"""
        request = self.Request.create({
            'customer_id': self.customer.id,
            'product_id': self.product.id,
            'quantity': 10.0,
            'unit': 'kg',
            'pickup_date': fields.Date.today() + timedelta(days=1),
            'pickup_time': 'morning',
            'location_latitude': 30.0444,
            'location_longitude': 31.2357,
            'address': 'Test address',
        })
        
        expected_price = 10.0 * self.product.price_per_kg
        self.assertEqual(request.calculated_price, expected_price)
    
    def test_commission_calculation(self):
        """Test commission = price × rate"""
        # Create and complete request
        request = self.Request.create({
            'customer_id': self.customer.id,
            'product_id': self.product.id,
            'quantity': 10.0,
            'unit': 'kg',
            'pickup_date': fields.Date.today() + timedelta(days=1),
            'pickup_time': 'morning',
            'location_latitude': 30.0444,
            'location_longitude': 31.2357,
            'address': 'Test address',
            'status': 'assigned',
            'collector_id': self.collector.id,
        })
        
        # Complete order
        request.write({'status': 'collected'})
        
        # Check commission
        commission = self.Commission.search([('request_id', '=', request.id)])
        expected_commission = request.calculated_price * 0.15
        self.assertEqual(commission.commission_amount, expected_commission)
    
    def test_qr_code_generation(self):
        """Test QR code auto-generated"""
        request = self.Request.create({
            'customer_id': self.customer.id,
            'product_id': self.product.id,
            'quantity': 10.0,
            'unit': 'kg',
            'pickup_date': fields.Date.today() + timedelta(days=1),
            'pickup_time': 'morning',
            'location_latitude': 30.0444,
            'location_longitude': 31.2357,
            'address': 'Test address',
        })
        
        # Verify QR code exists
        self.assertTrue(request.qr_code)
        self.assertTrue(request.qr_code.startswith('CYCLEX-REQ-'))
        self.assertTrue(request.qr_code_image)  # Binary image exists
    
    def test_qr_code_uniqueness(self):
        """Test each request has unique QR code"""
        qr_codes = []
        for i in range(5):
            request = self.Request.create({
                'customer_id': self.customer.id,
                'product_id': self.product.id,
                'quantity': 10.0,
                'unit': 'kg',
                'pickup_date': fields.Date.today() + timedelta(days=1),
                'pickup_time': 'morning',
                'location_latitude': 30.0444,
                'location_longitude': 31.2357,
                'address': 'Test address',
            })
            qr_codes.append(request.qr_code)
        
        # All QR codes should be unique
        self.assertEqual(len(qr_codes), len(set(qr_codes)))
    
    def test_workflow_transitions(self):
        """Test request status workflow"""
        request = self.Request.create({
            'customer_id': self.customer.id,
            'product_id': self.product.id,
            'quantity': 10.0,
            'unit': 'kg',
            'pickup_date': fields.Date.today() + timedelta(days=1),
            'pickup_time': 'morning',
            'location_latitude': 30.0444,
            'location_longitude': 31.2357,
            'address': 'Test address',
        })
        
        # Initial state
        self.assertEqual(request.status, 'pending')
        
        # Assign to collector
        request.write({
            'status': 'assigned',
            'collector_id': self.collector.id
        })
        self.assertEqual(request.status, 'assigned')
        
        # Complete order
        request.write({'status': 'collected'})
        self.assertEqual(request.status, 'collected')
        
        # Verify wallet credited
        wallet = self.customer.wallet_id
        self.assertEqual(wallet.current_balance, request.calculated_price)
    
    def test_auto_revert_overdue(self):
        """Test auto-revert of overdue orders"""
        # Create assigned order
        request = self.Request.create({
            'customer_id': self.customer.id,
            'product_id': self.product.id,
            'quantity': 10.0,
            'unit': 'kg',
            'pickup_date': fields.Date.today() + timedelta(days=1),
            'pickup_time': 'morning',
            'location_latitude': 30.0444,
            'location_longitude': 31.2357,
            'address': 'Test address',
            'status': 'assigned',
            'collector_id': self.collector.id,
        })
        
        # Simulate 4 days old
        old_date = fields.Datetime.now() - timedelta(days=4)
        self.env.cr.execute(
            "UPDATE cyclex_request SET write_date = %s WHERE id = %s",
            (old_date, request.id)
        )
        self.env.cr.commit()
        
        # Run cron job
        self.Request._cron_auto_revert_overdue_orders()
        
        # Verify reverted
        request.invalidate_cache()
        self.assertEqual(request.status, 'pending')
        self.assertFalse(request.collector_id)
    
    def test_withdrawal_approval(self):
        """Test withdrawal approval workflow"""
        wallet = self.customer.wallet_id
        
        # Add some balance
        wallet.add_credit(100.00, 'Test credit', request_id=1)
        
        # Request withdrawal
        wallet.add_debit(50.00, 'Withdrawal')
        
        # Get transaction
        transaction = self.env['cyclex.wallet.transaction'].search([
            ('wallet_id', '=', wallet.id),
            ('transaction_type', '=', 'debit')
        ], limit=1)
        
        # Verify pending
        self.assertEqual(transaction.withdrawal_status, 'pending')
        
        # Approve
        transaction.action_approve_withdrawal()
        self.assertEqual(transaction.withdrawal_status, 'approved')
        
        # Balance should remain deducted
        self.assertEqual(wallet.current_balance, 50.0)
```

---

## 9️⃣ Running Tests

### Option 1: Via Odoo Test Framework

```bash
cd /media/sabry3/sabry_backup/cycle_x/odoo18

# Run all tests
python odoo-bin -c ../odoo_conf/odoo.conf -d cyclex_db --test-enable --stop-after-init -u cyclex

# Run specific test
python odoo-bin -c ../odoo_conf/odoo.conf -d cyclex_db --test-enable --test-tags /cyclex
```

---

### Option 2: Via Odoo Shell (Manual Testing)

```bash
cd /media/sabry3/sabry_backup/cycle_x/odoo18
python odoo-bin shell -c ../odoo_conf/odoo.conf -d cyclex_db
```

Then run test commands from this guide.

---

### Option 3: Via Postman (API Testing)

Use the Postman collection to test:
- All 22 endpoints
- Error responses
- Workflow transitions

---

## ✅ Testing Checklist

### Constraints & Validations:
- [ ] Phone number format (Egyptian +20)
- [ ] No duplicate phones for CycleX users
- [ ] Password strength (8+ chars, upper, lower, number)
- [ ] Max 5 working areas per collector
- [ ] Image size max 5MB
- [ ] Minimum withdrawal 10 EGP
- [ ] Balance cannot go negative

### Computed Fields:
- [ ] Wallet balance = credits - debits
- [ ] Transaction count updates
- [ ] Request calculated_price = quantity × price
- [ ] Commission amount = price × rate

### Workflows:
- [ ] Request: pending → assigned → collected
- [ ] Request: assigned → pending (reject)
- [ ] Withdrawal: pending → approved
- [ ] Withdrawal: pending → rejected (balance restored)

### QR Codes:
- [ ] Auto-generated on request creation
- [ ] Unique per request
- [ ] Contains request number + UUID
- [ ] Image generated (PNG base64)
- [ ] Validation works (scan endpoint)

### Cron Jobs:
- [ ] Auto-revert runs every 6 hours
- [ ] Orders 3+ days old revert to pending
- [ ] Pending withdrawals notification runs daily
- [ ] Logs show execution

### Business Logic:
- [ ] Collector max 5 pending orders
- [ ] Wallet auto-credited on order completion
- [ ] Commission auto-created on completion
- [ ] Rating only for collected orders
- [ ] Can't scan QR twice

---

## 📊 Test Results Template

```
=== CycleX Backend Testing Results ===
Date: [DATE]
Tester: [NAME]
Module Version: 18.0.1.0.0

✅ Constraints & Validations:  [X/7]
✅ Computed Fields:            [X/4]
✅ Workflows:                  [X/4]
✅ QR Codes:                   [X/5]
✅ Cron Jobs:                  [X/2]
✅ Business Logic:             [X/5]

Total: [X/27] tests passed

Issues Found:
1. [Issue description]
2. [Issue description]

Notes:
- [Any observations]
```

---

**Next:** Complete all tests and document results! 🚀

