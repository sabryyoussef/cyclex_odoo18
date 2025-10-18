# CycleX Database Schema Documentation 🗄️

**Complete database structure and Entity Relationship Diagram**

**Version:** 1.0  
**Date:** October 2025  
**Odoo Version:** 18

---

## 📊 Database Overview

### Models Count: 7

1. `res.partner` (Extended) - Users (Customers & Collectors)
2. `cyclex.category` - Recycling Categories
3. `cyclex.product` - Recyclable Products
4. `cyclex.working.area` - Geographic Service Areas
5. `cyclex.request` - Recycling Requests/Orders
6. `cyclex.wallet` - Customer Wallets
7. `cyclex.wallet.transaction` - Wallet Transactions
8. `cyclex.commission` - Collector Commissions

---

## 🔗 Entity Relationship Diagram (ERD)

```
┌─────────────────────────────────────────────────────────────────────┐
│                       CycleX Database Schema                         │
└─────────────────────────────────────────────────────────────────────┘

┌──────────────────────┐
│   res.partner        │  (Extended Model)
├──────────────────────┤
│ PK id                │
│    name              │
│    phone  (unique)   │
│    email             │
│    is_cyclex_user    │─────┐
│    cyclex_user_type  │     │
│    phone_verified    │     │
│    collector_verified│     │
│    commission_rate   │     │
│    fcm_token         │     │
│    language          │     │
│    verification_code │     │
└──────────────────────┘     │
         │                    │
         │ 1:1               │ 1:N
         ▼                    ▼
┌──────────────────────┐  ┌──────────────────────┐
│  cyclex.wallet       │  │ cyclex.request       │
├──────────────────────┤  ├──────────────────────┤
│ PK id                │  │ PK id                │
│ FK partner_id    ────┼──┤ FK customer_id   ────┤
│    current_balance   │  │ FK collector_id  ────┤
│    total_credits     │  │ FK product_id        │
│    total_debits      │  │ FK category_id       │
│    transaction_count │  │    name              │
│    currency_id       │  │    quantity          │
└──────────────────────┘  │    unit              │
         │                │    calculated_price  │
         │ 1:N            │    status            │
         ▼                │    pickup_date       │
┌──────────────────────┐  │    pickup_time       │
│cyclex.wallet.transaction│location_latitude    │
├──────────────────────┤  │    location_longitude│
│ PK id                │  │    address           │
│ FK wallet_id     ────┤  │    notes             │
│ FK request_id        │  │    qr_code   (unique)│
│    amount            │  │    qr_code_image     │
│    transaction_type  │  │    collection_date   │
│    description       │  │    rating            │
│    reference         │  │    comments          │
│    withdrawal_status │  │    image             │
│    approved_by       │  └──────────────────────┘
│    approval_date     │           │
│    rejection_reason  │           │ 1:1
└──────────────────────┘           ▼
                         ┌──────────────────────┐
                         │ cyclex.commission    │
                         ├──────────────────────┤
                         │ PK id                │
                         │ FK request_id    ────┤
                         │ FK collector_id      │
                         │    amount            │
                         │    commission_rate   │
┌──────────────────────┐ │    commission_amount │
│ cyclex.category      │ │    status            │
├──────────────────────┤ │    payment_date      │
│ PK id                │ └──────────────────────┘
│    name              │
│    name_ar           │
│    description       │           ▲
│    description_ar    │           │ N:1
│    image             │           │
│    parent_id         │  ┌──────────────────────┐
│    sequence          │  │ cyclex.product       │
└──────────────────────┘  ├──────────────────────┤
         │                │ PK id                │
         │ 1:N            │ FK category_id   ────┤
         └────────────────┼────────────────      │
                          │    name              │
                          │    name_ar           │
                          │    price_per_kg      │
                          │    unit_of_measure   │
┌──────────────────────┐  │    description       │
│cyclex.working.area   │  │    description_ar    │
├──────────────────────┤  │    image             │
│ PK id                │  └──────────────────────┘
│    name              │
│    name_ar           │
│    active            │
└──────────────────────┘
         ▲
         │ N:N
         │
    (Many-to-Many via res_partner_working_area_rel)
         │
         │
┌────────┴─────────────┐
│   res.partner        │
│  (collectors only)   │
│  working_area_ids    │
└──────────────────────┘
```

---

## 📋 Detailed Model Schemas

### 1. res.partner (Extended)

**Table Name:** `res_partner`

| Field | Type | Required | Unique | Description |
|-------|------|----------|--------|-------------|
| `id` | Integer | Yes | PK | Primary Key |
| `name` | Char | Yes | No | User full name |
| `phone` | Char | Yes* | Yes* | Phone number (unique for CycleX users) |
| `email` | Char | No | No | Email address |
| `is_cyclex_user` | Boolean | No | No | Is this a CycleX user? |
| `cyclex_user_type` | Selection | No | No | customer / collector |
| `phone_verified` | Boolean | No | No | Phone verification status |
| `verification_code` | Char | No | No | 6-digit SMS code |
| `verification_code_expiry` | Datetime | No | No | Code expiry (10 minutes) |
| `collector_verified` | Boolean | No | No | Admin approval (collectors only) |
| `commission_rate` | Float | No | No | % commission (default 15%) |
| `fcm_token` | Char | No | No | Firebase Cloud Messaging token |
| `language` | Selection | No | No | ar / en (default: ar) |
| `working_area_ids` | Many2many | No | No | Collector working areas (max 5) |
| `wallet_id` | One2many | No | No | Customer wallet (auto-created) |
| `request_ids` | One2many | No | No | Customer requests |
| `collector_request_ids` | One2many | No | No | Assigned requests (collector) |
| `commission_ids` | One2many | No | No | Commissions earned (collector) |

**Indexes:**
- `phone` (unique constraint for CycleX users)
- `cyclex_user_type`
- `phone_verified`
- `collector_verified`

**Constraints:**
- Egyptian phone format: `^(\+20|0)(1[0-2,5])\d{8}$`
- No duplicate phones for CycleX users
- Max 5 working areas per collector

---

### 2. cyclex.category

**Table Name:** `cyclex_category`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | Integer | Yes (PK) | Primary Key |
| `name` | Char | Yes | Category name (English) |
| `name_ar` | Char | No | Category name (Arabic) |
| `description` | Text | No | Category description (English) |
| `description_ar` | Text | No | Category description (Arabic) |
| `image` | Binary | No | Category image |
| `parent_id` | Many2one | No | Parent category (hierarchical) |
| `child_ids` | One2many | No | Sub-categories |
| `product_ids` | One2many | No | Products in this category |
| `sequence` | Integer | No | Display order |
| `active` | Boolean | No | Is active? (default: True) |

**Indexes:**
- `parent_id`
- `sequence`
- `active`

**Sample Data:**
- Plastic (بلاستيك)
- Paper & Cardboard (ورق وكرتون)
- Metal (معادن)
- Glass (زجاج)
- Electronics (إلكترونيات)

---

### 3. cyclex.product

**Table Name:** `cyclex_product`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | Integer | Yes (PK) | Primary Key |
| `name` | Char | Yes | Product name (English) |
| `name_ar` | Char | No | Product name (Arabic) |
| `category_id` | Many2one | Yes | Category (cyclex.category) |
| `price_per_kg` | Float | Yes | Price in EGP per unit |
| `unit_of_measure` | Selection | Yes | kg / unit / ton |
| `description` | Text | No | Product description (English) |
| `description_ar` | Text | No | Product description (Arabic) |
| `image` | Binary | No | Product image |
| `active` | Boolean | No | Is active? (default: True) |

**Indexes:**
- `category_id`
- `active`

**Sample Products:**
- Plastic Bottles: 3.50 EGP/kg
- Cardboard: 2.50 EGP/kg
- Aluminum Cans: 8.00 EGP/kg
- Mobile Phones: 50.00 EGP/unit

---

### 4. cyclex.working.area

**Table Name:** `cyclex_working_area`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | Integer | Yes (PK) | Primary Key |
| `name` | Char | Yes | Area name (English) |
| `name_ar` | Char | No | Area name (Arabic) |
| `active` | Boolean | No | Is active? (default: True) |
| `collector_ids` | Many2many | No | Collectors serving this area |

**Indexes:**
- `active`

**Sample Areas:**
- Nasr City (مدينة نصر)
- Maadi (المعادي)
- Heliopolis (مصر الجديدة)

---

### 5. cyclex.request

**Table Name:** `cyclex_request`

| Field | Type | Required | Computed | Description |
|-------|------|----------|----------|-------------|
| `id` | Integer | Yes (PK) | No | Primary Key |
| `name` | Char | Auto | No | Request number (REQ-00001) |
| `customer_id` | Many2one | Yes | No | Customer (res.partner) |
| `collector_id` | Many2one | No | No | Assigned collector |
| `product_id` | Many2one | Yes | No | Product (cyclex.product) |
| `category_id` | Many2one | Yes | No | Category (cyclex.category) |
| `quantity` | Float | Yes | No | Quantity |
| `unit` | Selection | Yes | No | kg / unit / ton |
| `calculated_price` | Float | No | Yes | quantity × price_per_kg |
| `currency_id` | Many2one | No | No | Currency (default: EGP) |
| `status` | Selection | No | No | pending/assigned/collected/cancelled |
| `pickup_date` | Date | Yes | No | Requested pickup date |
| `pickup_time` | Selection | Yes | No | morning/afternoon/evening |
| `location_latitude` | Float | Yes | No | GPS latitude |
| `location_longitude` | Float | Yes | No | GPS longitude |
| `address` | Text | Yes | No | Pickup address |
| `notes` | Text | No | No | Special instructions |
| `qr_code` | Char | Auto | No | Unique QR code string |
| `qr_code_image` | Binary | Auto | No | QR code PNG image |
| `collection_date` | Datetime | No | No | When collected |
| `rating` | Selection | No | No | 1-5 stars |
| `comments` | Text | No | No | Customer feedback |
| `image` | Binary | No | No | Item photo (max 5MB) |

**Indexes:**
- `customer_id`
- `collector_id`
- `product_id`
- `status`
- `qr_code` (unique)
- `pickup_date`

**Constraints:**
- `qr_code` must be unique
- Image size ≤ 5MB
- Pickup date ≥ today

**Status Workflow:**
```
draft → pending → assigned → collected
                      ↓
                  cancelled
```

---

### 6. cyclex.wallet

**Table Name:** `cyclex_wallet`

| Field | Type | Required | Computed | Description |
|-------|------|----------|----------|-------------|
| `id` | Integer | Yes (PK) | No | Primary Key |
| `partner_id` | Many2one | Yes | No | Customer (res.partner) |
| `current_balance` | Float | No | Yes | total_credits - total_debits |
| `total_credits` | Float | No | Yes | Sum of all credit transactions |
| `total_debits` | Float | No | Yes | Sum of all debit transactions |
| `transaction_count` | Integer | No | Yes | Count of transactions |
| `transaction_ids` | One2many | No | No | All transactions |
| `currency_id` | Many2one | No | No | Currency (default: EGP) |

**Indexes:**
- `partner_id` (unique - one wallet per customer)

**Computed Fields:**
- `current_balance` = SUM(credits) - SUM(debits)
- `total_credits` = SUM(transaction_ids WHERE type='credit')
- `total_debits` = SUM(transaction_ids WHERE type='debit')
- `transaction_count` = COUNT(transaction_ids)

---

### 7. cyclex.wallet.transaction

**Table Name:** `cyclex_wallet_transaction`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | Integer | Yes (PK) | Primary Key |
| `wallet_id` | Many2one | Yes | Wallet (cyclex.wallet) |
| `request_id` | Many2one | No | Related request (if any) |
| `amount` | Float | Yes | Transaction amount |
| `transaction_type` | Selection | Yes | credit / debit |
| `description` | Text | Yes | Transaction description |
| `reference` | Char | No | Reference number |
| `transaction_date` | Datetime | Auto | No | When created |
| `withdrawal_status` | Selection | No | pending/approved/rejected (debits only) |
| `approved_by` | Many2one | No | Admin who approved |
| `approval_date` | Datetime | No | When approved |
| `rejection_reason` | Text | No | Why rejected |

**Indexes:**
- `wallet_id`
- `request_id`
- `transaction_type`
- `withdrawal_status`
- `transaction_date`

**Constraints:**
- Amount must be > 0
- Withdrawal (debit) requires approval

---

### 8. cyclex.commission

**Table Name:** `cyclex_commission`

| Field | Type | Required | Computed | Description |
|-------|------|----------|----------|-------------|
| `id` | Integer | Yes (PK) | No | Primary Key |
| `request_id` | Many2one | Yes | No | Request (cyclex.request) |
| `collector_id` | Many2one | Yes | No | Collector (res.partner) |
| `amount` | Float | Yes | No | Request total price |
| `commission_rate` | Float | Yes | No | Commission % (from collector) |
| `commission_amount` | Float | No | Yes | amount × rate / 100 |
| `status` | Selection | No | No | earned / paid |
| `payment_date` | Datetime | No | No | When paid to collector |
| `currency_id` | Many2one | No | No | Currency (default: EGP) |

**Indexes:**
- `request_id` (unique - one commission per request)
- `collector_id`
- `status`

**Computed Fields:**
- `commission_amount` = `amount` × `commission_rate` / 100

---

## 🔗 Relationships Summary

### One-to-One (1:1)
- `res.partner` → `cyclex.wallet` (Customer has one wallet)
- `cyclex.request` → `cyclex.commission` (Request has one commission)

### One-to-Many (1:N)
- `res.partner` → `cyclex.request` (Customer has many requests)
- `res.partner` → `cyclex.request` (Collector handles many requests)
- `cyclex.category` → `cyclex.product` (Category has many products)
- `cyclex.category` → `cyclex.category` (Parent → Children)
- `cyclex.wallet` → `cyclex.wallet.transaction` (Wallet has many transactions)
- `res.partner` → `cyclex.commission` (Collector has many commissions)

### Many-to-Many (N:N)
- `res.partner` ↔ `cyclex.working.area` (Collectors serve multiple areas)

---

## 📊 Database Statistics (With Sample Data)

```sql
-- Check record counts
SELECT 'Categories' as model, COUNT(*) FROM cyclex_category
UNION ALL
SELECT 'Products', COUNT(*) FROM cyclex_product
UNION ALL
SELECT 'Working Areas', COUNT(*) FROM cyclex_working_area
UNION ALL
SELECT 'Customers', COUNT(*) FROM res_partner WHERE cyclex_user_type = 'customer'
UNION ALL
SELECT 'Collectors', COUNT(*) FROM res_partner WHERE cyclex_user_type = 'collector'
UNION ALL
SELECT 'Requests', COUNT(*) FROM cyclex_request
UNION ALL
SELECT 'Wallets', COUNT(*) FROM cyclex_wallet
UNION ALL
SELECT 'Transactions', COUNT(*) FROM cyclex_wallet_transaction
UNION ALL
SELECT 'Commissions', COUNT(*) FROM cyclex_commission;
```

**Expected Results (With Sample Data):**
- Categories: 5
- Products: 11
- Working Areas: 5
- Customers: 3
- Collectors: 3
- Requests: 0 (created via API/testing)
- Wallets: 6 (auto-created for users)
- Transactions: 0 (created when orders complete)
- Commissions: 0 (created when orders complete)

---

## 🔍 Common Queries

### Get Customer with Wallet Balance

```sql
SELECT 
    p.id,
    p.name,
    p.phone,
    w.current_balance,
    w.transaction_count,
    COUNT(r.id) as total_requests
FROM res_partner p
LEFT JOIN cyclex_wallet w ON w.partner_id = p.id
LEFT JOIN cyclex_request r ON r.customer_id = p.id
WHERE p.cyclex_user_type = 'customer'
GROUP BY p.id, p.name, p.phone, w.current_balance, w.transaction_count;
```

---

### Get Collector Performance

```sql
SELECT 
    p.id,
    p.name,
    p.phone,
    p.commission_rate,
    COUNT(r.id) as completed_orders,
    SUM(c.commission_amount) as total_earned
FROM res_partner p
LEFT JOIN cyclex_request r ON r.collector_id = p.id AND r.status = 'collected'
LEFT JOIN cyclex_commission c ON c.collector_id = p.id
WHERE p.cyclex_user_type = 'collector'
GROUP BY p.id, p.name, p.phone, p.commission_rate;
```

---

### Get Pending Orders by Area

```sql
SELECT 
    r.id,
    r.name as request_number,
    r.calculated_price,
    r.pickup_date,
    p.name as customer,
    prod.name as product,
    wa.name as area
FROM cyclex_request r
JOIN res_partner p ON r.customer_id = p.id
JOIN cyclex_product prod ON r.product_id = prod.id
LEFT JOIN cyclex_working_area wa ON wa.id IN (
    -- This would need proper join via collector's areas
    SELECT working_area_id FROM res_partner_cyclex_working_area_rel 
    WHERE partner_id = 10  -- Specific collector
)
WHERE r.status = 'pending';
```

---

### Get Wallet Transaction History

```sql
SELECT 
    wt.id,
    wt.transaction_date,
    wt.transaction_type,
    wt.amount,
    wt.description,
    wt.withdrawal_status,
    r.name as request_number
FROM cyclex_wallet_transaction wt
JOIN cyclex_wallet w ON wt.wallet_id = w.id
LEFT JOIN cyclex_request r ON wt.request_id = r.id
WHERE w.partner_id = 5  -- Specific customer
ORDER BY wt.transaction_date DESC;
```

---

## 🎯 Key Business Rules (Reflected in Schema)

### 1. User Management
- ✅ One wallet per customer (1:1)
- ✅ Unique phone numbers for CycleX users
- ✅ Collectors need admin verification
- ✅ Max 5 working areas per collector

### 2. Request Lifecycle
- ✅ QR code auto-generated (unique)
- ✅ Calculated price = quantity × product price
- ✅ Status workflow enforced
- ✅ Only collected orders can be rated

### 3. Financial Rules
- ✅ Wallet balance = credits - debits (computed)
- ✅ Auto-credit on order completion
- ✅ Withdrawals require admin approval
- ✅ Commission auto-calculated (price × rate)

### 4. Geographic Rules
- ✅ Collectors serve specific areas
- ✅ Only see orders in their areas
- ✅ Max 5 areas per collector

---

## 🔐 Security & Access Control

### Security Groups:

1. **CycleX User** (`group_cyclex_user`)
   - Read: Own data only
   - Create: Own requests
   - Update: Own profile
   - Delete: No

2. **CycleX Manager** (`group_cyclex_manager`)
   - Read: All data
   - Create: Categories, products, areas
   - Update: All records except commissions
   - Delete: Soft delete (archive)

3. **CycleX Admin** (`group_cyclex_admin`)
   - Full access to all models
   - Approve/reject withdrawals
   - Verify collectors
   - Manage system parameters

---

## 📈 Database Performance Considerations

### Indexes Created:
- ✅ Phone number (unique for CycleX users)
- ✅ Status fields (for filtering)
- ✅ Foreign keys (for joins)
- ✅ QR codes (for fast lookups)
- ✅ Dates (for cron jobs)

### Suggested Additional Indexes (Production):
```sql
-- For faster API queries
CREATE INDEX idx_request_status_pickup ON cyclex_request(status, pickup_date);
CREATE INDEX idx_transaction_wallet_type ON cyclex_wallet_transaction(wallet_id, transaction_type);
CREATE INDEX idx_commission_collector_status ON cyclex_commission(collector_id, status);
```

---

## 🔄 Data Flow Diagram

### Complete Order Flow:

```
Customer Creates Request
         ↓
    [cyclex.request] created
         ↓ (auto)
    qr_code generated
         ↓
    Status: pending
         ↓
Collector Accepts Order
         ↓
    Status: assigned
    collector_id set
         ↓
Collector Scans QR Code
         ↓
    Status: collected
         ↓ (auto)
    [cyclex.wallet.transaction] created (credit)
         ↓ (auto)
    Wallet balance updated
         ↓ (auto)
    [cyclex.commission] created
         ↓
    Commission amount calculated
         ↓
Order Complete ✅
```

---

## 📝 Schema Version History

### Version 1.0 (October 2025)
- Initial schema design
- 8 models created
- Relationships established
- Constraints implemented
- Sample data structure

### Future Considerations (v2.0):
- [ ] Audit log table (track all changes)
- [ ] SMS log table (track SMS sending)
- [ ] Notification log table (track push notifications)
- [ ] Payment transactions (actual money transfers)
- [ ] Collector ratings (customers rate collectors)

---

## 🛠️ Database Maintenance

### Backup Recommendations:
```bash
# Daily backup
pg_dump cyclex_db > cyclex_backup_$(date +%Y%m%d).sql

# Backup with compression
pg_dump cyclex_db | gzip > cyclex_backup_$(date +%Y%m%d).sql.gz
```

### Cleanup Queries:
```sql
-- Archive old collected orders (6+ months)
UPDATE cyclex_request 
SET active = False 
WHERE status = 'collected' 
  AND collection_date < NOW() - INTERVAL '6 months';

-- Archive old transactions (1+ year)
UPDATE cyclex_wallet_transaction 
SET active = False 
WHERE transaction_date < NOW() - INTERVAL '1 year';
```

---

## 📚 Additional Resources

- **Odoo ORM Documentation:** https://www.odoo.com/documentation/18.0/developer/reference/backend/orm.html
- **PostgreSQL Documentation:** https://www.postgresql.org/docs/
- **API Documentation:** See `API_DOCUMENTATION.md`
- **Sample Data:** See `docs/SAMPLE_DATA_GUIDE.md`

---

**Last Updated:** October 17, 2025  
**Maintained By:** CycleX Development Team

