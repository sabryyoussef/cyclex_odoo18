# 🛠️ CycleX API Alignment Fix Plan

**Objective:** Bring Postman Collections and Odoo Endpoints to 100% alignment  
**Current Status:** 65% compatibility (20 path mismatches, 13 missing endpoints, 2 collections corrected)  
**Target:** 100% alignment with automated testing

---

## Stage 1 — Discovery & Validation (2-3 hours)

**Purpose:** Lock down what's wrong, remove ambiguity, and freeze the scope.

### Tasks

1. **Freeze Current State**
   - Duplicate Postman workspace → `CycleX_Refactor_Backup`
   - Export all 37 collections to JSON backup
   - Document current base_url and environment variables

2. **Extract Odoo Endpoint Inventory**
   - Parse all controller files (`auth_controller.py`, `request_controller.py`, etc.)
   - Extract exact endpoint paths, methods, and parameters
   - Create `ODOO_ENDPOINTS_REFERENCE.md` with:
     - Full path
     - HTTP method
     - Auth requirement
     - Request body schema
     - Response schema
     - Error codes

3. **Deep Map Comparison**
   - Re-map Postman → Odoo with 100% accuracy
   - Confirm:
     - Missing endpoints (exact count: 15)
     - Path mismatches (exact count: 22)
     - Method mismatches (1: PUT vs POST)
     - Status value mismatches (`active` vs `pending`)
     - Architectural conflicts (cart vs direct creation)

4. **Risk Assessment**
   - Identify breaking changes for mobile team
   - Document backward compatibility needs
   - List endpoints that mobile app depends on

### Deliverables

- ✅ `ODOO_ENDPOINTS_REFERENCE.md` - Complete endpoint inventory
- ✅ `VERIFIED_ENDPOINT_MATRIX_V2.md` - Detailed mapping with status codes
- ✅ `PRIORITY_LIST.md` - Ranked list of fixes (Critical → Low)
- ✅ `RISK_NOTES_MOBILE_TEAM.md` - Breaking changes documentation

### Success Criteria

- Zero ambiguity about what needs fixing
- Complete endpoint inventory documented
- Priority list approved by team

---

## Stage 2 — Path Normalization (High Impact, Low Effort) (0.5 Day)

**Purpose:** Fix the biggest blocker — API paths. This unblocks 22 endpoints immediately.

### Work

1. **Create Path Mapping Rules**
   ```
   /auth/*                    → /api/cyclex/*
   /catalog/*                 → /api/cyclex/*
   /catalog/categories/{id}/items → /api/cyclex/products?category_id={id}
   /orders/*                  → /api/cyclex/request/*
   /orders/{id}/rate          → /api/cyclex/order/rate/{id}
   /user/*                    → /api/cyclex/*
   /wallet/*                  → /api/cyclex/wallet/*
   /collector/*               → /api/cyclex/collector/*
   /collector/orders/*        → /api/cyclex/collector/*
   /home/*                    → /api/cyclex/home/* (to be implemented)
   /app/*                     → /api/cyclex/app/* (to be implemented)
   ```

2. **Bulk Update Postman Collections**
   - Script or manual update of all 37 collection files
   - Update `url.path` arrays in JSON
   - Update `url.raw` strings
   - Preserve query parameters and path variables

3. **Update Environment Variables**
   - Verify `{{base_url}}` is correct
   - Add helper variables if needed:
     - `{{api_prefix}}` = `/api/cyclex`
     - `{{full_base_url}}` = `{{base_url}}{{api_prefix}}`

4. **Update Request Examples**
   - Fix all example URLs in collection descriptions
   - Update body examples to match Odoo format
   - Fix status filter values (`active` → `pending`)

5. **Smoke Test**
   - Test 5-10 critical endpoints manually
   - Verify responses match expected format
   - Document any unexpected issues

### Collections to Update

**Authentication (4):**
- 01-login.postman_collection.json
- 02-signup.postman_collection.json
- 03-verify-otp.postman_collection.json
- 04-resend-otp.postman_collection.json

**Categories (6):**
- 08-categories-list.postman_collection.json
- 09-13 category items collections

**Orders (4):**
- 19-my-orders.postman_collection.json
- 20-active-orders.postman_collection.json
- 21-orders-tracking.postman_collection.json
- 22-rating-order.postman_collection.json

**Profile (4):**
- 23-profile.postman_collection.json
- 24-update-profile.postman_collection.json
- 25-profile-wallet.postman_collection.json
- 26-wallet-transactions.postman_collection.json

**Collector (7):**
- 28-login-collector.postman_collection.json
- 29-signup-collector.postman_collection.json
- 32-collector-active-orders.postman_collection.json
- 33-scan-qr.postman_collection.json
- 34-accept-order.postman_collection.json
- 35-reject-order.postman_collection.json
- 36-collector-finish-order.postman_collection.json
- 37-collector-profile.postman_collection.json

### Deliverables

- ✅ Updated Postman Collections v1.1 (all 37 files)
- ✅ Updated environment file with new variables
- ✅ Smoke test report (10 endpoints tested)
- ✅ Status: 22 endpoints fixed and verified

### Success Criteria

- All paths updated correctly
- Manual smoke tests pass
- No broken URLs in collections

---

## Stage 3 — Implement Missing Endpoints in Odoo (1-2 Days)

**Purpose:** Build new endpoints required by UI flows. These are blocking mobile app development.

### Missing Endpoints to Implement

#### 1. Home Summary Endpoint

**Endpoint:** `GET /api/cyclex/home/summary`

**Controller:** `CyclexHomeController` (new file)

**Implementation:**
```python
@http.route('/api/cyclex/home/summary', type='json', auth='user', methods=['GET'], csrf=False)
def get_home_summary(self, **kwargs):
    """
    Get home screen summary for customer
    Returns: balance, stats, active orders count, recent activity
    """
    partner = request.env.user.partner_id
    
    # Get wallet balance
    wallet = request.env['cyclex.wallet'].sudo().search([
        ('user_id', '=', partner.id)
    ], limit=1)
    
    # Get active orders count
    active_orders = request.env['cyclex.request'].sudo().search_count([
        ('customer_id', '=', partner.id),
        ('status', 'in', ['pending', 'assigned'])
    ])
    
    return {
        'success': True,
        'data': {
            'balance': wallet.balance if wallet else 0.0,
            'total_earnings': wallet.total_earned if wallet else 0.0,
            'active_orders_count': active_orders,
            'total_requests': partner.total_requests_created,
            'currency_symbol': 'E£',
        }
    }
```

**Files to Create/Modify:**
- `custom_addons/cyclex/controllers/home_controller.py` (new)
- `custom_addons/cyclex/controllers/__init__.py` (add import)

---

#### 2. App Config Endpoint

**Endpoint:** `GET /api/cyclex/app/config`

**Controller:** `CyclexAppController` (new file)

**Implementation:**
```python
@http.route('/api/cyclex/app/config', type='json', auth='public', methods=['GET'], csrf=False)
def get_app_config(self, **kwargs):
    """
    Get app configuration (version, features, settings)
    Public endpoint for splash screen
    """
    language = kwargs.get('language', 'en')
    
    return {
        'success': True,
        'data': {
            'version': '1.0.0',
            'min_supported_version': '1.0.0',
            'features': {
                'wallet_enabled': True,
                'qr_code_enabled': True,
                'push_notifications': False,  # Phase 7
            },
            'settings': {
                'default_language': language,
                'supported_languages': ['en', 'ar'],
            }
        }
    }
```

**Files to Create/Modify:**
- `custom_addons/cyclex/controllers/app_controller.py` (new)
- `custom_addons/cyclex/controllers/__init__.py` (add import)

---

#### 3. Address Management Endpoints

**Endpoint:** `GET /api/cyclex/user/addresses`  
**Endpoint:** `POST /api/cyclex/user/addresses`  
**Endpoint:** `PUT /api/cyclex/user/addresses/<int:address_id>`

**Controller:** Add to `CyclexAuthController` or create `CyclexAddressController`

**Implementation:**
```python
@http.route('/api/cyclex/user/addresses', type='json', auth='user', methods=['GET'], csrf=False)
def get_addresses(self, **kwargs):
    """Get all saved addresses for user"""
    partner = request.env.user.partner_id
    
    # Get child partners (addresses)
    addresses = request.env['res.partner'].sudo().search([
        ('parent_id', '=', partner.id),
        ('is_address', '=', True)
    ])
    
    address_list = []
    for addr in addresses:
        address_list.append({
            'id': addr.id,
            'label': addr.name,
            'street': addr.street or '',
            'building': addr.street2 or '',
            'floor': addr.comment or '',
            'city': addr.city or '',
            'lat': addr.gps_latitude,
            'lng': addr.gps_longitude,
            'is_default': addr.is_default_address,
        })
    
    return {'success': True, 'data': {'addresses': address_list}}

@http.route('/api/cyclex/user/addresses', type='json', auth='user', methods=['POST'], csrf=False)
def create_address(self, **kwargs):
    """Create new saved address"""
    partner = request.env.user.partner_id
    
    # Create child partner (address)
    address_vals = {
        'parent_id': partner.id,
        'name': kwargs.get('label'),
        'street': kwargs.get('street'),
        'street2': kwargs.get('building'),
        'city': kwargs.get('city'),
        'gps_latitude': kwargs.get('lat'),
        'gps_longitude': kwargs.get('lng'),
        'is_address': True,
        'is_default_address': kwargs.get('is_default', False),
    }
    
    address = request.env['res.partner'].sudo().create(address_vals)
    
    return {
        'success': True,
        'message': 'Address created successfully',
        'data': {'address_id': address.id}
    }

@http.route('/api/cyclex/user/addresses/<int:address_id>', type='json', auth='user', methods=['POST'], csrf=False)
def update_address(self, address_id, **kwargs):
    """Update saved address"""
    partner = request.env.user.partner_id
    
    address = request.env['res.partner'].sudo().browse(address_id)
    
    # Verify ownership
    if address.parent_id.id != partner.id:
        return {
            'success': False,
            'message': 'Access denied',
            'error_code': 'ACCESS_DENIED'
        }
    
    # Update address
    address.sudo().write({
        'name': kwargs.get('label', address.name),
        'street': kwargs.get('street', address.street),
        'street2': kwargs.get('building', address.street2),
        'city': kwargs.get('city', address.city),
        'gps_latitude': kwargs.get('lat', address.gps_latitude),
        'gps_longitude': kwargs.get('lng', address.gps_longitude),
        'is_default_address': kwargs.get('is_default', address.is_default_address),
    })
    
    return {
        'success': True,
        'message': 'Address updated successfully'
    }
```

**Files to Create/Modify:**
- `custom_addons/cyclex/controllers/auth_controller.py` (add methods)
- OR `custom_addons/cyclex/controllers/address_controller.py` (new)
- `custom_addons/cyclex/models/res_partner.py` (add `is_address` field if needed)

---

#### 4. Collector Status Endpoint

**Endpoint:** `GET /api/cyclex/collector/status`

**Controller:** Add to `CyclexCollectorController`

**Implementation:**
```python
@http.route('/api/cyclex/collector/status', type='json', auth='user', methods=['GET'], csrf=False)
def get_collector_status(self, **kwargs):
    """Get collector approval status"""
    partner = request.env.user.partner_id
    
    if partner.cyclex_user_type != 'collector':
        return {
            'success': False,
            'message': 'Not a collector',
            'error_code': 'INVALID_USER_TYPE'
        }
    
    return {
        'success': True,
        'data': {
            'approval_status': partner.collector_approval_status,
            'status_message': self._get_status_message(partner.collector_approval_status),
            'user_id': partner.id,
        }
    }

def _get_status_message(self, status):
    """Get human-readable status message"""
    messages = {
        'pending': 'Your registration is pending admin approval',
        'approved': 'Your account is approved and active',
        'rejected': 'Your registration was rejected. Please contact support.',
        'suspended': 'Your account is temporarily suspended',
    }
    return messages.get(status, 'Unknown status')
```

**Files to Modify:**
- `custom_addons/cyclex/controllers/collector_controller.py` (add method)

---

#### 5. Collector Home Endpoint

**Endpoint:** `GET /api/cyclex/collector/home`

**Controller:** Add to `CyclexCollectorController`

**Implementation:**
```python
@http.route('/api/cyclex/collector/home', type='json', auth='user', methods=['GET'], csrf=False)
def get_collector_home(self, **kwargs):
    """Get collector dashboard summary"""
    partner = request.env.user.partner_id
    
    if partner.cyclex_user_type != 'collector':
        return {
            'success': False,
            'message': 'Not a collector',
            'error_code': 'INVALID_USER_TYPE'
        }
    
    # Get available orders count
    available_orders = request.env['cyclex.request'].sudo().search_count([
        ('status', '=', 'pending')
    ])
    
    # Get assigned orders count
    assigned_orders = request.env['cyclex.request'].sudo().search_count([
        ('collector_id', '=', partner.id),
        ('status', '=', 'assigned')
    ])
    
    # Get total earnings (from commissions)
    total_earnings = sum(
        request.env['cyclex.commission'].sudo().search([
            ('collector_id', '=', partner.id)
        ]).mapped('amount')
    )
    
    return {
        'success': True,
        'data': {
            'available_orders_count': available_orders,
            'assigned_orders_count': assigned_orders,
            'total_orders_completed': partner.total_requests_completed,
            'total_earnings': total_earnings,
            'average_rating': partner.average_rating or 0,
            'approval_status': partner.collector_approval_status,
            'currency_symbol': 'E£',
        }
    }
```

**Files to Modify:**
- `custom_addons/cyclex/controllers/collector_controller.py` (add method)

---

#### 6. Order Confirmation Endpoint (Optional)

**Endpoint:** `POST /api/cyclex/request/confirm/<int:request_id>`

**Decision:** Only implement if mobile app requires explicit confirmation step.

**Implementation:** (if needed)
```python
@http.route('/api/cyclex/request/confirm/<int:request_id>', type='json', auth='user', methods=['POST'], csrf=False)
def confirm_request(self, request_id, **kwargs):
    """Confirm and finalize order (if confirmation step is required)"""
    partner = request.env.user.partner_id
    
    req = request.env['cyclex.request'].sudo().browse(request_id)
    
    # Verify ownership
    if req.customer_id.id != partner.id:
        return {
            'success': False,
            'message': 'Access denied',
            'error_code': 'ACCESS_DENIED'
        }
    
    # Mark as confirmed (if status field exists)
    req.sudo().write({'status': 'confirmed'})
    
    return {
        'success': True,
        'message': 'Order confirmed successfully'
    }
```

**Files to Modify:**
- `custom_addons/cyclex/controllers/request_controller.py` (add method)

---

### Work Breakdown

**Day 1:**
- Morning: Implement home summary + app config (2-3 hours)
- Afternoon: Implement address management (3-4 hours)
- Evening: Testing + documentation (1 hour)

**Day 2:**
- Morning: Implement collector status + collector home (2-3 hours)
- Afternoon: Optional order confirmation (if needed) (1-2 hours)
- Evening: Integration testing + bug fixes (2-3 hours)

### Deliverables

- ✅ 5 new endpoints implemented and tested
- ✅ Updated `API_DOCUMENTATION.md` with new endpoints
- ✅ Security ACL checks added
- ✅ Unit tests for each endpoint (if test framework exists)
- ✅ Integration test results

### Success Criteria

- All 5 endpoints return correct responses
- Security checks pass (auth required, ownership verified)
- No breaking changes to existing endpoints
- Documentation updated

---

## Stage 4 — Align Logic Differences (Cart vs Direct Flow) (0.5 Day)

**Purpose:** Resolve architecture conflict between cart-based and direct creation.

### Decision Required

**Option A — Implement Full Cart System (4-6 days)**
- Pros: Matches Postman collections exactly
- Cons: Significant backend changes, more complex
- Effort: High

**Option B — Update Postman to Match Odoo (Recommended) (0.5 day)**
- Pros: Simple, aligns with existing backend
- Cons: Postman collections need updates
- Effort: Low

### Recommended: Option B

**Work:**

1. **Update Collection 14 (Add New Item)**
   - Current: `POST /orders/items/custom` (multipart)
   - New: `POST /api/cyclex/request/create` (with custom item data)
   - Update body to match Odoo format:
     ```json
     {
       "category_id": 1,
       "product_id": null,  // null for custom items
       "quantity": 10,
       "weight": 5.5,
       "pickup_date": "2025-11-20",
       "photo_1": "base64_encoded_image",
       "item_name": "Custom item name",
       "gps_latitude": 30.0444,
       "gps_longitude": 31.2357
     }
     ```

2. **Remove Collection 15 (Estimate Item)**
   - Mark as deprecated
   - Or update to use product price calculation
   - Note: Odoo calculates price automatically on creation

3. **Update Collection 16 (Add Other Items)**
   - Current: `POST /orders/items` (add to cart)
   - New: Document that items are added in single request creation
   - Update to show example of multiple items in one request

4. **Update Collection 17 (Finish Order)**
   - Already correct: `POST /api/cyclex/request/create`
   - Update documentation to clarify it creates order directly

5. **Update Collection 18 (Confirm Order)**
   - Option A: Remove if not needed
   - Option B: Keep for future use (mark as TODO)
   - Option C: Implement confirmation endpoint in Odoo (Stage 3, optional)

6. **Update Documentation**
   - Add note about direct creation approach
   - Update flow diagrams
   - Remove cart-related terminology

### Deliverables

- ✅ Updated Postman collections (14, 15, 16, 17, 18)
- ✅ Updated API documentation
- ✅ Architecture decision document
- ✅ Migration guide for mobile team

### Success Criteria

- All collections align with Odoo architecture
- No cart-related endpoints remain
- Documentation reflects direct creation flow

---

## Stage 5 — Apply Method Corrections (0.5 Day)

**Purpose:** Fix the low-level mismatches that break requests.

### Changes

1. **Method Correction**
   - Collection 24: Change `PUT /user/profile` → `POST /api/cyclex/update-profile`
   - Update HTTP method in Postman collection

2. **Status Value Normalization**
   - Collection 20: Change `status=active` → `status=pending`
   - Update all status filters to match Odoo:
     - `active` → `pending` (for pending orders)
     - `assigned` → `assigned` (already correct)
     - `completed` → `collected` (for completed orders)

3. **ID Format Normalization**
   - Ensure all path variables use integer format
   - Update examples: `:order_id`, `:address_id`, `:request_id`

4. **JSON Payload Alignment**
   - Verify all request bodies match Odoo expectations
   - Update field names if needed:
     - `verification_code` (Postman) → `verification_code` (Odoo) ✅
     - `otp` (Postman) → `verification_code` (Odoo) ⚠️
   - Fix Collection 03: Change `otp` → `verification_code`

5. **Response Format Alignment**
   - Ensure test scripts expect correct response structure
   - Update token extraction scripts if needed
   - Odoo returns: `{success: true, data: {...}}`
   - Postman expects: `{token: "...", user: {...}}`
   - **Fix:** Update test scripts to match Odoo format

### Detailed Fixes

**Collection 03 (Verify OTP):**
```json
// Current
{
  "phone": "01000000000",
  "otp": "123456"
}

// Fixed
{
  "phone": "01000000000",
  "verification_code": "123456"
}
```

**Collection 24 (Update Profile):**
```json
// Current: PUT method
// Fixed: POST method
// Path: /api/cyclex/update-profile
```

**Collection 20 (Active Orders):**
```json
// Current query: ?status=active
// Fixed query: ?status=pending
```

**Test Script Updates:**
```javascript
// Current (Collection 01)
const json = pm.response.json();
if (json.token) {
    pm.environment.set("auth_token", json.token);
}

// Fixed (Odoo format)
const json = pm.response.json();
if (json.success && json.data && json.data.user_id) {
    // Odoo doesn't return token in response, uses session
    // Store user_id instead
    pm.environment.set("user_id", json.data.user_id);
}
```

### Deliverables

- ✅ All method corrections applied
- ✅ Status values normalized
- ✅ Test scripts updated
- ✅ Response format aligned

### Success Criteria

- All HTTP methods match Odoo
- All status filters work correctly
- Test scripts extract correct values

---

## Stage 6 — Automated Testing with n8n (1 Day)

**Purpose:** Build reusable test suite for regression testing.

### Workflow Setup

1. **Create n8n Workflow: "CycleX API Test Pipeline"**

   **Structure:**
   ```
   Start → Set Variables → Test Auth → Test Categories → Test Orders → Test Profile → Test Wallet → Test Collector → Report Results
   ```

2. **HTTP Request Nodes**

   **Node 1: Login**
   - Method: POST
   - URL: `{{base_url}}/api/cyclex/login`
   - Body: `{phone: "test_user", password: "test123"}`
   - Store session cookie

   **Node 2: Get Categories**
   - Method: GET
   - URL: `{{base_url}}/api/cyclex/categories`
   - Use session from Node 1
   - Validate: `success === true`

   **Node 3: Create Request**
   - Method: POST
   - URL: `{{base_url}}/api/cyclex/request/create`
   - Body: Test request data
   - Validate: `success === true` and `data.request_id` exists

   **Node 4: Get Profile**
   - Method: GET
   - URL: `{{base_url}}/api/cyclex/profile`
   - Validate: `success === true` and `data.user_id` exists

   **Node 5: Get Wallet**
   - Method: GET
   - URL: `{{base_url}}/api/cyclex/wallet/balance`
   - Validate: `success === true` and `data.balance` is number

   **Node 6: Collector Available Orders**
   - Method: GET
   - URL: `{{base_url}}/api/cyclex/collector/available-orders`
   - Validate: `success === true`

3. **Validation Logic**

   Each HTTP node includes:
   - Status code check (200, 201, etc.)
   - Response structure validation
   - Error code checking
   - Data type validation

4. **Error Handling**

   - If any node fails → log error
   - Continue to next test (don't stop pipeline)
   - Collect all errors for final report

5. **Reporting**

   **Final Node: Send Report**
   - Format: Markdown or JSON
   - Include:
     - Test timestamp
     - Pass/fail count
     - Failed endpoints list
     - Response times
   - Send to:
     - Slack channel
     - Email
     - Save to file

### n8n Workflow Configuration

**Environment Variables:**
```json
{
  "base_url": "http://localhost:10018",
  "test_phone": "01234567890",
  "test_password": "test123",
  "slack_webhook": "https://hooks.slack.com/..."
}
```

**Schedule:**
- Daily at 2 AM
- On-demand trigger
- On git push (webhook)

### Deliverables

- ✅ n8n workflow JSON export
- ✅ Test data setup script
- ✅ Slack integration configured
- ✅ Test report template
- ✅ Documentation: "How to Run Tests"

### Success Criteria

- All critical endpoints tested automatically
- Reports generated successfully
- Alerts sent on failure

---

## Stage 7 — Documentation & Handover (0.5 Day)

**Purpose:** Finalize and package everything for the mobile team + backend team.

### Deliverables

1. **API_DOCUMENTATION_v2.md**
   - Complete endpoint reference
   - All 37 endpoints documented
   - Request/response examples
   - Error codes
   - Authentication guide

2. **Postman Export "CycleX_API_v2"**
   - All 37 collections updated
   - Environment file included
   - Pre-request scripts
   - Test scripts
   - Example responses

3. **CHANGELOG.md**
   - List of all changes
   - Breaking changes highlighted
   - Migration guide
   - Version history

4. **KNOWN_ISSUES.md**
   - Current limitations
   - Future improvements
   - Workarounds

5. **TEST_REPORT.md**
   - First automated test run results
   - Pass/fail summary
   - Performance metrics

6. **MOBILE_TEAM_HANDOFF.md**
   - Quick start guide
   - Common issues
   - Support contacts

### Documentation Structure

```
docs/
├── API_DOCUMENTATION_v2.md
├── CHANGELOG.md
├── KNOWN_ISSUES.md
├── TEST_REPORT.md
├── MOBILE_TEAM_HANDOFF.md
└── postman/
    ├── CycleX_API_v2.postman_collection.json
    └── CycleX-Local.postman_environment.json
```

### Success Criteria

- All documentation complete
- Postman collections exported
- Mobile team can start integration
- Backend team has clear reference

---

## ⚡ High-Level Timeline

| Stage | Duration | Dependencies | Priority |
|-------|----------|--------------|----------|
| Stage 1 | 2-3 hours | None | Critical |
| Stage 2 | 0.5 day | Stage 1 | Critical |
| Stage 3 | 1-2 days | Stage 2 | High |
| Stage 4 | 0.5 day | Stage 2 | Medium |
| Stage 5 | 0.5 day | Stage 2 | Medium |
| Stage 6 | 1 day | Stage 3, 4, 5 | Low |
| Stage 7 | 0.5 day | All stages | Low |

**Total Estimated Time:** 4-6 days

---

## 📌 Final Output

You walk away with:

✅ **100% aligned API set** (37/37 endpoints working)  
✅ **Clean Postman workspace** (all paths corrected)  
✅ **5 missing endpoints implemented** (home, config, addresses, collector status/home)  
✅ **Automated testing in n8n** (daily regression tests)  
✅ **Updated documentation** (v2 with all changes)  
✅ **Smooth handoff** (mobile team ready to integrate)

---

## 🚨 Risk Mitigation

### Risk 1: Breaking Mobile App Integration
**Mitigation:** 
- Document all breaking changes in CHANGELOG
- Provide migration guide
- Maintain backward compatibility where possible

### Risk 2: Missing Endpoints Block Mobile Development
**Mitigation:**
- Prioritize Stage 3 (missing endpoints) early
- Implement critical endpoints first (home, addresses)
- Provide workarounds for non-critical endpoints

### Risk 3: Test Coverage Gaps
**Mitigation:**
- Test all 37 endpoints manually in Stage 2
- Automated tests cover critical paths
- Mobile team provides feedback on missing tests

---

## 📋 Quick Reference Checklist

### Pre-Execution
- [ ] Backup current Postman collections
- [ ] Review comparison report
- [ ] Get team approval on architecture decision (Stage 4)
- [ ] Set up test environment

### During Execution
- [ ] Stage 1: Complete endpoint inventory
- [ ] Stage 2: Fix all 22 path mismatches
- [ ] Stage 3: Implement 5 missing endpoints
- [ ] Stage 4: Align architecture (cart vs direct)
- [ ] Stage 5: Fix method/status mismatches
- [ ] Stage 6: Set up automated testing
- [ ] Stage 7: Complete documentation

### Post-Execution
- [ ] Verify all endpoints work
- [ ] Run full test suite
- [ ] Hand off to mobile team
- [ ] Monitor for issues

---

**Plan Created:** November 13, 2025  
**Status:** Ready for Execution  
**Next Step:** Begin Stage 1 (Discovery & Validation)

