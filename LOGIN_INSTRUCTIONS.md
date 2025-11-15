# 🔐 Login Instructions for CycleX App

## Quick Start - Demo Mode

The app is currently in **Demo Mode** (`USE_DEMO_DATA = True`), which means you can login instantly without needing to register!

### Demo Users Available:

#### 👤 **Customer Account**
- **Phone:** `01000000000`
- **Password:** `demo123`
- **Features:** Browse categories, create orders, view wallet, etc.

#### 🚚 **Collector Account**
- **Phone:** `01000000001`
- **Password:** `demo123`
- **Features:** View available orders, accept/reject orders, collector dashboard

---

## How to Login

### Option 1: Quick Demo Login (Recommended)
1. Go to the **Login** screen
2. Click the **"📱 Demo Mode - Quick Login"** expander at the top
3. Click either:
   - **"👤 Login as Customer"** - For customer features
   - **"🚚 Login as Collector"** - For collector features
4. You'll be logged in instantly!

### Option 2: Use Demo Credentials in Form
1. Go to the **Login** screen
2. The form is pre-filled with demo credentials
3. Click **"Login"** button
4. You'll be logged in as a customer

### Option 3: Register New Account
1. Go to **Login** screen
2. Click **"📝 Don't have an account? Sign Up"**
3. Fill in the registration form:
   - Full Name
   - Phone Number
   - Password
   - Confirm Password
   - Email (optional)
   - Account Type (Customer or Collector)
   - Accept Terms & Conditions
4. Click **"Sign Up"**
5. You'll be redirected to **Verify OTP** screen
6. Enter the OTP code (check Odoo logs/database for the code)
7. After verification, go back to Login
8. Login with your new credentials

---

## Real API Mode

If you want to use the real Odoo API instead of demo data:

1. Open `streamlit_app.py`
2. Change line 23:
   ```python
   USE_DEMO_DATA = False  # Changed from True
   ```
3. Restart the Streamlit app
4. You'll need to:
   - Have a user account in Odoo database
   - Phone number must be verified
   - Account status must be 'active'
   - Use the correct password

---

## Troubleshooting

### Can't Login?
- **Demo Mode:** Make sure `USE_DEMO_DATA = True`
- **Real API:** 
  - Check if Odoo is running on port 8025
  - Verify user exists in database
  - Check if phone is verified
  - Check account status

### Phone Not Verified?
- Use the **"Go to Verify OTP"** button that appears
- Or register a new account and verify during signup

### Forgot Password?
- Currently, password reset is not implemented
- You'll need to create a new account or contact admin

---

## Current Status

✅ **Demo Mode:** Enabled  
✅ **Demo Users:** Available  
✅ **Quick Login:** Working  
🌐 **App URL:** http://localhost:8501

---

**Enjoy testing the CycleX app!** 🎉

