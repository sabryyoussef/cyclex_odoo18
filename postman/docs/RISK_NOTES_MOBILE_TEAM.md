# Risk Notes for Mobile Team

**Generated:** November 13, 2025  
**Purpose:** Document breaking changes and risks for mobile app integration

---

## 🚨 Critical Breaking Changes

### 1. All API Paths Changed

**Before (Postman Collections):**
```
POST /auth/login
GET /catalog/categories
GET /orders
GET /user/profile
GET /wallet
```

**After (Odoo Backend):**
```
POST /api/cyclex/login
GET /api/cyclex/categories
GET /api/cyclex/request/list
GET /api/cyclex/profile
GET /api/cyclex/wallet/balance
```

**Impact:** ⚠️ **HIGH** - All API calls will fail until paths are updated

**Action Required:**
- Update base URL in mobile app
- Add `/api/cyclex` prefix to all endpoints
- Test all API calls after update

**Timeline:** Must be fixed before mobile app can connect to backend

---

### 2. Base URL Mismatch

**Postman Environment:**
- `base_url`: `http://localhost:8000/api`

**Odoo Documentation:**
- Base URL: `http://localhost:10018`

**Impact:** ⚠️ **HIGH** - API calls will fail with connection errors

**Action Required:**
- Confirm correct base URL with backend team
- Update mobile app configuration
- Test connectivity

**Timeline:** Must be resolved before testing

---

### 3. Response Format Differences

**Postman Test Scripts Expect:**
```json
{
  "token": "abc123",
  "user": {
    "id": 123
  }
}
```

**Odoo Actually Returns:**
```json
{
  "success": true,
  "data": {
    "user_id": 123,
    "name": "John Doe"
  }
}
```

**Impact:** ⚠️ **MEDIUM** - Token extraction and user data parsing will fail

**Action Required:**
- Update response parsing logic
- Odoo uses session-based auth (no token in response)
- Extract `user_id` from `data.user_id` instead of `user.id`

**Timeline:** Fix during API integration phase

---

## ⚠️ Medium Risk Changes

### 4. HTTP Method Mismatch

**Update Profile Endpoint:**
- Postman: `PUT /user/profile`
- Odoo: `POST /api/cyclex/update-profile`

**Impact:** ⚠️ **MEDIUM** - Profile update will fail

**Action Required:**
- Change HTTP method from PUT to POST
- Update endpoint path

---

### 5. Parameter Name Changes

**Verify OTP:**
- Postman: `{"phone": "...", "otp": "123456"}`
- Odoo: `{"phone": "...", "verification_code": "123456"}`

**Impact:** ⚠️ **MEDIUM** - OTP verification will fail

**Action Required:**
- Change parameter name from `otp` to `verification_code`

---

### 6. Status Value Differences

**Active Orders:**
- Postman: `GET /orders?status=active`
- Odoo: `GET /api/cyclex/request/list?status=pending`

**Impact:** ⚠️ **LOW** - Will return wrong results

**Action Required:**
- Use `pending` instead of `active` for pending orders
- Status values in Odoo:
  - `pending` - Pending collector acceptance
  - `assigned` - Assigned to collector
  - `collected` - Completed
  - `cancelled` - Cancelled

---

## 🔄 Architectural Changes

### 7. Cart System vs Direct Creation

**Postman Collections Assume:**
1. Add items to cart (`POST /orders/items`)
2. Add custom items (`POST /orders/items/custom`)
3. Finish order (`POST /orders`)
4. Confirm order (`PUT /orders/{id}/confirm`)

**Odoo Uses:**
1. Create request directly (`POST /api/cyclex/request/create`)

**Impact:** ⚠️ **HIGH** - Order creation flow completely different

**Action Required:**
- **Option A:** Implement cart system in mobile app (complex)
- **Option B:** Update mobile app to use direct creation (recommended)
- Collect all items first, then send single request

**Timeline:** Major refactoring required

---

### 8. Missing Endpoints

**Endpoints Not Available in Odoo:**
1. `GET /home/summary` - Home dashboard
2. `GET /app/config` - App configuration
3. `GET/POST/PUT /user/addresses` - Address management
4. `GET /collector/status` - Collector approval status
5. `GET /collector/home` - Collector dashboard
6. `POST /orders/items/custom/estimate` - Estimate price
7. `PUT /orders/{id}/confirm` - Confirm order

**Impact:** ⚠️ **MEDIUM** - Some screens won't work

**Action Required:**
- **Workaround:** Implement missing endpoints in Odoo (Stage 3)
- **Alternative:** Modify mobile app to work without these endpoints
- **Timeline:** Endpoints will be implemented in 1-2 days

---

## 📋 Migration Checklist for Mobile Team

### Before Integration

- [ ] Confirm base URL with backend team
- [ ] Review Odoo API documentation
- [ ] Understand response format differences
- [ ] Plan for session-based authentication

### During Integration

- [ ] Update all API paths with `/api/cyclex` prefix
- [ ] Fix HTTP methods (PUT → POST for profile update)
- [ ] Fix parameter names (`otp` → `verification_code`)
- [ ] Update status values (`active` → `pending`)
- [ ] Update response parsing logic
- [ ] Implement session-based auth (no token extraction)

### After Integration

- [ ] Test all endpoints
- [ ] Verify response formats
- [ ] Test error handling
- [ ] Document any issues

---

## 🛡️ Mitigation Strategies

### 1. Use Environment Configuration

**Mobile App:**
```dart
// config.dart
class ApiConfig {
  static const String baseUrl = 'http://localhost:10018';
  static const String apiPrefix = '/api/cyclex';
  
  static String getFullUrl(String endpoint) {
    return '$baseUrl$apiPrefix$endpoint';
  }
}
```

**Benefits:**
- Easy to update base URL
- Centralized path management
- Easy to switch between dev/staging/prod

---

### 2. Create API Service Layer

**Mobile App:**
```dart
// api_service.dart
class CyclexApiService {
  final String baseUrl = ApiConfig.baseUrl;
  
  Future<Map<String, dynamic>> login(String phone, String password) async {
    final response = await http.post(
      Uri.parse('${baseUrl}/api/cyclex/login'),
      body: jsonEncode({
        'phone': phone,
        'password': password,
      }),
    );
    
    final data = jsonDecode(response.body);
    // Handle Odoo response format
    if (data['success'] == true) {
      return data['data'];
    }
    throw Exception(data['message']);
  }
}
```

**Benefits:**
- Centralized API calls
- Consistent error handling
- Easy to update when endpoints change

---

### 3. Response Wrapper

**Mobile App:**
```dart
// response_wrapper.dart
class ApiResponse<T> {
  final bool success;
  final String? message;
  final T? data;
  final String? errorCode;
  
  ApiResponse.fromJson(Map<String, dynamic> json, T Function(dynamic) fromJsonT) {
    success = json['success'] ?? false;
    message = json['message'];
    errorCode = json['error_code'];
    data = json['data'] != null ? fromJsonT(json['data']) : null;
  }
}
```

**Benefits:**
- Consistent response handling
- Type-safe data extraction
- Error code support

---

## 📞 Support Contacts

**Backend Team:**
- Odoo Module: `cyclex_odoo18/custom_addons/cyclex/`
- API Documentation: `API_DOCUMENTATION.md`
- Endpoint Reference: `ODOO_ENDPOINTS_REFERENCE.md`

**Issues to Report:**
- Endpoint not working
- Response format unexpected
- Error codes not documented
- Missing endpoints blocking development

---

## ⏰ Timeline Impact

### Immediate (Before Mobile Integration)
- ✅ Path fixes (Stage 2) - 0.5 day
- ✅ Base URL confirmation - 1 hour

### Short-term (During Mobile Integration)
- ✅ Missing endpoints (Stage 3) - 1-2 days
- ✅ Architecture alignment (Stage 4) - 0.5 day

### Long-term (After Integration)
- ✅ Automated testing (Stage 6) - 1 day
- ✅ Documentation updates (Stage 7) - 0.5 day

---

## 🎯 Recommendations

1. **Wait for Stage 2 completion** before starting mobile integration
   - All paths will be fixed
   - Base URL will be confirmed
   - Response formats documented

2. **Use workarounds** for missing endpoints
   - Home screen: Fetch data from multiple endpoints
   - Addresses: Store locally until endpoint ready
   - App config: Hardcode values

3. **Implement direct creation** instead of cart system
   - Simpler implementation
   - Matches Odoo backend
   - Faster development

4. **Test incrementally**
   - Start with authentication
   - Then categories/products
   - Then orders
   - Finally collector features

---

**Risk Notes Generated:** November 13, 2025  
**Status:** Ready for mobile team review

