# Streamlit App v2 - Complete Guide

## 🎯 What's New

### Based on Mobile App Screenshots
The app now matches the actual mobile app design from screenshots in `/postman/screenshots/`

### App Flow
1. **Splash Screen** → Welcome screen with "Get Started" button
2. **Login Screen** → Enter phone & password
3. **Sign Up Screen** → Create new account
4. **Verify OTP** → Verify phone number
5. **Home** → Dashboard (different for customer/collector)

---

## 🔐 Login Issue - Why It's Not Working

### Current Status
The login endpoint is working correctly, but you need:
1. **Valid user account** in Odoo database
2. **Verified phone number** (phone_verified = True)
3. **Active account status** (account_status = 'active')
4. **Correct password** for the user

### Solution: Create User First

**Option 1: Use Sign Up in the App**
1. Go to Login screen
2. Click "Sign Up"
3. Fill the form:
   - Name: Your name
   - Phone: Your phone number
   - Password: Create password
   - Role: Customer or Collector
4. Submit → Account created
5. Go to Verify OTP screen
6. Enter OTP code (check Odoo logs or database for OTP)
7. After verification, go back to Login
8. Login with your credentials

**Option 2: Create User in Odoo**
1. Go to Odoo UI: http://localhost:8025
2. Create a partner with:
   - Phone number
   - is_cyclex_user = True
   - cyclex_user_type = 'customer' or 'collector'
   - phone_verified = True
   - account_status = 'active'
3. Create a user account linked to this partner
4. Set password for the user
5. Then login in Streamlit app

---

## 📱 Screens Available

### Unauthenticated
- ✅ **Splash** - Welcome screen
- ✅ **Login** - Phone + password
- ✅ **Sign Up** - Registration form
- ✅ **Verify OTP** - Phone verification

### Customer Screens
- ✅ **Home** - Dashboard with metrics
- ✅ **Categories** - Browse categories
- ✅ **Create Order** - Add recycling request
- ✅ **My Orders** - Order history
- ✅ **Profile** - View profile
- ✅ **Wallet** - Balance & transactions

### Collector Screens
- ✅ **Home** - Collector dashboard
- ✅ **Available Orders** - See and accept/reject
- ✅ **My Orders** - Assigned orders
- ✅ **Scan QR** - Process QR codes
- ✅ **Profile** - Collector profile

---

## 🐛 Troubleshooting

### Login Returns "Invalid credentials"
- User doesn't exist → Use Sign Up first
- Phone not verified → Verify OTP first
- Wrong password → Check password in Odoo
- Account suspended → Check account_status in Odoo

### Screenshots Not Showing
- Check if files exist in `/postman/screenshots/`
- App will work without screenshots (they're just references)

### API Errors
- Make sure Odoo is running on port 8025
- Check if cyclex module is upgraded
- Check Odoo logs for errors

---

## 🚀 Quick Start

1. **Start Odoo**: Make sure it's running on port 8025
2. **Open App**: http://localhost:8501
3. **Create Account**: Use Sign Up screen
4. **Verify**: Enter OTP code
5. **Login**: Use your credentials
6. **Test**: Navigate through all screens

---

**Status:** ✅ Running  
**URL:** http://localhost:8501  
**Version:** v2 (Based on mobile app screenshots)

