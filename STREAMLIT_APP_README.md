# CycleX Mobile App Mock - Streamlit Application

A Streamlit web application that mimics the CycleX mobile app for testing API endpoints.

## Features

- 🔐 **Authentication**: Login, Signup, OTP Verification
- 🏠 **Home Dashboard**: View summary and statistics
- 📦 **Categories & Products**: Browse categories and products
- 📋 **Orders**: Create orders, view order history, track orders
- 👤 **Profile**: View and update user profile
- 💰 **Wallet**: Check balance and view transactions
- 🚚 **Collector App**: Dashboard, available orders, QR scanning

## Installation

1. Install dependencies:
```bash
pip install -r requirements_streamlit.txt
```

## Running the App

```bash
streamlit run streamlit_app.py
```

The app will open in your browser at `http://localhost:8501`

## Configuration

The app is configured to use:
- **API Base URL**: `http://localhost:8025/api/cyclex`

You can modify this in the `streamlit_app.py` file:
```python
API_BASE_URL = "http://localhost:8025/api/cyclex"
```

## Usage

1. **Start Odoo** on port 8025
2. **Run Streamlit app**: `streamlit run streamlit_app.py`
3. **Navigate** through the app using the sidebar
4. **Test endpoints** by interacting with the forms and buttons

## Features by Screen

### Authentication
- Login with phone and password
- Sign up for new account
- Verify OTP code
- Resend OTP

### Home
- View dashboard summary
- See active orders count
- Check wallet balance
- View total requests

### Categories & Products
- Browse all categories
- View products by category
- Filter by language (en/ar)

### Orders
- Create new order with photo upload
- View order history with status filter
- Track specific order by ID

### Profile
- View user profile information
- Update profile details
- Change language preference

### Wallet
- Check current balance
- View transaction history
- See total earnings and withdrawals

### Collector App
- View collector dashboard
- See available orders
- Accept/reject orders
- Scan QR codes

## Session Management

The app automatically manages session cookies for authenticated requests. Once you login, the session is maintained across all requests.

## Notes

- All fields match the Postman collection structure
- The app uses the same API endpoints as the mobile app
- Responses are displayed in JSON format for debugging
- Error messages are shown clearly for failed requests

## Troubleshooting

1. **Connection Error**: Make sure Odoo is running on port 8025
2. **401 Errors**: Login first to authenticate
3. **Module Not Found**: Make sure the cyclex module is installed and upgraded in Odoo
4. **Empty Responses**: Check Odoo logs for errors

---

**Status**: Ready for testing  
**Last Updated**: November 13, 2025

