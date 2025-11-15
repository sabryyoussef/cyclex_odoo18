# CycleX Postman Collections

This directory contains Postman collections and environments for testing the CycleX API.

## Structure

```
postman/
├── collections/          # All 37 Postman collection files
├── environments/        # Environment configuration files
├── docs/                # API documentation and alignment reports
├── backup/              # Backup of original collections
└── screenshots/         # UI screenshots (reference)
```

## Quick Start

### 1. Import Environment

1. Open Postman
2. Click **Import** button
3. Select `environments/CycleX-Local.postman_environment.json`
4. The environment will be created with variables:
   - `odoo_host`: http://localhost:8025 (your local Odoo server)
   - `api_prefix`: /api/cyclex
   - `base_url`: {{odoo_host}}{{api_prefix}} = http://localhost:8025/api/cyclex
   - `auth_token`: (auto-filled after login)
   - `user_id`: (auto-filled after login)
   - `collector_id`: (auto-filled after collector login)
   - `language`: en

### 2. Import Collections

Import all collection files from `collections/` directory. You can:
- Import them one by one
- Or select multiple files and import them all at once

### 3. Select Environment

After importing, make sure to select the **CycleX-Local** environment from the environment dropdown in Postman.

## Environment Configuration

### Local Development

**File:** `environments/CycleX-Local.postman_environment.json`

- **Odoo Host:** `http://localhost:8025`
- **Database:** `automatic_error_reporter`
- **Config:** `/home/sabry3/edu_demo/odoo.conf/odoo.conf`

### Production

**File:** `environments/CycleX-Production.postman_environment.json`

- **Odoo Host:** Update `odoo_host` variable to your production URL
- **API Prefix:** Same (`/api/cyclex`)

## Switching Environments

To switch between local and production:

1. In Postman, select the environment dropdown
2. Choose **CycleX-Local** or **CycleX-Production**
3. All requests will automatically use the correct base URL

## Collections Overview

### Auth Flow (User App)
- 01-login.postman_collection.json
- 02-signup.postman_collection.json
- 03-verify-otp.postman_collection.json
- 04-resend-otp.postman_collection.json

### Home & Navigation
- 05-home-summary.postman_collection.json
- 06-home-order-active.postman_collection.json
- 07-splash.postman_collection.json

### Categories & Catalog
- 08-categories-list.postman_collection.json
- 09-13: Category items collections (Plastic, Paper, Metal, Glass, Electronics)

### Items & Orders
- 14-add-new-item.postman_collection.json
- 15-estimate-item.postman_collection.json
- 16-add-other-items.postman_collection.json
- 17-finish-order.postman_collection.json
- 18-confirm-order.postman_collection.json

### Order Management
- 19-my-orders.postman_collection.json
- 20-active-orders.postman_collection.json
- 21-orders-tracking.postman_collection.json
- 22-rating-order.postman_collection.json

### Profile & Account
- 23-profile.postman_collection.json
- 24-update-profile.postman_collection.json
- 25-profile-wallet.postman_collection.json
- 26-wallet-transactions.postman_collection.json
- 27-user-addresses.postman_collection.json

### Collector App
- 28-login-collector.postman_collection.json
- 29-signup-collector.postman_collection.json
- 30-collector-status.postman_collection.json
- 31-collector-home.postman_collection.json
- 32-collector-active-orders.postman_collection.json
- 33-scan-qr.postman_collection.json
- 34-accept-order.postman_collection.json
- 35-reject-order.postman_collection.json
- 36-collector-finish-order.postman_collection.json
- 37-collector-profile.postman_collection.json

## Testing Your Local Odoo

### Prerequisites

1. Odoo 18 running on `http://localhost:8025`
2. Database: `automatic_error_reporter`
3. CycleX module installed and active

### Quick Test

1. **Health Check:**
   - Import collection (if you have a health check collection)
   - Or test manually: `GET http://localhost:8025/api/cyclex/health`

2. **Login Test:**
   - Use collection: `01-login.postman_collection.json`
   - Update phone/password with test user credentials
   - Run request
   - Check that `auth_token` and `user_id` are saved to environment

## Documentation

See `docs/` directory for:
- **CYCLEX_API_ALIGNMENT_FIX_PLAN.md** - Complete fix plan
- **ODOO_ENDPOINTS_REFERENCE.md** - All Odoo endpoints documented
- **VERIFIED_ENDPOINT_MATRIX_V2.md** - Postman vs Odoo mapping
- **PRIORITY_LIST.md** - Fix priorities
- **STAGE_1_COMPLETION_REPORT.md** - Stage 1 results

## Notes

- All endpoints use the `/api/cyclex` prefix
- Authentication is session-based (Odoo handles sessions)
- Some endpoints may need path corrections (see Stage 2 in fix plan)
- Missing endpoints will be implemented in Stage 3

## Troubleshooting

### Connection Errors

- **404 Not Found:** Check that Odoo is running on port 8025
- **Connection Refused:** Verify Odoo server is started
- **Wrong Port:** Update `odoo_host` in environment file

### Authentication Issues

- **401 Unauthorized:** Make sure you've logged in first
- **Token Not Saved:** Check test scripts in login collections

### Path Errors

- **404 on endpoints:** Paths may need `/api/cyclex` prefix (Stage 2 fixes this)
- See `VERIFIED_ENDPOINT_MATRIX_V2.md` for correct paths

---

**Last Updated:** November 13, 2025  
**Odoo Version:** 18  
**Module Location:** `/home/sabry3/edu_demo/custom_addons/cyclex`

