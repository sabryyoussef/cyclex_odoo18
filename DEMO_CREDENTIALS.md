# 🎭 CycleX Demo Credentials

All demo users are automatically created when you install the CycleX module.

---

## 👥 DEMO CUSTOMERS

### Customer 1: Ahmed Ali
- **Phone:** `01200111111`
- **Password:** `Test1234`
- **OTP:** `123456`
- **City:** Cairo
- **Status:** Active, Verified

### Customer 2: Sara Mohamed
- **Phone:** `01200222222`
- **Password:** `Test1234`
- **OTP:** `123456`
- **City:** Giza
- **Status:** Active, Verified

### Customer 3: Omar Hassan
- **Phone:** `01200333333`
- **Password:** `Test1234`
- **OTP:** `123456`
- **City:** Alexandria
- **Status:** Active, Verified

---

## 🚚 DEMO COLLECTORS

### Collector 1: Mahmoud Collector
- **Phone:** `01250111111`
- **Password:** `Test1234`
- **OTP:** `123456`
- **City:** Cairo
- **Status:** Active, Verified

### Collector 2: Fatma Collector
- **Phone:** `01250222222`
- **Password:** `Test1234`
- **OTP:** `123456`
- **City:** Giza
- **Status:** Active, Verified

### Collector 3: Youssef Collector
- **Phone:** `01250333333`
- **Password:** `Test1234`
- **OTP:** `123456`
- **City:** Alexandria
- **Status:** Active, Verified

---

## 🎯 Quick Test Guide

### Test as Customer
1. Go to http://localhost:8501
2. Login with any customer phone (e.g., `01200111111`)
3. Password: `Test1234`
4. Navigate through: Home, Categories, Create Order, My Orders, Profile

### Test as Collector
1. Go to http://localhost:8501
2. Login with any collector phone (e.g., `01250111111`)
3. Password: `Test1234`
4. Navigate through: Home, Available Orders, My Orders, Scan QR, Profile

---

## 📦 Demo Data Included

### Categories (5)
- Plastic
- Paper
- Metal
- Glass
- Electronics

### Products (12)
- PET Bottles (Clear) - 3.80 EGP/kg
- HDPE Bottles (Colored) - 3.20 EGP/kg
- Plastic Bags - 2.50 EGP/kg
- Newspapers - 1.20 EGP/kg
- Cardboard Boxes - 1.50 EGP/kg
- Office Paper - 2.00 EGP/kg
- Aluminum Cans - 5.00 EGP/kg
- Copper Wire - 25.00 EGP/kg
- Glass Bottles (Clear) - 0.90 EGP/kg
- Glass Bottles (Colored) - 0.70 EGP/kg
- Mobile Phones - 20.00 EGP/kg
- Small Appliances - 12.00 EGP/kg

---

## 🔄 Reinstall Module

If you need to reload all demo data:

### Option 1: Via PyCharm
1. Find CycleX module
2. Uninstall
3. Install again

### Option 2: Via Odoo Web
1. Go to http://localhost:8069
2. Apps → CycleX
3. Uninstall → Install

---

## ✅ What to Test

### Customer Flow
1. ✅ Login with customer account
2. ✅ View categories (should see 5)
3. ✅ Browse products in each category
4. ✅ Create a new order
5. ✅ View order in "My Orders"
6. ✅ Check profile information
7. ✅ Test logout

### Collector Flow
1. ✅ Login with collector account
2. ✅ View available orders
3. ✅ Accept an order
4. ✅ View "My Orders"
5. ✅ Complete order workflow
6. ✅ Check earnings/commission
7. ✅ Test logout

---

## 🐛 Troubleshooting

### Can't login?
- Make sure you updated/reinstalled the module
- Users are only created during module installation
- Try uninstalling and installing fresh

### No categories showing?
- Click "Load" button on Categories screen
- Check if module was installed (not just upgraded)
- Verify in Odoo: CycleX → Categories menu

### API errors?
- Check Odoo is running: http://localhost:8069
- Check Streamlit is running: http://localhost:8501
- Review logs: `tail -f ~/edu_demo/logs/odoo.log`

---

*Created: November 14, 2025*
*Module: CycleX v18.0.1.0.0*

