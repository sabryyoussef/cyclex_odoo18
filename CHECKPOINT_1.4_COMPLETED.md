# Checkpoint 1.4: Core Models - Requests/Orders ✅

**Status:** Completed  
**Date:** October 17, 2025  
**Module:** CycleX v18.0.1.0.0

---

## 📋 Objectives

Complete the Request/Order model for managing recyclable material collection requests between customers and collectors.

---

## ✅ Tasks Completed

### 1. CyclexRequest Model Enhanced

**Model:** `cyclex.request`  
**Description:** Core model for managing recycling pickup requests

**All Required Fields Implemented:**

#### Customer & Collector Fields
- ✅ **Customer** (many2one res.partner) - Required, domain filtered
- ✅ **Collector** (many2one res.partner) - Optional, assigned later

#### Product & Pricing Fields
- ✅ **Category** (many2one cyclex.category) - Required
- ✅ **Product** (many2one cyclex.product) - Required, filtered by category
- ✅ **Quantity** (integer) - Required, default: 1
- ✅ **Weight (KG)** (float) - Required, 2 decimal places
- ✅ **Calculated Price** (monetary) - Computed from weight × price_per_kg

#### Status & Dates
- ✅ **Status** (selection) - draft/pending/assigned/collected/cancelled
- ✅ **Pickup Date** (date) - Required
- ✅ **Creation Date** (datetime) - Auto-populated, readonly
- ✅ **Completion Date** (datetime) - Set when status = collected

#### Photos & Media
- ✅ **Photo 1** (binary) - Attachment field
- ✅ **Photo 2** (binary) - Attachment field

#### GPS Location
- ✅ **GPS Latitude** (float) - From customer location
- ✅ **GPS Longitude** (float) - From customer location
- Auto-populated from customer's profile on creation

#### QR Code & Verification
- ✅ **QR Code** (char) - Unique UUID, auto-generated
- ✅ **Request Number** (char) - Auto-sequence: REQ/2025/0001

#### Rating & Feedback
- ✅ **Rating** (selection) - 1-5 stars
- ✅ **Comments** (text) - Customer feedback

#### Supporting Fields
- ✅ **Currency** (many2one res.currency) - For price calculation
- ✅ **Company** (many2one res.company) - Multi-company support

---

## 🔧 Technical Features Implemented

### 1. Computed Fields

**Price Calculation:**
```python
@api.depends('weight', 'product_id', 'product_id.price_per_kg')
def _compute_calculated_price(self):
    calculated_price = weight × price_per_kg
```

### 2. QR Code Generation

**Automatic UUID Generation:**
```python
def _generate_qr_code(self):
    return str(uuid.uuid4())
```

- Unique identifier for each request
- Used for mobile app scanning
- Generated automatically on creation

### 3. GPS Location Auto-fill

**Customer Location Retrieval:**
- Automatically copies customer's GPS coordinates to request
- Fallback to manual entry if customer location not available
- Helps collectors locate pickup point

### 4. Sequence Generation

**Request Numbering:**
- Format: REQ/2025/0001
- Auto-incremented
- Configured via `cyclex.request` sequence

---

## 🔄 Business Logic Methods

### Status Workflow Methods

#### 1. **action_submit()**
- Transition: draft → pending
- Makes request visible to collectors
- Validates status before transition

#### 2. **action_assign_collector(collector_id)**
- Transition: pending → assigned
- Assigns a collector to the request
- TODO: Send notification to collector

#### 3. **action_mark_collected()**
- Transition: assigned → collected
- Sets completion_date
- TODO: Create wallet transaction
- TODO: Create commission record
- TODO: Send notification to customer

#### 4. **action_cancel()**
- Cancels the request (except if collected)
- Available from any status except collected

---

## ✅ Data Validation

### Constraints Implemented

#### 1. **Weight Validation**
```python
@api.constrains('weight')
def _check_weight(self):
    if weight <= 0:
        raise ValidationError('Weight must be greater than zero.')
```

#### 2. **Quantity Validation**
```python
@api.constrains('quantity')
def _check_quantity(self):
    if quantity <= 0:
        raise ValidationError('Quantity must be greater than zero.')
```

#### 3. **Pickup Date Validation**
```python
@api.constrains('pickup_date')
def _check_pickup_date(self):
    if pickup_date < today:
        raise ValidationError('Pickup date cannot be in the past.')
```

---

## 📊 Status Workflow

```
Draft → Submit → Pending → Assign → Assigned → Collect → Collected
  ↓                ↓                    ↓                      
Cancel          Cancel               Cancel                   
```

**Status Definitions:**
- **Draft:** Initial state, being created by customer
- **Pending:** Submitted, waiting for collector assignment
- **Assigned:** Collector assigned, awaiting pickup
- **Collected:** Items collected, transaction complete
- **Cancelled:** Request cancelled (can't cancel after collected)

---

## 🔗 Integration Points

### Current Integrations
- ✅ **res.partner** - Customer and collector relationships
- ✅ **cyclex.category** - Material categorization
- ✅ **cyclex.product** - Product selection and pricing
- ✅ **mail.thread** - Activity tracking and chatter
- ✅ **ir.sequence** - Request numbering

### Future Integrations (Checkpoints 1.5-1.7)
- 🔲 **cyclex.wallet** - Customer earnings (on collection)
- 🔲 **cyclex.commission** - Collector earnings (on collection)
- 🔲 **Firebase FCM** - Push notifications
- 🔲 **Mobile API** - REST endpoints for mobile apps

---

## 📈 Database Changes

### New Fields Added
| Field | Type | Purpose |
|-------|------|---------|
| `gps_latitude` | Float(10,7) | Customer location latitude |
| `gps_longitude` | Float(10,7) | Customer location longitude |
| `completion_date` | Datetime | When request was completed |
| `qr_code` | Char (indexed) | Unique verification code |

### Existing Fields Enhanced
- `create_date` - Now indexed for performance
- `status` - Tracked for audit trail
- `calculated_price` - Stored for performance

---

## 🎯 Example Request Flow

**1. Customer Creates Request:**
```python
request = env['cyclex.request'].create({
    'customer_id': customer_id,
    'category_id': plastic_category_id,
    'product_id': pet_bottles_id,
    'quantity': 10,
    'weight': 5.5,  # kg
    'pickup_date': '2025-10-20',
    # GPS auto-filled from customer
    # QR code auto-generated
    # Request number auto-assigned
})
# calculated_price = 5.5 kg × 3.50 EGP/kg = 19.25 EGP
```

**2. Customer Submits:**
```python
request.action_submit()
# status: draft → pending
```

**3. Collector Accepts:**
```python
request.action_assign_collector(collector_id)
# status: pending → assigned
# TODO: Notification sent to collector
```

**4. Collector Picks Up:**
```python
request.action_mark_collected()
# status: assigned → collected
# completion_date set
# TODO: Wallet credited: +19.25 EGP
# TODO: Commission created: 5% = 0.96 EGP
```

---

## 🧪 Testing Checklist

### Manual Testing Performed
- ✅ Request creation with all fields
- ✅ QR code auto-generation verified
- ✅ GPS location auto-fill from customer
- ✅ Price calculation: weight × price_per_kg
- ✅ Sequence numbering working
- ✅ Status transitions validated
- ✅ Data constraints working (weight, quantity, date)

### Database Verification
```sql
-- Verified fields exist
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'cyclex_request';

-- Verified QR code uniqueness
SELECT COUNT(DISTINCT qr_code) = COUNT(*) FROM cyclex_request;
```

---

## 📝 Code Quality

### Imports Added
```python
from odoo.exceptions import ValidationError
import uuid
from datetime import datetime
```

### Documentation
- ✅ All methods have docstrings
- ✅ Complex logic commented
- ✅ Field help text provided
- ✅ TODO comments for future features

### Best Practices
- ✅ Follows Odoo 18 conventions
- ✅ Proper use of @api decorators
- ✅ Validation constraints
- ✅ Transaction safety
- ✅ No deprecated code

---

## 🔐 Security

### Access Control
- Security groups defined (customer, collector, manager, admin)
- Model access configured in `ir.model.access.csv`
- Record rules to be added in Phase 2

### Data Integrity
- Foreign key constraints
- Required field validation
- Status transition validation
- Date validation

---

## 🚀 Next Steps (Checkpoint 1.5)

The request model is now complete and ready for wallet integration:

1. **Wallet System**
   - Create wallet transactions on collection
   - Track customer earnings
   - Handle withdrawals

2. **Commission System** (Checkpoint 1.7)
   - Calculate collector commissions
   - Track payments

3. **Notifications** (Phase 3)
   - Implement FCM push notifications
   - Send status updates to users

4. **Mobile API** (Phase 3)
   - REST endpoints for request CRUD
   - QR code scanning
   - Photo uploads

---

## 📊 Statistics

| Metric | Value |
|--------|-------|
| Total Fields | 24 |
| Business Methods | 4 |
| Validators | 3 |
| Status States | 5 |
| Photo Fields | 2 |
| Auto-generated Fields | 3 |

---

## 🎯 Status

**Checkpoint 1.4: COMPLETED** ✅

The Request/Order model is fully functional with:
- Complete data structure
- Automatic QR code generation
- GPS location integration
- Price calculation
- Status workflow
- Data validation
- Business logic methods

**Ready for:** Checkpoint 1.5 - Core Models - Wallet System

---

## 📝 Notes

- QR codes use UUID v4 for guaranteed uniqueness
- GPS coordinates use 7 decimal places for ~1cm accuracy
- Price calculation is automatic and stored for performance
- Status workflow enforces business rules
- All database changes are backward compatible
- Ready for mobile app integration

---

**Module Version:** 18.0.1.0.0  
**Odoo Version:** 18.0  
**Database:** cyclex_db  
**Server:** Running on http://localhost:10018

