# Streamlit App v2 - Mobile App Mock

**Date:** November 13, 2025  
**Status:** ✅ **RUNNING**

---

## What's New in v2

### 🎨 Based on Actual Mobile App Screenshots

The app now matches the actual mobile app design based on screenshots in `/postman/screenshots/`:

- ✅ **Splash Screen** - Initial welcome screen
- ✅ **Login Screen** - Matches `login.png`
- ✅ **Sign Up Screen** - Matches `sign up.png`
- ✅ **Verify OTP Screen** - Matches `verify.png`
- ✅ **Home Screen** - Matches `Home.png`
- ✅ **Categories** - Matches `categories.png`
- ✅ **My Orders** - Matches `my orders.png`
- ✅ **Profile** - Matches `profile.png`
- ✅ **Wallet** - Matches `profile-wallet.png`
- ✅ **Collector Screens** - Matches collector screenshots

---

## App Flow

### Unauthenticated Flow
1. **Splash Screen** → Click "Get Started"
2. **Login Screen** → Enter phone/password OR click "Sign Up"
3. **Sign Up Screen** → Fill form → Creates account → Goes to Verify OTP
4. **Verify OTP Screen** → Enter code → Verified → Back to Login

### Authenticated Flow (Customer)
- 🏠 **Home** - Dashboard with metrics
- 📦 **Categories** - Browse categories
- 📋 **My Orders** - View order history
- ➕ **Create Order** - Add new recycling request
- 👤 **Profile** - View/Edit profile
- 💰 **Wallet** - Balance and transactions

### Authenticated Flow (Collector)
- 🏠 **Home** - Collector dashboard
- 📦 **Available Orders** - See and accept/reject orders
- 📋 **My Orders** - Assigned orders
- 📷 **Scan QR** - Process QR codes
- 👤 **Profile** - Collector profile

---

## Login Fix

### Issues Fixed:
1. ✅ **JSON-RPC 2.0 Handling** - Now properly extracts `result` from JSON-RPC responses
2. ✅ **Session Cookies** - Properly saves and uses cookies for authentication
3. ✅ **Response Format** - Handles both JSON-RPC and direct JSON formats
4. ✅ **Error Handling** - Better error messages and handling

### Login Process:
1. User enters phone and password
2. App calls `/api/cyclex/auth/login`
3. Response is checked for JSON-RPC format
4. If successful, session cookies are saved
5. User data is stored in session state
6. App navigates to home screen

---

## Screenshot Integration

The app displays relevant screenshots from `/postman/screenshots/`:
- Shows actual mobile app design
- Helps understand expected UI
- Reference for testing

---

## Testing

### To Test Login:
1. Go to http://localhost:8501
2. Click "Get Started" on splash screen
3. Enter phone: `01000000000`
4. Enter password: `secret123` (or your actual password)
5. Click "Login"

### If Login Fails:
- Check if user exists in Odoo
- Check if phone is verified
- Check Odoo logs for errors
- Verify API endpoint is working: `curl -X POST http://localhost:8025/api/cyclex/auth/login -H "Content-Type: application/json" -d '{"phone": "01000000000", "password": "test123"}'`

---

## Registration Flow

1. **Sign Up** → Fill form (name, phone, password, role)
2. **Account Created** → Shows success message
3. **Verify OTP** → Enter 6-digit code
4. **Verified** → Can now login

---

## Features

- ✅ Screenshot references for each screen
- ✅ Proper navigation flow
- ✅ Session management
- ✅ JSON-RPC 2.0 support
- ✅ Cookie-based authentication
- ✅ Error handling
- ✅ Responsive design

---

**Status:** Ready for testing  
**URL:** http://localhost:8501

