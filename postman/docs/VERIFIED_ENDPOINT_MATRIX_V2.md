# Verified Endpoint Matrix v2

**Generated:** November 13, 2025  
**Purpose:** Complete mapping of Postman Collections (37) to Odoo Endpoints (24)

---

## Matrix Legend

- ✅ **MATCHED** - Endpoint exists in Odoo, path/method may need correction
- ⚠️ **PATH MISMATCH** - Endpoint exists but path is different
- ⚠️ **METHOD MISMATCH** - Endpoint exists but HTTP method is different
- ❌ **MISSING** - Endpoint does not exist in Odoo
- 🔄 **ARCHITECTURAL DIFF** - Different approach (cart vs direct)

---

## Complete Mapping Table

| # | Postman Collection | Postman Path | Postman Method | Odoo Path | Odoo Method | Status | Notes |
|---|-------------------|--------------|----------------|-----------|-------------|--------|-------|
| 01 | Login | `/auth/login` | POST | `/api/cyclex/login` | POST | ⚠️ **PATH MISMATCH** | Missing `/api/cyclex` prefix |
| 02 | Sign Up | `/auth/register` | POST | `/api/cyclex/register` | POST | ⚠️ **PATH MISMATCH** | Missing `/api/cyclex` prefix |
| 03 | Verify OTP | `/auth/verify-otp` | POST | `/api/cyclex/verify` | POST | ⚠️ **PATH MISMATCH** | Path + param name (`otp` → `verification_code`) |
| 04 | Resend OTP | `/auth/resend-otp` | POST | `/api/cyclex/resend-code` | POST | ⚠️ **PATH MISMATCH** | Path name differs |
| 05 | Home Summary | `/home/summary` | GET | ❌ **NOT FOUND** | - | ❌ **MISSING** | Need to implement |
| 06 | Home (Order Active) | `/home/summary?include_active_order=true` | GET | ❌ **NOT FOUND** | - | ❌ **MISSING** | Need to implement |
| 07 | Splash Screen | `/app/config` | GET | ❌ **NOT FOUND** | - | ❌ **MISSING** | Need to implement |
| 08 | Categories List | `/catalog/categories` | GET | `/api/cyclex/categories` | GET | ⚠️ **PATH MISMATCH** | Missing `/api/cyclex` prefix |
| 09 | Category Items (Plastic) | `/catalog/categories/PLASTIC/items` | GET | `/api/cyclex/products?category_id=X` | GET | ⚠️ **PATH MISMATCH** | Different structure (path param → query param) |
| 10 | Category Items (Paper) | `/catalog/categories/PAPER/items` | GET | `/api/cyclex/products?category_id=X` | GET | ⚠️ **PATH MISMATCH** | Different structure |
| 11 | Category Items (Metal) | `/catalog/categories/METAL/items` | GET | `/api/cyclex/products?category_id=X` | GET | ⚠️ **PATH MISMATCH** | Different structure |
| 12 | Category Items (Glass) | `/catalog/categories/GLASS/items` | GET | `/api/cyclex/products?category_id=X` | GET | ⚠️ **PATH MISMATCH** | Different structure |
| 13 | Category Items (Electronics) | `/catalog/categories/ELECTRONICS/items` | GET | `/api/cyclex/products?category_id=X` | GET | ⚠️ **PATH MISMATCH** | Different structure |
| 14 | Add New Item | `/orders/items/custom` | POST (multipart) | `/api/cyclex/request/create` | POST | 🔄 **ARCHITECTURAL DIFF** | Cart-based vs direct creation |
| 15 | Estimate Item | `/orders/items/custom/estimate` | POST | ❌ **NOT FOUND** | - | ❌ **MISSING** | Price calculated on creation |
| 16 | Add Other Items | `/orders/items` | POST | `/api/cyclex/request/create` | POST | 🔄 **ARCHITECTURAL DIFF** | Cart-based vs direct creation |
| 17 | Finish Order | `/orders` | POST | `/api/cyclex/request/create` | POST | ⚠️ **PATH MISMATCH** | Different request structure |
| 18 | Confirm Order | `/orders/{id}/confirm` | PUT | ❌ **NOT FOUND** | - | ❌ **MISSING** | Auto-confirmed on creation |
| 19 | My Orders | `/orders?status=all` | GET | `/api/cyclex/request/list` | GET | ⚠️ **PATH MISMATCH** | Different status naming |
| 20 | Active Orders | `/orders?status=active` | GET | `/api/cyclex/request/list?status=pending` | GET | ⚠️ **PATH + STATUS MISMATCH** | `active` → `pending` |
| 21 | Orders Tracking | `/orders/{id}` | GET | `/api/cyclex/request/details/{id}` | GET | ⚠️ **PATH MISMATCH** | Missing `/api/cyclex/request/details` |
| 22 | Rating Order | `/orders/{id}/rate` | POST | `/api/cyclex/order/rate/{id}` | POST | ⚠️ **PATH MISMATCH** | Path structure differs |
| 23 | Profile | `/user/profile` | GET | `/api/cyclex/profile` | GET | ⚠️ **PATH MISMATCH** | Missing `/api/cyclex` prefix |
| 24 | Update Profile | `/user/profile` | PUT | `/api/cyclex/update-profile` | POST | ⚠️ **PATH + METHOD MISMATCH** | PUT → POST, path differs |
| 25 | Profile Wallet | `/wallet` | GET | `/api/cyclex/wallet/balance` | GET | ⚠️ **PATH MISMATCH** | Missing `/api/cyclex/wallet/balance` |
| 26 | Wallet Transactions | `/wallet/transactions` | GET | `/api/cyclex/wallet/transactions` | GET | ⚠️ **PATH MISMATCH** | Missing `/api/cyclex` prefix |
| 27 | User Addresses | `/user/addresses` | GET/POST/PUT | ❌ **NOT FOUND** | - | ❌ **MISSING** | Need to implement |
| 28 | Login (Collector) | `/auth/login` (role=collector) | POST | `/api/cyclex/login` | POST | ⚠️ **PATH MISMATCH** | Same endpoint, different path |
| 29 | Sign Up (Collector) | `/auth/register` (role=collector) | POST | `/api/cyclex/register` | POST | ⚠️ **PATH MISMATCH** | Same endpoint, different path |
| 30 | Collector Status | `/collector/status` | GET | ❌ **NOT FOUND** | - | ❌ **MISSING** | Status in profile, need dedicated endpoint |
| 31 | Collector Home | `/collector/home` | GET | ❌ **NOT FOUND** | - | ❌ **MISSING** | Need to implement |
| 32 | Collector Active Orders | `/collector/orders?status=assigned` | GET | `/api/cyclex/collector/available-orders` | GET | ⚠️ **PATH MISMATCH** | Different endpoint name |
| 33 | Scan QR | `/collector/orders/scan-qr` | POST | `/api/cyclex/collector/scan-qr` | POST | ⚠️ **PATH MISMATCH** | Missing `/api/cyclex` prefix |
| 34 | Accept Order | `/collector/orders/{id}/accept` | POST | `/api/cyclex/collector/accept-order/{id}` | POST | ⚠️ **PATH MISMATCH** | Path structure differs |
| 35 | Reject Order | `/collector/orders/{id}/reject` | POST | `/api/cyclex/collector/reject-order/{id}` | POST | ⚠️ **PATH MISMATCH** | Path structure differs |
| 36 | Collector Finish Order | `/collector/orders/{id}/complete` | POST | `/api/cyclex/collector/complete-order/{id}` | POST | ⚠️ **PATH MISMATCH** | Path structure differs |
| 37 | Collector Profile | `/collector/profile` | GET | `/api/cyclex/profile` | GET | ⚠️ **PATH MISMATCH** | Same endpoint for all users |

---

## Summary Statistics

### Status Breakdown

| Status | Count | Percentage |
|--------|-------|------------|
| ✅ Fully Matched | 0 | 0% |
| ⚠️ Path Mismatch | 22 | 59% |
| ⚠️ Method Mismatch | 1 | 3% |
| ⚠️ Path + Method Mismatch | 1 | 3% |
| ⚠️ Path + Status Mismatch | 1 | 3% |
| 🔄 Architectural Difference | 3 | 8% |
| ❌ Missing in Odoo | 9 | 24% |
| **Total** | **37** | **100%** |

### Missing Endpoints (9)

1. `GET /api/cyclex/home/summary` - Home dashboard
2. `GET /api/cyclex/home/summary?include_active_order=true` - Home with active order
3. `GET /api/cyclex/app/config` - App configuration
4. `POST /api/cyclex/orders/items/custom/estimate` - Estimate item price
5. `PUT /api/cyclex/request/{id}/confirm` - Confirm order
6. `GET /api/cyclex/user/addresses` - Get addresses
7. `POST /api/cyclex/user/addresses` - Create address
8. `PUT /api/cyclex/user/addresses/{id}` - Update address
9. `GET /api/cyclex/collector/status` - Collector approval status
10. `GET /api/cyclex/collector/home` - Collector dashboard

**Note:** Collections 14, 15, 16, 18 represent architectural differences (cart system) rather than missing endpoints.

---

## Path Mismatch Patterns

### Pattern 1: Missing `/api/cyclex` Prefix
**Affected:** 22 collections

**Fix Rule:**
```
/auth/* → /api/cyclex/*
/catalog/* → /api/cyclex/*
/orders/* → /api/cyclex/request/* or /api/cyclex/order/*
/user/* → /api/cyclex/*
/wallet/* → /api/cyclex/wallet/*
/collector/* → /api/cyclex/collector/*
```

### Pattern 2: Different Path Structure
**Affected:** 5 collections

- Collection 09-13: `/catalog/categories/{id}/items` → `/api/cyclex/products?category_id={id}`
- Collection 21: `/orders/{id}` → `/api/cyclex/request/details/{id}`
- Collection 22: `/orders/{id}/rate` → `/api/cyclex/order/rate/{id}`
- Collection 34-36: `/collector/orders/{id}/*` → `/api/cyclex/collector/*-order/{id}`

### Pattern 3: Method Mismatch
**Affected:** 1 collection

- Collection 24: `PUT /user/profile` → `POST /api/cyclex/update-profile`

### Pattern 4: Status Value Mismatch
**Affected:** 1 collection

- Collection 20: `status=active` → `status=pending`

---

## Parameter Mismatches

### Collection 03 (Verify OTP)
- **Postman:** `{"phone": "...", "otp": "123456"}`
- **Odoo:** `{"phone": "...", "verification_code": "123456"}`
- **Fix:** Change `otp` → `verification_code`

---

## Architectural Differences

### Cart-Based vs Direct Creation

**Postman Collections (Cart-Based):**
- 14: Add custom item to cart
- 15: Estimate item price
- 16: Add catalog items to cart
- 17: Finish order (checkout)
- 18: Confirm order

**Odoo (Direct Creation):**
- Single endpoint: `POST /api/cyclex/request/create`
- Creates request with all items at once
- No cart concept

**Decision Needed:** Implement cart system OR update Postman collections to match Odoo approach.

---

## Priority Classification

### Critical (Must Fix in Stage 2)
- All 22 path mismatches (blocks all API calls)
- 1 method mismatch (Collection 24)

### High Priority (Stage 3)
- Home summary endpoint (Collection 05, 06)
- Address management endpoints (Collection 27)
- Collector status endpoint (Collection 30)
- Collector home endpoint (Collection 31)

### Medium Priority (Stage 4)
- Architectural alignment (Collections 14-18)
- App config endpoint (Collection 07)

### Low Priority (Optional)
- Estimate item endpoint (Collection 15) - Price calculated automatically
- Confirm order endpoint (Collection 18) - Auto-confirmed on creation

---

## Action Items for Stage 2

1. ✅ Update all 22 collections with path corrections
2. ✅ Fix Collection 24 method (PUT → POST)
3. ✅ Fix Collection 03 parameter name (`otp` → `verification_code`)
4. ✅ Fix Collection 20 status value (`active` → `pending`)
5. ✅ Update test scripts to match Odoo response format

---

**Matrix Generated:** November 13, 2025  
**Next Step:** Stage 2 - Path Normalization

