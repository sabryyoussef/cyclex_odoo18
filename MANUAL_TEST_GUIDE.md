# 📱 Quick Manual Test Guide - Streamlit App

**Start Here**: http://localhost:8501

---

## ✅ Pre-Test: APIs Verified Working

All backend APIs tested and confirmed working:
- ✅ Login API
- ✅ Categories API  
- ✅ Products API (via category)
- ✅ OTP Verification

---

## 🧪 5-Minute Essential Flow Test

### **Test 1: Login** (1 min)

1. Open: http://localhost:8501
2. Use existing account:
   - **Phone**: `01000111111`
   - **Password**: `Test1234`
3. Click "Login"

**✅ Pass if**: Shows home dashboard with user name

**❌ Fail if**: Error message or stays on login screen

---

### **Test 2: Navigate Tabs** (1 min)

After login, click each bottom tab:

- **🏠 Home** - Should show dashboard
- **📦 Categories** - Should list categories
- **➕ Create Order** - Should show create form
- **📋 My Orders** - Should show orders list (empty OK)
- **👤 Profile** - Should show user info

**✅ Pass if**: All tabs load without errors

**❌ Fail if**: Any tab shows error or doesn't load

---

### **Test 3: View Categories** (1 min)

1. Click **📦 Categories** tab
2. Should see categories list
3. Try clicking a category (if implemented)

**✅ Pass if**: Categories display

**❌ Fail if**: Error or empty (check Odoo data)

---

### **Test 4: New Registration** (2 min)

1. Logout (if logout button exists) or open in incognito
2. Go to: http://localhost:8501
3. Click "📝 Don't have an account? Sign Up"
4. Fill form:
   - **Name**: `Manual Test User`
   - **Phone**: `01000444444` (use unique number)
   - **Password**: `Test1234`
   - **Confirm Password**: `Test1234`
   - **Account Type**: Customer
   - ✓ Accept Terms
5. Click "Sign Up"
6. Should see OTP screen with test code **123456**
7. Enter OTP: `123456`
8. Click "Verify"
9. Should redirect to login
10. Login with new credentials

**✅ Pass if**: Complete flow works, can login

**❌ Fail if**: Error at any step

---

## 🐛 Common Issues & Fixes

### Issue: "Connection refused" or "Failed to fetch"
**Fix**: Check Odoo is running
```bash
ss -tlnp | grep 8025
# If not running:
cd /home/sabry3/edu_demo
./odoo18/odoo-bin -c odoo.conf/odoo.conf -d automatic_error_reporter &
```

### Issue: Login shows "Invalid credentials"
**Cause**: May need to verify OTP first  
**Fix**: Register → Verify OTP → Then login

### Issue: Categories/Products empty
**Cause**: No data in Odoo  
**Fix**: Need to add categories/products in Odoo backend

### Issue: Streamlit not responding
**Fix**: Restart Streamlit
```bash
pkill -f streamlit
cd /home/sabry3/edu_demo/custom_addons/cyclex
streamlit run streamlit_app.py --server.port 8501 --server.headless true &
```

---

## 📋 Quick Status Check

After testing, mark what works:

- [ ] Login works
- [ ] Can navigate between tabs
- [ ] Categories display
- [ ] Products display (by category)
- [ ] Can register new user
- [ ] OTP verification works
- [ ] Profile shows user data

---

## 🔍 Check Logs for Errors

If something fails:

```bash
# Odoo logs (real-time)
tail -f ~/edu_demo/logs/odoo.log | grep -i "error\|cyclex"

# Check last 50 errors
tail -100 ~/edu_demo/logs/odoo.log | grep ERROR
```

**Browser Console**: Press F12 → Console tab to see JavaScript errors

---

## 📝 Report Format

When reporting issues, include:

1. **What you were doing**: "Clicked Categories tab"
2. **What happened**: "Got AttributeError"
3. **Error message**: (copy exact error)
4. **Browser console**: (any red errors)
5. **Odoo log**: (if relevant)

---

## ✨ Quick Wins

Things that should work immediately:
- ✅ Login with 01000111111 / Test1234
- ✅ View categories list
- ✅ View products (when clicking category)
- ✅ Register → Verify OTP → Login

Things that may need work:
- ⚠️ Creating orders/requests
- ⚠️ Profile editing
- ⚠️ Wallet transactions
- ⚠️ Collector features

---

## 🎯 Success Criteria

**Minimum viable**: If login + categories + products work, we're good to proceed!

**Full success**: All tabs load, no errors, complete flows work

---

**Time Estimate**: 5-10 minutes for essential tests

**Ready?** Open http://localhost:8501 and start with Test 1! 🚀

