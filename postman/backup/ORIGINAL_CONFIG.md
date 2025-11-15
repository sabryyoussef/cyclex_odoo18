# Original Configuration (Before Stage 1 Changes)

**Date:** November 13, 2025  
**Backup Location:** `postman/backup/2025-11-13/`

---

## Environment Variables

**File:** `CycleX-Local.postman_environment.json`

| Variable | Value | Type | Notes |
|----------|-------|------|-------|
| `base_url` | `http://localhost:8000/api` | default | **Note:** After Stage 2, this will need `/api/cyclex` prefix |
| `auth_token` | (empty, auto-filled) | secret | Auto-filled after login |
| `user_id` | (empty, auto-filled) | default | Auto-filled after login |
| `collector_id` | (empty, auto-filled) | default | Auto-filled after collector login |
| `language` | `en` | default | Default language |

---

## Collections Backed Up

**Total Collections:** 37

All Postman collection JSON files have been backed up to:
- `postman/backup/2025-11-13/*.postman_collection.json`

**Collections List:**
1. 01-login.postman_collection.json
2. 02-signup.postman_collection.json
3. 03-verify-otp.postman_collection.json
4. 04-resend-otp.postman_collection.json
5. 05-home-summary.postman_collection.json
6. 06-home-order-active.postman_collection.json
7. 07-splash.postman_collection.json
8. 08-categories-list.postman_collection.json
9. 09-category-items-plastic.postman_collection.json
10. 10-category-items-paper.postman_collection.json
11. 11-category-items-metal.postman_collection.json
12. 12-category-items-glass.postman_collection.json
13. 13-category-items-electronics.postman_collection.json
14. 14-add-new-item.postman_collection.json
15. 15-estimate-item.postman_collection.json
16. 16-add-other-items.postman_collection.json
17. 17-finish-order.postman_collection.json
18. 18-confirm-order.postman_collection.json
19. 19-my-orders.postman_collection.json
20. 20-active-orders.postman_collection.json
21. 21-orders-tracking.postman_collection.json
22. 22-rating-order.postman_collection.json
23. 23-profile.postman_collection.json
24. 24-update-profile.postman_collection.json
25. 25-profile-wallet.postman_collection.json
26. 26-wallet-transactions.postman_collection.json
27. 27-user-addresses.postman_collection.json
28. 28-login-collector.postman_collection.json
29. 29-signup-collector.postman_collection.json
30. 30-collector-status.postman_collection.json
31. 31-collector-home.postman_collection.json
32. 32-collector-active-orders.postman_collection.json
33. 33-scan-qr.postman_collection.json
34. 34-accept-order.postman_collection.json
35. 35-reject-order.postman_collection.json
36. 36-collector-finish-order.postman_collection.json
37. 37-collector-profile.postman_collection.json

---

## Current Base URL Structure

**Postman Collections Use:**
- `/auth/*` → Should be `/api/cyclex/*`
- `/catalog/*` → Should be `/api/cyclex/*`
- `/orders/*` → Should be `/api/cyclex/request/*` or `/api/cyclex/order/*`
- `/user/*` → Should be `/api/cyclex/*`
- `/wallet/*` → Should be `/api/cyclex/wallet/*`
- `/collector/*` → Should be `/api/cyclex/collector/*`

**Odoo Backend Uses:**
- All endpoints prefixed with `/api/cyclex/`
- Base URL: `http://localhost:10018` (from API_DOCUMENTATION.md)

**Note:** There's a mismatch:
- Postman environment: `http://localhost:8000/api`
- Odoo documentation: `http://localhost:10018`

This needs to be resolved in Stage 2.

---

## Backup Verification

✅ All 37 collection files backed up  
✅ Environment file backed up  
✅ Configuration documented

---

**Backup Complete:** November 13, 2025

