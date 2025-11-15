# 🔄 Update CycleX Module - Load Demo Data

## Quick Steps (Via PyCharm)

Since you're using PyCharm, follow these steps to load the demo data:

### 1. Update the Module
1. Open **PyCharm**
2. Go to **Odoo** menu or use the Odoo plugin
3. Find **CycleX** module
4. Click **Update Module** or **Upgrade**
5. Wait for the update to complete

### 2. Verify Data Loaded
After updating, the following will be created automatically:

**5 Categories:**
- 📦 Plastic (3.50 EGP/kg)
- 📄 Paper (1.20 EGP/kg)
- 🔩 Metal (4.50 EGP/kg)
- 🥃 Glass (0.80 EGP/kg)
- 📱 Electronics (15.00 EGP/kg)

**12 Products:**
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

### 3. Test in Streamlit
1. Refresh your browser at http://localhost:8501
2. Click **📦 Categories** button
3. You should now see **5 categories** instead of 0
4. Click **View Products** to see products in each category
5. Go to **➕ Create** to create an order with real products

---

## Alternative: Manual Update via Odoo Web

If you prefer to update via Odoo web interface:

1. Go to http://localhost:8069
2. Login as admin
3. Go to **Apps** menu
4. Search for **"CycleX"**
5. Click **Upgrade** button
6. Wait for completion
7. Refresh Streamlit app

---

## Files Created

### 1. Demo Data Files
```
/home/sabry3/edu_demo/custom_addons/cyclex/data/demo_categories.xml
/home/sabry3/edu_demo/custom_addons/cyclex/data/demo_products.xml
```

### 2. Manifest Updated
```
/home/sabry3/edu_demo/custom_addons/cyclex/__manifest__.py
```

Added:
```python
# Demo Data
'data/demo_categories.xml',
'data/demo_products.xml',
```

---

## Troubleshooting

### Problem: Demo data not loading
**Solution:** 
- Delete the module
- Reinstall it fresh
- This will force reload all data files

### Problem: Categories show 0 in Streamlit
**Solution:**
- Check Odoo logs: `tail -f ~/edu_demo/logs/odoo.log`
- Verify categories exist in Odoo:
  - Go to CycleX > Categories menu
  - Check if 5 categories are listed

### Problem: API returns empty data
**Solution:**
- Check the API endpoint manually:
```bash
curl -X GET "http://localhost:8069/cyclex/catalog/categories" \
  -H "Content-Type: application/json"
```

---

## After Update - Test Flow

1. **Refresh Browser** (Ctrl+F5 to force reload)
2. **Login** to Streamlit (01000111111 / Test1234)
3. **Click Categories** - Should show 5 categories
4. **Click "View Products"** - Should show products
5. **Go to Create** - Should be able to select categories & products
6. **Fill the form:**
   - Category ID: 8 (Plastic)
   - Product ID: 0 (for custom item) or specific product ID
   - Quantity: 5
   - Weight: 2.5 kg
   - Pickup Date: Today's date
   - Notes: Test order
7. **Click "Create Order"** - Should create successfully
8. **Go to My Orders** - Should see the order listed

---

## Need Help?

If issues persist:
1. Check Odoo logs for errors
2. Verify module is installed and updated
3. Test API endpoints with curl
4. Restart Streamlit app

**Quick restart Streamlit:**
```bash
pkill -f streamlit
cd /home/sabry3/edu_demo/custom_addons/cyclex
streamlit run streamlit_app.py --server.port 8501 --server.headless true &
```

---

*Created: November 14, 2025*

