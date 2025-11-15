# 🚀 Quick Testing Commands

## Switch to Real API Mode

```bash
cd /home/sabry3/edu_demo/custom_addons/cyclex

# Edit streamlit_app.py line 23
sed -i 's/USE_DEMO_DATA = True/USE_DEMO_DATA = False/' streamlit_app.py

# Restart Streamlit
pkill -f streamlit
python3 -m streamlit run streamlit_app.py --server.port 8501 --server.headless true > /tmp/streamlit.log 2>&1 &
```

## Check Odoo Status

```bash
# Check if Odoo is running
curl -s http://localhost:8025/web/database/selector | head -1

# Check API endpoint
curl -s http://localhost:8025/api/cyclex/health-check | python3 -m json.tool
```

## View Odoo Data (SQL)

```bash
# Connect to Odoo database
psql -d automatic_error_reporter -c "
SELECT name, phone, cyclex_user_type, phone_verified 
FROM res_partner 
WHERE is_cyclex_user = true 
LIMIT 5;
"
```

## Test API Endpoints

```bash
# Test login
curl -X POST http://localhost:8025/api/cyclex/auth/login \
  -H "Content-Type: application/json" \
  -d '{"phone": "01012345678", "password": "test123"}' | python3 -m json.tool

# Test categories
curl -s http://localhost:8025/api/cyclex/catalog/categories?language=en | python3 -m json.tool
```

## Monitor Streamlit Logs

```bash
# Watch Streamlit logs
tail -f /tmp/streamlit.log

# Check for errors
grep -i error /tmp/streamlit.log | tail -10
```

## Monitor Odoo Logs

```bash
# Find Odoo log file (usually in ~/edu_demo/)
tail -f ~/edu_demo/odoo.log 2>/dev/null || tail -f /var/log/odoo/odoo.log 2>/dev/null
```

