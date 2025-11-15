# 🧪 Complete User Flow Test - Streamlit App

**Date**: November 13, 2025  
**Testing Environment**:
- Streamlit: http://localhost:8501
- Odoo API: http://localhost:8025/api/cyclex
- Database: `automatic_error_reporter`

---

## ✅ Pre-Test Checklist

- [x] Odoo running on port 8025
- [x] Streamlit running on port 8501
- [x] `USE_DEMO_DATA = False` in `streamlit_app.py`
- [x] Test OTP code: `123456`

---

## 🎬 Test Flow Sequence

### **Phase 1: Authentication Flow** 🔐

#### Test 1.1: New User Registration

**Steps:**
1. Open browser: http://localhost:8501
2. Click "📝 Don't have an account? Sign Up"
3. Fill registration form:
   - **Full Name**: `Flow Test User`
   - **Phone Number**: `01000222222` (new unique number)
   - **Password**: `Test1234`
   - **Confirm Password**: `Test1234`
   - **Email** (optional): `flowtest@test.com`
   - **Account Type**: Customer
   - ✓ Accept Terms & Conditions
4. Click "Sign Up"

**Expected Result:**
- ✅ Success message: "Account created! Please verify OTP."
- ✅ Screen changes to "Verify OTP"
- ✅ Shows "🧪 Test OTP Code: 123456"

**Actual Result:**
```
[ ] Success - works as expected
[ ] Failed - Error: _________________________
```

---

#### Test 1.2: OTP Verification

**Steps:**
1. On "Verify OTP" screen
2. Enter OTP: `123456`
3. Click "Verify"

**Expected Result:**
- ✅ Success message: "OTP verified! You can now login."
- ✅ Redirects to Login screen

**Actual Result:**
```
[ ] Success
[ ] Failed - Error: _________________________
```

---

#### Test 1.3: Login

**Steps:**
1. On Login screen
2. Enter credentials:
   - **Phone**: `01000222222`
   - **Password**: `Test1234`
3. Click "Login"

**Expected Result:**
- ✅ Success message: "Login successful!"
- ✅ Redirects to Home Dashboard
- ✅ Shows user name in header
- ✅ Bottom navigation tabs visible

**Actual Result:**
```
[ ] Success
[ ] Failed - Error: _________________________
```

---

### **Phase 2: Home & Navigation** 🏠

#### Test 2.1: Home Dashboard

**Check:**
- [ ] Dashboard loads without errors
- [ ] Shows welcome message with user name
- [ ] Displays user stats (if any)
- [ ] Navigation tabs visible at bottom

**Screenshot/Notes:**
```
_______________________________________
```

---

#### Test 2.2: Navigation Tabs

**Test each tab:**
- [ ] 🏠 Home - Loads correctly
- [ ] 📦 Categories - Shows categories list
- [ ] ➕ Create Order - Shows order creation
- [ ] 📋 My Orders - Shows orders list (empty OK)
- [ ] 👤 Profile - Shows user profile

**Notes:**
```
_______________________________________
```

---

### **Phase 3: Categories & Products** 📦

#### Test 3.1: View Categories

**Steps:**
1. Click "📦" Categories tab
2. Observe category list

**Expected Result:**
- ✅ Categories load from API
- ✅ Shows category names (Plastic, Paper, Metal, Glass, Electronics, etc.)
- ✅ Each category clickable

**Actual Result:**
```
[ ] Success
[ ] Failed - Error: _________________________
[ ] No categories (check Odoo data)
```

---

#### Test 3.2: View Products by Category

**Steps:**
1. Select a category (e.g., "Plastic")
2. View products list

**Expected Result:**
- ✅ Products load for selected category
- ✅ Shows product names, prices, units
- ✅ Can view product details

**Actual Result:**
```
[ ] Success
[ ] Failed - Error: _________________________
[ ] No products (check Odoo data)
```

---

### **Phase 4: Order/Request Creation** ➕

#### Test 4.1: Create New Request

**Steps:**
1. Click "➕" Create Order tab
2. Fill request form:
   - Select category
   - Select product(s)
   - Enter quantity
   - Select pickup address/time
3. Submit request

**Expected Result:**
- ✅ Form loads correctly
- ✅ Can select options from dropdowns
- ✅ Request created successfully
- ✅ Shows confirmation message

**Actual Result:**
```
[ ] Success
[ ] Failed - Error: _________________________
[ ] Missing fields: _____________________
```

---

### **Phase 5: Orders Management** 📋

#### Test 5.1: View My Orders

**Steps:**
1. Click "📋" My Orders tab
2. View orders list

**Expected Result:**
- ✅ Orders list loads (may be empty for new user)
- ✅ If orders exist, shows order details
- ✅ Can filter by status (pending, active, completed)

**Actual Result:**
```
[ ] Success
[ ] Failed - Error: _________________________
[ ] Empty list (OK for new user)
```

---

### **Phase 6: User Profile** 👤

#### Test 6.1: View Profile

**Steps:**
1. Click "👤" Profile tab
2. View profile information

**Expected Result:**
- ✅ Profile loads with user data
- ✅ Shows: Name, Phone, Email, User Type
- ✅ Shows account stats (if any)

**Actual Result:**
```
[ ] Success
[ ] Failed - Error: _________________________
```

---

#### Test 6.2: Edit Profile

**Steps:**
1. Try to update profile fields (if available)
2. Save changes

**Expected Result:**
- ✅ Can edit profile fields
- ✅ Changes save successfully
- ✅ Updated data reflects immediately

**Actual Result:**
```
[ ] Success
[ ] Failed - Error: _________________________
[ ] Feature not implemented
```

---

### **Phase 7: Wallet** 💰

#### Test 7.1: View Wallet

**Steps:**
1. Navigate to Wallet (if accessible from profile or menu)
2. View wallet balance and transactions

**Expected Result:**
- ✅ Wallet balance displays
- ✅ Transaction history loads (may be empty)

**Actual Result:**
```
[ ] Success
[ ] Failed - Error: _________________________
[ ] Not accessible yet
```

---

### **Phase 8: Logout & Re-login** 🔓

#### Test 8.1: Logout

**Steps:**
1. Find and click Logout button
2. Confirm logout

**Expected Result:**
- ✅ Successfully logs out
- ✅ Redirects to Login screen
- ✅ Session cleared

**Actual Result:**
```
[ ] Success
[ ] Failed - Error: _________________________
```

---

#### Test 8.2: Re-login

**Steps:**
1. Login again with same credentials
2. Verify all data persisted

**Expected Result:**
- ✅ Login successful
- ✅ Previous orders/data still visible
- ✅ Session restored correctly

**Actual Result:**
```
[ ] Success
[ ] Failed - Error: _________________________
```

---

## 🐛 Issues Found

### Critical Issues
```
1. _________________________________________
2. _________________________________________
3. _________________________________________
```

### Medium Issues
```
1. _________________________________________
2. _________________________________________
```

### Minor Issues / UI Tweaks
```
1. _________________________________________
2. _________________________________________
```

---

## 📊 Test Summary

**Total Tests**: 15  
**Passed**: ___  
**Failed**: ___  
**Skipped**: ___  

**Overall Status**: [ ] ✅ All Pass | [ ] ⚠️ Some Issues | [ ] ❌ Critical Failures

---

## 🔍 API Endpoints Called

During this test, the following endpoints should be called:

1. `POST /api/cyclex/auth/register`
2. `POST /api/cyclex/auth/verify-otp`
3. `POST /api/cyclex/auth/login`
4. `GET /api/cyclex/catalog/categories`
5. `GET /api/cyclex/catalog/products`
6. `GET /api/cyclex/user/profile`
7. `POST /api/cyclex/orders/create`
8. `GET /api/cyclex/orders/list`
9. `GET /api/cyclex/wallet/balance`
10. `GET /api/cyclex/wallet/transactions`

---

## 📝 Next Steps After Testing

**If All Tests Pass:**
- [ ] Document any missing features
- [ ] Test with mobile app
- [ ] Move to Stage 2 of API alignment plan

**If Tests Fail:**
- [ ] Document errors in detail
- [ ] Check Odoo logs: `tail -f ~/edu_demo/logs/odoo.log`
- [ ] Check browser console for errors
- [ ] Fix issues and re-test

---

## 🚀 Quick Test Commands

```bash
# Check if services running
ss -tlnp | grep -E "8025|8501"

# Check Streamlit logs
ps aux | grep streamlit

# Check Odoo logs for errors
tail -50 ~/edu_demo/logs/odoo.log | grep ERROR

# Restart Streamlit if needed
pkill -f streamlit
cd /home/sabry3/edu_demo/custom_addons/cyclex
streamlit run streamlit_app.py --server.port 8501 --server.headless true &

# Restart Odoo if needed
pkill -f "odoo-bin -c.*automatic_error_reporter"
cd /home/sabry3/edu_demo
./odoo18/odoo-bin -c odoo.conf/odoo.conf -d automatic_error_reporter &
```

---

## 📸 Screenshots Location

Save screenshots to: `/home/sabry3/edu_demo/custom_addons/cyclex/test_screenshots/`

```bash
mkdir -p /home/sabry3/edu_demo/custom_addons/cyclex/test_screenshots
```

---

**Tester**: _____________  
**Date Completed**: _____________  
**Time Taken**: _____________ minutes

