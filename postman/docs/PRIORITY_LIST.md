# Priority List - CycleX API Alignment

**Generated:** November 13, 2025  
**Purpose:** Ranked list of fixes from Critical to Low priority

---

## 🔴 Critical Priority (Stage 2 - 0.5 Day)

**Impact:** Blocks all API calls  
**Effort:** Low (bulk path updates)

### Path Mismatches (22 collections)
All endpoints missing `/api/cyclex` prefix:

1. ✅ Collection 01: `/auth/login` → `/api/cyclex/login`
2. ✅ Collection 02: `/auth/register` → `/api/cyclex/register`
3. ✅ Collection 03: `/auth/verify-otp` → `/api/cyclex/verify` + fix param name
4. ✅ Collection 04: `/auth/resend-otp` → `/api/cyclex/resend-code`
5. ✅ Collection 08: `/catalog/categories` → `/api/cyclex/categories`
6. ✅ Collection 09-13: `/catalog/categories/{id}/items` → `/api/cyclex/products?category_id={id}`
7. ✅ Collection 17: `/orders` → `/api/cyclex/request/create`
8. ✅ Collection 19: `/orders` → `/api/cyclex/request/list`
9. ✅ Collection 20: `/orders?status=active` → `/api/cyclex/request/list?status=pending`
10. ✅ Collection 21: `/orders/{id}` → `/api/cyclex/request/details/{id}`
11. ✅ Collection 22: `/orders/{id}/rate` → `/api/cyclex/order/rate/{id}`
12. ✅ Collection 23: `/user/profile` → `/api/cyclex/profile`
13. ✅ Collection 24: `/user/profile` → `/api/cyclex/update-profile` + PUT → POST
14. ✅ Collection 25: `/wallet` → `/api/cyclex/wallet/balance`
15. ✅ Collection 26: `/wallet/transactions` → `/api/cyclex/wallet/transactions`
16. ✅ Collection 28: `/auth/login` → `/api/cyclex/login`
17. ✅ Collection 29: `/auth/register` → `/api/cyclex/register`
18. ✅ Collection 32: `/collector/orders` → `/api/cyclex/collector/available-orders`
19. ✅ Collection 33: `/collector/orders/scan-qr` → `/api/cyclex/collector/scan-qr`
20. ✅ Collection 34: `/collector/orders/{id}/accept` → `/api/cyclex/collector/accept-order/{id}`
21. ✅ Collection 35: `/collector/orders/{id}/reject` → `/api/cyclex/collector/reject-order/{id}`
22. ✅ Collection 36: `/collector/orders/{id}/complete` → `/api/cyclex/collector/complete-order/{id}`
23. ✅ Collection 37: `/collector/profile` → `/api/cyclex/profile`

### Method Mismatch (1 collection)
24. ✅ Collection 24: Change HTTP method from PUT to POST

### Parameter Name Fix (1 collection)
25. ✅ Collection 03: Change `otp` → `verification_code` in request body

### Status Value Fix (1 collection)
26. ✅ Collection 20: Change `status=active` → `status=pending`

---

## 🟠 High Priority (Stage 3 - 1-2 Days)

**Impact:** Blocks specific UI screens  
**Effort:** Medium (new endpoint implementation)

### Missing Endpoints - User App

1. **Home Summary** (Collections 05, 06)
   - Endpoint: `GET /api/cyclex/home/summary`
   - Impact: Home screen won't load
   - Effort: 2-3 hours
   - Dependencies: Wallet model, Request model

2. **Address Management** (Collection 27)
   - Endpoints: 
     - `GET /api/cyclex/user/addresses`
     - `POST /api/cyclex/user/addresses`
     - `PUT /api/cyclex/user/addresses/{id}`
   - Impact: Can't save/manage addresses for orders
   - Effort: 3-4 hours
   - Dependencies: res.partner model (child addresses)

### Missing Endpoints - Collector App

3. **Collector Status** (Collection 30)
   - Endpoint: `GET /api/cyclex/collector/status`
   - Impact: Collector can't check approval status
   - Effort: 1 hour
   - Dependencies: res.partner model (collector_approval_status field)

4. **Collector Home** (Collection 31)
   - Endpoint: `GET /api/cyclex/collector/home`
   - Impact: Collector dashboard won't load
   - Effort: 2-3 hours
   - Dependencies: Request model, Commission model

---

## 🟡 Medium Priority (Stage 4 - 0.5 Day)

**Impact:** Architectural alignment  
**Effort:** Low-Medium (decision + updates)

### Architectural Differences

1. **Cart-Based System** (Collections 14, 15, 16, 18)
   - Current: Postman assumes cart workflow
   - Odoo: Direct request creation
   - Decision: Update Postman to match Odoo (recommended)
   - Effort: 0.5 day
   - Impact: Collections 14, 15, 16, 18 need updates

2. **App Config** (Collection 07)
   - Endpoint: `GET /api/cyclex/app/config`
   - Impact: Splash screen configuration
   - Effort: 1-2 hours
   - Priority: Can use hardcoded values in mobile app as workaround

---

## 🟢 Low Priority (Optional)

**Impact:** Nice to have features  
**Effort:** Low

1. **Estimate Item** (Collection 15)
   - Endpoint: `POST /api/cyclex/orders/items/custom/estimate`
   - Note: Price calculated automatically on creation
   - Workaround: Use product price directly
   - Effort: 2-3 hours (if needed)

2. **Confirm Order** (Collection 18)
   - Endpoint: `PUT /api/cyclex/request/{id}/confirm`
   - Note: Orders auto-confirmed on creation
   - Workaround: Remove confirmation step
   - Effort: 1-2 hours (if needed)

---

## Summary by Stage

### Stage 2 (Critical - 0.5 Day)
- ✅ 22 path mismatches
- ✅ 1 method mismatch
- ✅ 1 parameter name fix
- ✅ 1 status value fix
- **Total:** 25 fixes
- **Result:** 22 endpoints working (59% → 59% but functional)

### Stage 3 (High - 1-2 Days)
- ✅ 4 missing endpoints
- **Total:** 4 new endpoints
- **Result:** +4 endpoints (59% → 73% coverage)

### Stage 4 (Medium - 0.5 Day)
- ✅ Architectural alignment
- ✅ 1 optional endpoint
- **Total:** 5 collections updated
- **Result:** 100% alignment achieved

---

## Risk Assessment

### High Risk Items
- **Path mismatches:** All 22 collections will fail until fixed
- **Home summary:** Blocks main user screen
- **Address management:** Blocks order creation flow

### Medium Risk Items
- **Collector endpoints:** Blocks collector app functionality
- **Architectural differences:** May confuse mobile team

### Low Risk Items
- **App config:** Can be hardcoded
- **Estimate/Confirm:** Workarounds available

---

## Recommended Execution Order

1. **Day 1 Morning:** Stage 2 (Path fixes) - Unblock all endpoints
2. **Day 1 Afternoon:** Stage 3 (Home + Addresses) - Unblock user flow
3. **Day 2 Morning:** Stage 3 (Collector endpoints) - Unblock collector flow
4. **Day 2 Afternoon:** Stage 4 (Architecture alignment) - Final alignment
5. **Day 3:** Testing + Documentation

---

**Priority List Generated:** November 13, 2025  
**Next Action:** Begin Stage 2 - Path Normalization

