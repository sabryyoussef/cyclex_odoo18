# CycleX User Roles & Permissions Guide 🔐

**Complete reference for user roles, permissions, and access control**

**Version:** 1.0  
**Date:** October 2025

---

## 🎯 Overview

CycleX implements **3 security groups** with different access levels:

1. **CycleX User** - Mobile app users (customers & collectors)
2. **CycleX Manager** - System managers
3. **CycleX Admin** - Full administrators

---

## 👥 User Types

### Mobile App Users (via API):

| User Type | Description | Permissions |
|-----------|-------------|-------------|
| **Customer** | Sells recyclable items | Create requests, view own data, manage wallet |
| **Collector** | Picks up items | View available orders, accept/reject, scan QR codes |

### Backend Users (Odoo Interface):

| Role | Description | Access Level |
|------|-------------|--------------|
| **Manager** | Operational staff | Manage master data, view reports |
| **Admin** | System administrator | Full access, approvals, system config |

---

## 🔒 Security Groups

### 1. CycleX User (`group_cyclex_user`)

**XML ID:** `cyclex.group_cyclex_user`

**Members:**
- All mobile app users (customers & collectors)
- Automatically assigned on registration

**Permissions:**

#### Read Access:
- ✅ Own profile (`res.partner`)
- ✅ Own requests (customers)
- ✅ Own wallet and transactions (customers)
- ✅ Own commissions (collectors)
- ✅ Assigned requests (collectors)
- ✅ Categories and products (all)
- ✅ Working areas (all)

#### Create Access:
- ✅ Recycling requests (customers only)
- ✅ Wallet transactions (via API only)

#### Update Access:
- ✅ Own profile (name, email, language, FCM token)
- ✅ Own requests (before assigned)
- ✅ Rate completed orders (customers)

#### Delete Access:
- ❌ No delete permissions (soft delete only)

**Access via:**
- 📱 Mobile API only
- ❌ No Odoo backend access

---

### 2. CycleX Manager (`group_cyclex_manager`)

**XML ID:** `cyclex.group_cyclex_manager`

**Members:**
- Operational staff
- Customer support team
- Data managers

**Permissions:**

#### Read Access:
- ✅ All categories, products, working areas
- ✅ All requests and orders
- ✅ All customers and collectors
- ✅ All wallets and transactions
- ✅ All commissions
- ✅ Reports and analytics

#### Create Access:
- ✅ Categories
- ✅ Products
- ✅ Working areas
- ✅ Manual requests (on behalf of customers)

#### Update Access:
- ✅ Categories, products, working areas
- ✅ Customer profiles
- ✅ Collector profiles (except verification)
- ✅ Request details (except financial)

#### Delete Access:
- ✅ Archive categories, products (soft delete)
- ❌ Cannot delete requests, wallets, transactions

**Access via:**
- 🖥️ Odoo backend interface
- 📊 Reports and dashboards

**Cannot Do:**
- ❌ Verify collectors
- ❌ Approve withdrawals
- ❌ Modify commissions
- ❌ Access system parameters
- ❌ Manage security groups

---

### 3. CycleX Admin (`group_cyclex_admin`)

**XML ID:** `cyclex.group_cyclex_admin`

**Members:**
- System administrators
- Super users
- Technical team

**Permissions:**

#### Full Access:
- ✅ All models (read, create, update, delete)
- ✅ All records
- ✅ All menus and views
- ✅ System parameters
- ✅ Security settings
- ✅ Scheduled actions (cron jobs)

#### Special Powers:
- ✅ **Verify collectors** (enable collector accounts)
- ✅ **Approve/reject withdrawals** (financial approvals)
- ✅ **Modify commissions** (if needed)
- ✅ **Manual wallet credits** (bonuses, corrections)
- ✅ **Access technical menus** (Settings → Technical)
- ✅ **Manage integrations** (SMS Misr, Firebase)

**Access via:**
- 🖥️ Full Odoo backend access
- 🔧 Technical settings
- 📊 All reports and analytics

---

## 📋 Permission Matrix

### Model Access Rights

| Model | User | Manager | Admin |
|-------|------|---------|-------|
| **res.partner** (own) | Read, Update | Read, Update | Full |
| **res.partner** (others) | No | Read | Full |
| **cyclex.category** | Read | Full | Full |
| **cyclex.product** | Read | Full | Full |
| **cyclex.working.area** | Read | Full | Full |
| **cyclex.request** (own) | Full | Read, Update | Full |
| **cyclex.request** (others) | No | Read | Full |
| **cyclex.wallet** (own) | Read | Read | Full |
| **cyclex.wallet** (others) | No | Read | Full |
| **cyclex.wallet.transaction** (own) | Read | Read | Full |
| **cyclex.commission** (own) | Read | Read | Full |
| **cyclex.commission** (others) | No | Read | Full |

**Legend:**
- **Full** = Create, Read, Update, Delete
- **Read, Update** = Can view and edit, cannot delete
- **Read** = View only
- **No** = No access

---

## 🎭 Field-Level Security

### Sensitive Fields (Admin Only):

#### res.partner:
- `collector_verified` - Only admins can verify
- `commission_rate` - Only admins can modify

#### cyclex.wallet.transaction:
- `withdrawal_status` - Only admins can approve/reject
- `approved_by` - System-managed
- `approval_date` - System-managed

#### cyclex.commission:
- `commission_amount` - Computed, read-only
- `payment_date` - Only admins can set

---

## 🚪 Menu Access Control

### CycleX User (Mobile Only):
```
No Odoo menu access
All interactions via mobile API
```

### CycleX Manager:
```
CycleX (Main Menu)
├── Dashboard
├── Recycling Requests
│   ├── All Requests
│   └── Pending Orders
├── Customers
├── Collectors (Read Only)
├── Configuration
│   ├── Categories
│   ├── Products
│   └── Working Areas
└── Reports
    ├── Requests Analysis
    └── Customer Statistics
```

### CycleX Admin:
```
CycleX (Main Menu)
├── Dashboard
├── Recycling Requests
│   ├── All Requests
│   ├── Pending Orders
│   ├── Assigned Orders
│   └── Completed Orders
├── Customers
├── Collectors
│   ├── All Collectors
│   ├── Pending Verification
│   └── Verified Collectors
├── Financial
│   ├── Wallets
│   ├── Transactions
│   ├── Pending Withdrawals ⚠️
│   └── Commissions
├── Configuration
│   ├── Categories
│   ├── Products
│   ├── Working Areas
│   └── System Parameters ⚠️
└── Reports
    ├── Requests Analysis
    ├── Customer Statistics
    ├── Collector Performance
    └── Financial Reports
```

**⚠️ = Admin only**

---

## 🔑 Default Users

### Admin User (Created on Install):
```
Username: admin@cyclex.com
Password: admin (change immediately!)
Groups: CycleX Admin
Access: Full Odoo backend
```

### Test Users (Created via Sample Data):
```
Customers:
- Ahmed Hassan: +201001234567 (API only)
- Fatma Mohamed: +201002345678 (API only)
- Omar Ali: +201003456789 (API only)

Collectors:
- Mahmoud Saad: +201101234567 (API only)
- Khaled Ibrahim: +201102345678 (API only)
- Hassan Youssef: +201103456789 (API only)

All have Groups: CycleX User (API only)
```

---

## 🛡️ Row-Level Security Rules

### Record Rules:

#### 1. Customers - Own Data Only
```python
# res.partner (customers)
[('id', '=', user.partner_id.id)]
```

Customers can only see/edit their own record.

---

#### 2. Collectors - Own and Assigned Orders
```python
# cyclex.request (collector view)
[
    '|',
    ('status', '=', 'pending'),  # Can see all pending
    ('collector_id', '=', user.partner_id.id)  # Can see assigned to them
]
```

Collectors see:
- All pending orders (to accept)
- Their assigned orders

---

#### 3. Wallets - Own Wallet Only
```python
# cyclex.wallet
[('partner_id', '=', user.partner_id.id)]
```

Users can only access their own wallet.

---

#### 4. Commissions - Own Commissions Only
```python
# cyclex.commission
[('collector_id', '=', user.partner_id.id)]
```

Collectors can only see their own earnings.

---

## 🎯 Permission Scenarios

### Scenario 1: Customer Creates Request

**User:** Customer (Ahmed)  
**Action:** Create recycling request  
**Permission Check:**

```
1. Check user is logged in ✅
2. Check user is customer ✅
3. Check product exists ✅
4. Check quantity > 0 ✅
5. Create request ✅
6. Generate QR code (auto) ✅
7. Return success ✅
```

**Result:** ✅ Allowed

---

### Scenario 2: Collector Views Available Orders

**User:** Collector (Mahmoud in Nasr City)  
**Action:** View available orders  
**Permission Check:**

```
1. Check user is logged in ✅
2. Check user is collector ✅
3. Check collector is verified ✅
4. Filter orders by working areas (Nasr City, Heliopolis) ✅
5. Return pending orders in those areas ✅
```

**Result:** ✅ Allowed (filtered results)

---

### Scenario 3: Collector Tries to View Another's Commission

**User:** Collector A  
**Action:** View Collector B's commission  
**Permission Check:**

```
1. Check user is logged in ✅
2. Check user is collector ✅
3. Check commission belongs to user ❌ (belongs to Collector B)
4. Deny access ❌
```

**Result:** ❌ Forbidden

---

### Scenario 4: Manager Verifies Collector

**User:** Manager  
**Action:** Verify collector account  
**Permission Check:**

```
1. Check user is logged in ✅
2. Check user is manager ✅
3. Try to update collector_verified field ❌ (admin only)
4. Deny access ❌
```

**Result:** ❌ Forbidden (Needs Admin)

---

### Scenario 5: Admin Approves Withdrawal

**User:** Admin  
**Action:** Approve pending withdrawal  
**Permission Check:**

```
1. Check user is logged in ✅
2. Check user is admin ✅
3. Check withdrawal is pending ✅
4. Update withdrawal_status = approved ✅
5. Set approved_by = admin ✅
6. Set approval_date = now ✅
```

**Result:** ✅ Allowed

---

## 🔐 API Authentication

### Session-Based Authentication:

```
1. User calls /api/cyclex/login
2. Odoo creates session
3. Returns auth_token cookie
4. Mobile app stores cookie
5. All subsequent requests include cookie
6. Odoo validates session on each request
```

### Permission Checks in API:

```python
# In every API controller method:
def my_endpoint(self, **kwargs):
    # 1. Check user is authenticated
    if not request.env.uid:
        return error_response(401, "Unauthorized")
    
    # 2. Get current user
    current_user = request.env.user.partner_id
    
    # 3. Check user type
    if current_user.cyclex_user_type != 'customer':
        return error_response(403, "Forbidden")
    
    # 4. Check ownership
    request_obj = request.env['cyclex.request'].browse(request_id)
    if request_obj.customer_id.id != current_user.id:
        return error_response(403, "Access denied")
    
    # 5. Proceed with operation
    # ...
```

---

## 📊 Permission Examples

### What Can Each Role Do?

#### Customer (via Mobile API):
```
✅ Register account
✅ Verify phone number
✅ Login
✅ View categories and products
✅ Create recycling requests
✅ View own requests
✅ View own wallet and transactions
✅ Request withdrawals
✅ Rate completed orders
✅ Update own profile
❌ Access Odoo backend
❌ View other customers' data
❌ Modify prices or categories
❌ Approve withdrawals
```

---

#### Collector (via Mobile API):
```
✅ Register account
✅ Verify phone number
✅ Login (after admin verification)
✅ View available orders (in their areas only)
✅ Accept orders
✅ Reject orders
✅ Scan QR codes
✅ View own completed orders
✅ View own commissions
✅ Update own profile
❌ Access Odoo backend
❌ View all orders
❌ Modify commission rates
❌ Access other collectors' data
```

---

#### Manager (Odoo Backend):
```
✅ View all requests, customers, collectors
✅ Create/edit categories and products
✅ Create/edit working areas
✅ View all wallets and transactions
✅ View all commissions
✅ Generate reports
✅ Export data
❌ Verify collectors (admin only)
❌ Approve withdrawals (admin only)
❌ Modify commissions
❌ Access system parameters
❌ Manage user groups
```

---

#### Admin (Odoo Backend):
```
✅ Everything Manager can do
✅ Verify collector accounts
✅ Approve/reject withdrawal requests
✅ Modify commission rates
✅ Manual wallet credits (bonuses)
✅ Access system parameters
✅ Configure SMS Misr credentials
✅ Configure Firebase FCM
✅ Manage security groups
✅ Access technical menus
✅ View/modify scheduled actions
✅ Database operations
```

---

## 🛠️ How to Assign Roles

### For Mobile Users (Automatic):

**Registration API automatically assigns:**
```python
# When user registers via API:
new_user.write({
    'groups_id': [(4, ref('cyclex.group_cyclex_user').id)]
})
```

Users **cannot** be assigned to Manager or Admin via API (security).

---

### For Backend Users (Manual):

**Create Backend User:**

1. Go to **Settings → Users & Companies → Users**
2. Click **Create**
3. Fill in details:
   ```
   Name: John Manager
   Email: john@cyclex.com
   Password: (set secure password)
   ```
4. Go to **Access Rights** tab
5. Under **Applications → CycleX:**
   - Select **Manager** OR **Admin**

**Group Selection:**
- **Manager:** `CycleX Manager` checkbox
- **Admin:** `CycleX Admin` checkbox

---

## 📝 Access Control List (ACL)

### ir.model.access.csv

Complete permissions table:

| Model | Group | Read | Write | Create | Delete |
|-------|-------|------|-------|--------|--------|
| **cyclex.category** | User | ✅ | ❌ | ❌ | ❌ |
| **cyclex.category** | Manager | ✅ | ✅ | ✅ | ✅ |
| **cyclex.category** | Admin | ✅ | ✅ | ✅ | ✅ |
| **cyclex.product** | User | ✅ | ❌ | ❌ | ❌ |
| **cyclex.product** | Manager | ✅ | ✅ | ✅ | ✅ |
| **cyclex.product** | Admin | ✅ | ✅ | ✅ | ✅ |
| **cyclex.working.area** | User | ✅ | ❌ | ❌ | ❌ |
| **cyclex.working.area** | Manager | ✅ | ✅ | ✅ | ✅ |
| **cyclex.request** | User | ✅ | ✅ | ✅ | ❌ |
| **cyclex.request** | Manager | ✅ | ✅ | ✅ | ❌ |
| **cyclex.request** | Admin | ✅ | ✅ | ✅ | ✅ |
| **cyclex.wallet** | User | ✅ | ❌ | ❌ | ❌ |
| **cyclex.wallet** | Manager | ✅ | ❌ | ❌ | ❌ |
| **cyclex.wallet** | Admin | ✅ | ✅ | ✅ | ✅ |
| **cyclex.wallet.transaction** | User | ✅ | ❌ | ❌ | ❌ |
| **cyclex.wallet.transaction** | Manager | ✅ | ❌ | ❌ | ❌ |
| **cyclex.wallet.transaction** | Admin | ✅ | ✅ | ✅ | ✅ |
| **cyclex.commission** | User | ✅ | ❌ | ❌ | ❌ |
| **cyclex.commission** | Manager | ✅ | ❌ | ❌ | ❌ |
| **cyclex.commission** | Admin | ✅ | ✅ | ✅ | ✅ |

---

## 🔍 Checking User Permissions

### Via Odoo Shell:

```python
# Get user
user = env['res.user'].search([('login', '=', 'admin@cyclex.com')])

# Check groups
user.groups_id.mapped('name')
# ['CycleX Admin', 'Administration / Settings', ...]

# Check if user has specific group
cyclex_admin = env.ref('cyclex.group_cyclex_admin')
user.id in cyclex_admin.users.ids
# True

# Check if user can access model
env['cyclex.request'].check_access_rights('write')
# True (if has permission), raises exception otherwise
```

---

### Via Python (API):

```python
# In controller
from odoo.http import request

def my_endpoint(self):
    # Get current user
    current_user = request.env.user
    
    # Check if admin
    is_admin = current_user.has_group('cyclex.group_cyclex_admin')
    
    # Check if manager or admin
    is_manager = current_user.has_group('cyclex.group_cyclex_manager')
    
    # Check access to model
    try:
        request.env['cyclex.wallet'].check_access_rights('write')
        can_write_wallet = True
    except:
        can_write_wallet = False
```

---

## 🎯 Best Practices

### 1. Principle of Least Privilege
- Give users **minimum permissions** needed
- Start with User group, escalate only if needed
- Review permissions quarterly

### 2. Separate Mobile and Backend Access
- Mobile users: **Never** give Odoo backend access
- Backend users: Create separate accounts
- Don't mix API and backend users

### 3. Audit Trail
- Track all administrative actions
- Log approvals and rejections
- Monitor permission changes

### 4. Regular Review
- Review user list monthly
- Deactivate unused accounts
- Check for permission creep

---

## 🚨 Security Warnings

### ⚠️ DO NOT:
- ❌ Give mobile users backend access
- ❌ Share admin credentials
- ❌ Allow users to change their own groups
- ❌ Bypass permission checks in API
- ❌ Store passwords in plain text

### ✅ DO:
- ✅ Use strong passwords
- ✅ Enable 2FA for admins
- ✅ Regular permission audits
- ✅ Log all sensitive operations
- ✅ Use HTTPS in production

---

## 📋 Permission Checklist

### Before Deployment:

- [ ] Default admin password changed
- [ ] Manager accounts created (if needed)
- [ ] Test users have correct groups
- [ ] Mobile users cannot access backend
- [ ] Withdrawal approval limited to admins
- [ ] Collector verification limited to admins
- [ ] System parameters secured
- [ ] API authentication working
- [ ] Session timeout configured
- [ ] Rate limiting enabled (SMS, API)

---

## 🔧 Troubleshooting

### Problem: User Can't Access Menu

**Symptoms:** Menu items not visible

**Solution:**
1. Check user's security groups
2. Verify group has menu access
3. Clear browser cache
4. Check record rules don't hide all records

---

### Problem: API Returns 403 Forbidden

**Symptoms:** Valid login but access denied

**Solution:**
1. Check user has `group_cyclex_user`
2. Verify user is trying to access own data
3. Check record rules in model
4. Verify user type (customer vs collector)

---

### Problem: Admin Can't Approve Withdrawal

**Symptoms:** Button not visible or action fails

**Solution:**
1. Check user has `group_cyclex_admin` (not just manager)
2. Verify withdrawal status is `pending`
3. Check transaction is type `debit`
4. Refresh browser

---

## 📚 Related Documentation

- **Security Groups:** `custom_addons/cyclex/security/cyclex_security.xml`
- **Access Rights:** `custom_addons/cyclex/security/ir.model.access.csv`
- **API Authentication:** `API_DOCUMENTATION.md`
- **Backend Views:** `custom_addons/cyclex/views/*.xml`

---

## 🎓 Training Guide

### For Managers:

**Week 1:**
- Learn Odoo navigation
- Understand CycleX menu structure
- Practice creating categories/products
- Review reports and dashboards

**Week 2:**
- Handle customer requests
- Monitor order flow
- Generate reports
- Export data

---

### For Admins:

**Week 1:**
- Everything from Manager training
- Understand security model
- Learn system parameters
- Practice collector verification

**Week 2:**
- Withdrawal approval workflow
- System configuration (SMS, Firebase)
- Monitoring and logging
- Database maintenance

---

**Last Updated:** October 17, 2025  
**Maintained By:** CycleX Technical Team

