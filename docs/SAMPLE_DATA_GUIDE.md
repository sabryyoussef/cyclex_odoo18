# CycleX Sample Data Guide 📊

**Complete reference for test data in the CycleX system**

---

## 🎯 Overview

The sample data file (`cyclex_sample_data.xml`) populates your Odoo database with realistic test data including:

- **5 Working Areas** (Cairo districts)
- **5 Categories** (Plastic, Paper, Metal, Glass, Electronics)
- **11 Products** (Various recyclable items with prices)
- **3 Test Customers** (With verified accounts)
- **3 Test Collectors** (With verified accounts and working areas)
- **Auto-created Wallets** (For all customers and collectors)

---

## 📍 Working Areas

### Complete List:

| ID | Name | Arabic Name | Description |
|----|------|-------------|-------------|
| 1 | Nasr City | مدينة نصر | Eastern Cairo district |
| 2 | Maadi | المعادي | Southern Cairo district |
| 3 | Heliopolis | مصر الجديدة | North-eastern Cairo district |
| 4 | Zamalek | الزمالك | Nile island district |
| 5 | Downtown Cairo | وسط البلد | Central Cairo |

**Usage in Postman:**
- These working areas are linked to collectors
- Collectors can only see orders in their assigned areas

---

## 📦 Categories & Products

### 1. Plastic (بلاستيك)

| Product | Arabic Name | Price/Unit | Unit | Product ID |
|---------|-------------|------------|------|-----------|
| Plastic Bottles (PET) | زجاجات بلاستيك | 3.50 EGP | kg | 1 |
| Plastic Bags | أكياس بلاستيك | 2.00 EGP | kg | 2 |
| Plastic Containers | حاويات بلاستيك | 4.00 EGP | kg | 3 |

**Test Scenario:**
```json
{
    "product_id": 1,
    "quantity": 10.5,
    "unit": "kg"
}
// Expected price: 10.5 × 3.50 = 36.75 EGP
```

---

### 2. Paper & Cardboard (ورق وكرتون)

| Product | Arabic Name | Price/Unit | Unit | Product ID |
|---------|-------------|------------|------|-----------|
| Newspapers | جرائد | 1.50 EGP | kg | 4 |
| Cardboard Boxes | صناديق كرتون | 2.50 EGP | kg | 5 |
| Office Paper | ورق مكتبي | 3.00 EGP | kg | 6 |

**Test Scenario:**
```json
{
    "product_id": 5,
    "quantity": 20.0,
    "unit": "kg"
}
// Expected price: 20.0 × 2.50 = 50.00 EGP
```

---

### 3. Metal (معادن)

| Product | Arabic Name | Price/Unit | Unit | Product ID |
|---------|-------------|------------|------|-----------|
| Aluminum Cans | علب ألومنيوم | 8.00 EGP | kg | 7 |
| Scrap Metal | خردة معادن | 5.00 EGP | kg | 8 |

**Test Scenario:**
```json
{
    "product_id": 7,
    "quantity": 5.0,
    "unit": "kg"
}
// Expected price: 5.0 × 8.00 = 40.00 EGP
```

---

### 4. Glass (زجاج)

| Product | Arabic Name | Price/Unit | Unit | Product ID |
|---------|-------------|------------|------|-----------|
| Glass Bottles | زجاجات زجاجية | 1.00 EGP | kg | 9 |

**Test Scenario:**
```json
{
    "product_id": 9,
    "quantity": 15.0,
    "unit": "kg"
}
// Expected price: 15.0 × 1.00 = 15.00 EGP
```

---

### 5. Electronics (إلكترونيات)

| Product | Arabic Name | Price/Unit | Unit | Product ID |
|---------|-------------|------------|------|-----------|
| Old Mobile Phones | هواتف محمولة قديمة | 50.00 EGP | unit | 10 |
| Computer Parts | قطع كمبيوتر | 30.00 EGP | kg | 11 |

**Test Scenario:**
```json
{
    "product_id": 10,
    "quantity": 3,
    "unit": "unit"
}
// Expected price: 3 × 50.00 = 150.00 EGP
```

---

## 👥 Test Users

### Customers

#### Customer 1: Ahmed Hassan
```
Phone: +201001234567
Password: TestPass123 (set after import)
Email: ahmed.hassan@example.com
Language: Arabic (ar)
Location: 15 El Nasr Street, Nasr City
Status: Verified ✅
```

**Postman Usage:**
```json
{
    "phone": "+201001234567",
    "password": "TestPass123"
}
```

---

#### Customer 2: Fatma Mohamed
```
Phone: +201002345678
Password: TestPass123 (set after import)
Email: fatma.mohamed@example.com
Language: Arabic (ar)
Location: 22 Road 9, Maadi
Status: Verified ✅
```

**Postman Usage:**
```json
{
    "phone": "+201002345678",
    "password": "TestPass123"
}
```

---

#### Customer 3: Omar Ali
```
Phone: +201003456789
Password: TestPass123 (set after import)
Email: omar.ali@example.com
Language: English (en)
Location: 10 Merghany Street, Heliopolis
Status: Verified ✅
```

**Postman Usage:**
```json
{
    "phone": "+201003456789",
    "password": "TestPass123"
}
```

---

### Collectors

#### Collector 1: Mahmoud Saad
```
Phone: +201101234567
Password: TestPass123 (set after import)
Email: mahmoud.saad@example.com
Language: Arabic (ar)
Location: 5 Abbas El Akkad, Nasr City
Working Areas: Nasr City, Heliopolis
Commission Rate: 15%
Status: Verified ✅
```

**Postman Usage:**
```json
{
    "phone": "+201101234567",
    "password": "TestPass123"
}
```

**Will see orders from:** Nasr City, Heliopolis

---

#### Collector 2: Khaled Ibrahim
```
Phone: +201102345678
Password: TestPass123 (set after import)
Email: khaled.ibrahim@example.com
Language: Arabic (ar)
Location: 12 Road 218, Maadi
Working Areas: Maadi, Zamalek
Commission Rate: 15%
Status: Verified ✅
```

**Postman Usage:**
```json
{
    "phone": "+201102345678",
    "password": "TestPass123"
}
```

**Will see orders from:** Maadi, Zamalek

---

#### Collector 3: Hassan Youssef
```
Phone: +201103456789
Password: TestPass123 (set after import)
Email: hassan.youssef@example.com
Language: Arabic (ar)
Location: 8 26th July Street, Zamalek
Working Areas: Downtown Cairo, Zamalek
Commission Rate: 15%
Status: Verified ✅
```

**Postman Usage:**
```json
{
    "phone": "+201103456789",
    "password": "TestPass123"
}
```

**Will see orders from:** Downtown Cairo, Zamalek

---

## 🔧 Setup Instructions

### Step 1: Install/Upgrade Module

```bash
# Make sure Odoo is running
cd /media/sabry3/sabry_backup/cycle_x/odoo18

# Upgrade the module to load sample data
python odoo-bin -c ../odoo_conf/odoo.conf -u cyclex -d cyclex_db
```

### Step 2: Set Passwords

After importing, you need to set passwords for test users in Odoo:

1. Go to **CycleX → Customers** or **CycleX → Collectors**
2. Open each user
3. Click "Action" → "Change Password"
4. Set password to: `TestPass123`

**Or use SQL (faster):**
```sql
-- This would need to be done manually in Odoo or via registration API
-- Passwords are hashed, so can't be set directly
```

**Recommended:** Use the registration API to create passwords:
- Call `/api/cyclex/register` for each user
- OR manually set passwords in Odoo backend

---

### Step 3: Verify Sample Data

**In Odoo Backend:**
1. Go to **CycleX → Categories** - Should see 5 categories
2. Go to **CycleX → Products** - Should see 11 products
3. Go to **CycleX → Working Areas** - Should see 5 areas
4. Go to **CycleX → Customers** - Should see 3 customers
5. Go to **CycleX → Collectors** - Should see 3 collectors (verified)

**Via API (Postman):**
```http
POST /api/cyclex/categories
{
    "jsonrpc": "2.0",
    "method": "call",
    "params": {},
    "id": 1
}
```

Should return 5 categories.

---

## 🧪 Testing Scenarios

### Scenario 1: Complete Customer Journey

**1. Login as Customer:**
```json
POST /api/cyclex/login
{
    "phone": "+201001234567",
    "password": "TestPass123"
}
```

**2. Get Categories:**
```json
POST /api/cyclex/categories
{
    "language": "ar"
}
```

**3. Get Products (Plastic):**
```json
POST /api/cyclex/products
{
    "category_id": 1,
    "language": "ar"
}
```

**4. Create Request:**
```json
POST /api/cyclex/request/create
{
    "product_id": 1,
    "quantity": 10.5,
    "unit": "kg",
    "pickup_date": "2025-10-25",
    "pickup_time": "morning",
    "location_latitude": 30.0444,
    "location_longitude": 31.2357,
    "address": "15 El Nasr Street, Nasr City",
    "notes": "Please call before arriving"
}
```

**Expected Result:**
- Request created ✅
- Status: pending
- Calculated price: 36.75 EGP (10.5 × 3.50)
- QR code generated
- Visible to collectors in Nasr City & Heliopolis

---

### Scenario 2: Complete Collector Journey

**1. Login as Collector:**
```json
POST /api/cyclex/login
{
    "phone": "+201101234567",
    "password": "TestPass123"
}
```

**2. View Available Orders:**
```json
POST /api/cyclex/collector/available-orders
{
    "limit": 10
}
```

**Expected:** Will see orders from Nasr City and Heliopolis only

**3. Accept Order:**
```json
POST /api/cyclex/collector/accept-order
{
    "request_id": 1
}
```

**4. Scan QR Code:**
```json
POST /api/cyclex/collector/scan-qr
{
    "qr_code": "CYCLEX-REQ-00001-abc123..."
}
```

**Expected Result:**
- Order marked as collected ✅
- Customer wallet credited: 36.75 EGP
- Collector commission created: 5.51 EGP (15% of 36.75)

---

### Scenario 3: Testing Working Areas

**Customer in Nasr City creates order:**
- Visible to: Collector 1 (Mahmoud Saad) ✅
- NOT visible to: Collector 2, 3 ❌

**Customer in Maadi creates order:**
- Visible to: Collector 2 (Khaled Ibrahim) ✅
- NOT visible to: Collector 1, 3 ❌

**Customer in Zamalek creates order:**
- Visible to: Collector 2 (Khaled) AND Collector 3 (Hassan) ✅
- NOT visible to: Collector 1 ❌

---

## 💰 Wallet Testing

### Check Wallet Balance

```json
POST /api/cyclex/wallet/balance
// After login as customer
```

### After Order Completion:

**Customer Wallet:**
```
Initial: 0.00 EGP
After Order: 36.75 EGP
Transaction Type: Credit
Description: "Payment for recycling request REQ-00001"
```

**Collector Commission:**
```
Amount: 5.51 EGP (15% of 36.75)
Status: Earned
Request: REQ-00001
```

---

## 📊 Price Calculations

### Formula:
```
Calculated Price = Quantity × Price per Unit
Commission = Calculated Price × Commission Rate (15%)
Customer Receives = Calculated Price (full amount)
Collector Earns = Commission
```

### Example Calculations:

| Product | Quantity | Price/Unit | Total Price | Commission (15%) |
|---------|----------|------------|-------------|------------------|
| Plastic Bottles | 10 kg | 3.50 EGP | 35.00 EGP | 5.25 EGP |
| Cardboard | 25 kg | 2.50 EGP | 62.50 EGP | 9.38 EGP |
| Aluminum Cans | 5 kg | 8.00 EGP | 40.00 EGP | 6.00 EGP |
| Mobile Phones | 3 units | 50.00 EGP | 150.00 EGP | 22.50 EGP |

---

## 🔍 Verifying Sample Data in Database

### Via Odoo Shell:

```python
# Start Odoo shell
cd /media/sabry3/sabry_backup/cycle_x/odoo18
python odoo-bin shell -c ../odoo_conf/odoo.conf -d cyclex_db

# Check categories
env['cyclex.category'].search([])
# Expected: 5 records

# Check products
env['cyclex.product'].search([])
# Expected: 11 records

# Check working areas
env['cyclex.working.area'].search([])
# Expected: 5 records

# Check customers
env['res.partner'].search([('cyclex_user_type', '=', 'customer')])
# Expected: 3 records

# Check collectors
env['res.partner'].search([('cyclex_user_type', '=', 'collector')])
# Expected: 3 records

# Check collector working areas
collector = env['res.partner'].search([('phone', '=', '+201101234567')])
collector.working_area_ids
# Expected: 2 areas (Nasr City, Heliopolis)
```

---

## 🎯 Quick Test Checklist

### Before Testing:
- [ ] Module installed/upgraded
- [ ] Sample data loaded (check Odoo backend)
- [ ] Passwords set for all test users
- [ ] Postman collection imported
- [ ] Odoo server running on port 10018

### Test Each Feature:
- [ ] Categories API returns 5 categories
- [ ] Products API returns products filtered by category
- [ ] Customer can create request
- [ ] QR code is generated
- [ ] Collector sees orders in their working areas only
- [ ] Collector can accept order
- [ ] QR scan completes order
- [ ] Wallet is credited
- [ ] Commission is calculated correctly

---

## 🚨 Common Issues

### Issue 1: Sample Data Not Loading

**Symptoms:** No categories, products, or users in backend

**Solution:**
```bash
# Reinstall with sample data
python odoo-bin -c ../odoo_conf/odoo.conf -i cyclex -d cyclex_db --stop-after-init
```

---

### Issue 2: Cannot Login with Test Users

**Symptoms:** `Invalid credentials` error

**Solution:**
- Passwords need to be set manually in Odoo backend
- OR use registration API to create proper password hashes
- Sample data only creates users, not passwords (security)

---

### Issue 3: Collector Doesn't See Orders

**Symptoms:** `available-orders` returns empty

**Solution:**
- Check collector's working areas match order location
- Verify collector is `collector_verified = True`
- Ensure order status is `pending`

---

## 📝 Summary

**Sample Data Includes:**
- ✅ 5 Working Areas (Cairo districts)
- ✅ 5 Categories (Plastic, Paper, Metal, Glass, Electronics)
- ✅ 11 Products (With realistic prices)
- ✅ 3 Customers (Verified, different locations)
- ✅ 3 Collectors (Verified, different working areas)
- ✅ Auto-created Wallets (For all users)

**You Need to Add:**
- ⚠️ Passwords (Set manually or via API)
- 📋 Sample Requests (Create via API or backend)
- 💰 Transactions (Created automatically when orders complete)

**Next Steps:**
1. Import sample data (upgrade module)
2. Set passwords for test users
3. Use Postman to test workflows
4. Create sample requests and complete them
5. Verify wallet transactions and commissions

---

**Ready to test! 🚀**

