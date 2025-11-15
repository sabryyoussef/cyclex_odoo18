# Odoo Restart Instructions

**Date:** November 13, 2025  
**Reason:** Controller method changes (GET → POST) require server restart

---

## Current Status

✅ **Code fixes complete** - All 10 endpoints updated  
⚠️ **Odoo running with old code** - Process ID: 13855  
⚠️ **Restart required** - Changes won't take effect until restart

---

## How to Restart Odoo

### Option 1: If Odoo is running in a terminal

1. Go to the terminal where Odoo is running
2. Press `Ctrl+C` to stop it
3. Restart with:
   ```bash
   cd ~/edu_demo
   ./odoo18/odoo-bin -c odoo.conf/odoo.conf -d automatic_error_reporter
   ```

### Option 2: If Odoo is running in background

1. Stop the process:
   ```bash
   kill 13855
   # Or find and kill:
   pkill -f "odoo-bin.*8025"
   ```

2. Restart:
   ```bash
   cd ~/edu_demo
   ./odoo18/odoo-bin -c odoo.conf/odoo.conf -d automatic_error_reporter
   ```

### Option 3: Using systemd/service (if configured)

```bash
sudo systemctl restart odoo18
# Or
sudo service odoo18 restart
```

---

## Verify Restart

After restart, check:

1. **Process is running:**
   ```bash
   ps aux | grep odoo-bin | grep 8025
   ```

2. **Port is listening:**
   ```bash
   netstat -tlnp | grep 8025
   # Or
   ss -tlnp | grep 8025
   ```

3. **Test endpoint:**
   ```bash
   curl -X POST http://localhost:8025/api/cyclex/categories \
     -H "Content-Type: application/json" \
     -d '{"jsonrpc": "2.0", "method": "call", "params": {"language": "en"}, "id": 1}' \
     | python3 -m json.tool
   ```

---

## Expected After Restart

✅ All endpoints should accept POST requests  
✅ No more "405 Method Not Allowed" errors  
✅ Categories, Products, Health endpoints should work

---

## Quick Test Script

After restart, run:

```bash
cd ~/edu_demo
./custom_addons/cyclex/postman/CURL_TEST_SCRIPT.sh
```

---

**Status:** Waiting for Odoo restart  
**Next:** Test endpoints after restart

