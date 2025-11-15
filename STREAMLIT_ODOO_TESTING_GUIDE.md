# 🧪 Streamlit → Odoo Testing Guide

## Overview
This guide explains how to test the CycleX app from Streamlit and verify the results in Odoo.

---

## 🔧 Setup

### 1. Enable Real API Mode
In `streamlit_app.py`, line 23:
```python
USE_DEMO_DATA = False  # Change from True to False
```

### 2. Restart Streamlit
```bash
pkill -f streamlit
cd /home/sabry3/edu_demo/custom_addons/cyclex
python3 -m streamlit run streamlit_app.py --server.port 8501
```

### 3. Ensure Odoo is Running
- Odoo should be running on `http://localhost:8025`
- Database: `automatic_error_reporter`
- Module `cyclex` should be installed and upgraded

---

## 📋 Testing Scenarios

### 1. User Registration & Verification

#### In Streamlit:
1. Go to **Sign Up** screen
2. Fill the form:
   - Name: "Test User"
   - Phone: "01012345678"
   - Password: "test123"
   - Role: Customer
3. Click **Sign Up**

#### Check in Odoo:
1. Go to **Contacts** (`/web#action=contacts.action_contacts`)
2. Search for phone: `01012345678`
3. Open the contact record
4. Verify:
   - ✅ `is_cyclex_user` = True
   - ✅ `cyclex_user_type` = "customer"
   - ✅ `phone_verified` = False (before OTP verification)
   - ✅ `account_status` = "pending" or "active"
   - ✅ Check `verification_code` field (for OTP)

#### In Streamlit (OTP Verification):
1. Go to **Verify OTP** screen
2. Enter the OTP code (check Odoo contact record)
3. Click **Verify**

#### Check in Odoo:
1. Refresh the contact record
2. Verify:
   - ✅ `phone_verified` = True
   - ✅ `account_status` = "active"

---

### 2. User Login

#### In Streamlit:
1. Go to **Login** screen
2. Enter:
   - Phone: `01012345678`
   - Password: `test123`
3. Click **Login**

#### Check in Odoo:
1. Go to **Contacts** → Search phone
2. Verify:
   - ✅ `last_login_date` is updated
   - ✅ User can access Odoo (if user account exists)

---

### 3. Create Order/Request

#### In Streamlit:
1. Login as Customer
2. Go to **Create Order** tab
3. Fill form:
   - Category ID: 8 (or any valid category)
   - Quantity: 5
   - Weight: 2.5 kg
   - Pickup Date: Select a date
   - Item Name: "Mixed plastic bottles"
4. Click **Create Order**

#### Check in Odoo:
1. Go to **CycleX** → **Requests** (or search model: `cyclex.request`)
2. Find the new request
3. Verify:
   - ✅ `customer_id` = Your test user
   - ✅ `status` = "pending"
   - ✅ `total_amount` is calculated
   - ✅ `pickup_date` matches
   - ✅ Items are created

**Odoo Menu Path:**
```
Apps → Search "CycleX" → Requests
```

---

### 4. View Categories & Products

#### In Streamlit:
1. Go to **Categories** tab
2. Click **Load**
3. View categories list

#### Check in Odoo:
1. Go to **CycleX** → **Categories** (model: `cyclex.category`)
2. Compare categories shown in Streamlit
3. Verify:
   - ✅ Category names match
   - ✅ Product counts are correct

---

### 5. View Orders/Requests

#### In Streamlit:
1. Go to **My Orders** tab
2. Click **Load**
3. View orders list

#### Check in Odoo:
1. Go to **CycleX** → **Requests**
2. Filter by customer (your test user)
3. Compare:
   - ✅ Order IDs match
   - ✅ Status matches
   - ✅ Amounts match
   - ✅ Dates match

---

### 6. Wallet & Transactions

#### In Streamlit:
1. Go to **Wallet** tab (from sidebar)
2. Click **Load**
3. View balance and transactions

#### Check in Odoo:
1. Go to **Contacts** → Your test user
2. Check:
   - ✅ `wallet_balance` field
   - ✅ Related `cyclex.transaction` records
3. Or go to **CycleX** → **Transactions**
4. Filter by partner (your test user)
5. Verify:
   - ✅ Transaction amounts
   - ✅ Transaction types (credit/debit)
   - ✅ Dates

---

### 7. Collector - Accept Order

#### In Streamlit:
1. Login as Collector
2. Go to **Available Orders** tab
3. Click **Load Orders**
4. Click **Accept** on an order

#### Check in Odoo:
1. Go to **CycleX** → **Requests**
2. Find the accepted order
3. Verify:
   - ✅ `status` = "assigned"
   - ✅ `collector_id` = Your collector user
   - ✅ `assigned_date` is set

---

## 🔍 Odoo Debugging Tips

### View API Logs
1. Enable Developer Mode in Odoo
2. Go to **Settings** → **Technical** → **Logging**
3. Check logs for API calls

### Check Database Directly
```sql
-- View all CycleX users
SELECT name, phone, cyclex_user_type, phone_verified, account_status 
FROM res_partner 
WHERE is_cyclex_user = true;

-- View requests
SELECT id, customer_id, status, total_amount, pickup_date 
FROM cyclex_request 
ORDER BY create_date DESC 
LIMIT 10;

-- View transactions
SELECT id, partner_id, type, amount, date 
FROM cyclex_transaction 
ORDER BY date DESC 
LIMIT 10;
```

### Enable Odoo Debug Mode
In Odoo config (`/home/sabry3/edu_demo/odoo.conf/odoo.conf`):
```ini
[options]
log_level = debug
log_handler = :DEBUG
```

---

## 📊 Testing Checklist

### Authentication
- [ ] Sign Up creates user in Odoo
- [ ] OTP verification updates `phone_verified`
- [ ] Login updates `last_login_date`
- [ ] Login fails with wrong credentials

### Orders/Requests
- [ ] Create order creates request in Odoo
- [ ] Order status is correct
- [ ] Order amounts are calculated
- [ ] Order items are saved

### Categories & Products
- [ ] Categories match Odoo data
- [ ] Product counts are accurate
- [ ] Language switching works

### Wallet
- [ ] Balance matches Odoo
- [ ] Transactions are recorded
- [ ] Transaction history is correct

### Collector
- [ ] Available orders match Odoo
- [ ] Accept order updates status
- [ ] Reject order works correctly

---

## 🐛 Common Issues

### Issue: Data not appearing in Odoo
**Solution:**
- Check if `USE_DEMO_DATA = False`
- Verify Odoo module is upgraded
- Check Odoo logs for errors
- Verify API endpoint is correct

### Issue: Login fails
**Solution:**
- Check user exists in Odoo
- Verify `phone_verified = True`
- Check `account_status = 'active'`
- Verify password in Odoo user account

### Issue: Orders not created
**Solution:**
- Check Odoo logs
- Verify category/product IDs exist
- Check request model permissions
- Verify API endpoint is working

---

## 🔗 Quick Links

- **Odoo URL:** http://localhost:8025
- **Streamlit URL:** http://localhost:8501
- **Odoo Database:** `automatic_error_reporter`
- **API Base:** http://localhost:8025/api/cyclex

---

## 📝 Notes

- Always test with `USE_DEMO_DATA = False` for real Odoo testing
- Use demo data (`USE_DEMO_DATA = True`) for UI/UX testing only
- Check Odoo logs if something doesn't work
- Use Odoo's Developer Mode for detailed debugging

---

**Happy Testing!** 🎉

