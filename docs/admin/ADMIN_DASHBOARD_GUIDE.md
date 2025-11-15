# CycleX Admin Dashboard Usage Guide 📊

**Complete guide for using the Odoo backend dashboard and administrative features**

**Version:** 1.0  
**For:** CycleX Administrators and Managers

---

## 🚀 Getting Started

### Access the Dashboard:

1. **Open Browser:** Navigate to `http://localhost:10018` (or your server URL)
2. **Login:**
   ```
   Database: cyclex_db
   Email: admin@cyclex.com
   Password: admin (change on first login!)
   ```
3. **Navigate:** Click **CycleX** in the main menu

---

## 📊 Dashboard Overview

### Main Dashboard (CycleX → Dashboard)

**KPIs Displayed:**

```
┌─────────────────────────────────────────────────────────┐
│              CycleX Dashboard - Overview                 │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  📦 Total Requests        💰 Total Revenue              │
│      156                      15,450 EGP                │
│                                                          │
│  👥 Active Customers      🚚 Active Collectors          │
│      89                       12                        │
│                                                          │
│  ⏳ Pending Orders        ✅ Completed Today            │
│      23                       8                         │
│                                                          │
│  💸 Pending Withdrawals   🎯 Completion Rate            │
│      5 (2,300 EGP)           87%                        │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

**Quick Actions:**
- 🆕 New Request
- 👤 New Customer
- 📋 View Pending Orders
- 💰 Pending Withdrawals

---

## 📋 Main Menu Structure

### CycleX Menu:

```
CycleX
├── 📊 Dashboard
├── 📦 Recycling Requests
│   ├── All Requests
│   ├── Pending Orders
│   ├── Assigned Orders
│   ├── Completed Orders
│   └── Cancelled Orders
├── 👥 Customers
├── 🚚 Collectors
│   ├── All Collectors
│   ├── Pending Verification ⚠️
│   └── Verified Collectors
├── 💰 Financial
│   ├── Wallets
│   ├── Transactions
│   ├── Pending Withdrawals ⚠️
│   └── Commissions
├── ⚙️ Configuration
│   ├── Categories
│   ├── Products
│   ├── Working Areas
│   └── System Parameters ⚠️ (Admin only)
└── 📈 Reports
    ├── Requests Analysis
    ├── Customer Statistics
    ├── Collector Performance
    └── Financial Reports
```

**⚠️ = Admin only**

---

## 1️⃣ Managing Recycling Requests

### View All Requests

**Path:** CycleX → Recycling Requests → All Requests

**List View Shows:**
- Request Number (REQ-00001)
- Customer Name
- Product
- Quantity & Unit
- Calculated Price
- Status (badge color-coded)
- Pickup Date
- Collector (if assigned)
- QR Code

**Filters:**
- Status: Pending, Assigned, Collected, Cancelled
- Pickup Date: Today, This Week, This Month
- Customer: Select customer
- Collector: Select collector
- Working Area: Filter by area

---

### View Request Details

**Click on any request** to open form view:

**Information Sections:**

1. **Request Information:**
   - Request Number
   - Customer (link to customer profile)
   - Product & Category
   - Quantity, Unit
   - Calculated Price, Currency

2. **Pickup Details:**
   - Pickup Date
   - Pickup Time (Morning/Afternoon/Evening)
   - Address
   - Location (GPS coordinates)
   - Map view (if integrated)

3. **Collector Assignment:**
   - Assigned Collector (if any)
   - Assignment Date
   - Collection Date (when completed)

4. **QR Code & Rating:**
   - QR Code (text)
   - QR Code Image (scannable)
   - Customer Rating (1-5 stars)
   - Comments/Feedback

5. **Additional Info:**
   - Photo (if uploaded)
   - Notes
   - Status
   - Created Date

**Smart Buttons (Top):**
- 💰 **Wallet** - View customer's wallet
- 💸 **Commission** - View collector's commission (if completed)

---

### Common Actions

#### 1. Create Manual Request (Admin/Manager)

**Path:** CycleX → Recycling Requests → Create

**Steps:**
1. Click **Create**
2. Fill in:
   ```
   Customer: Select customer
   Product: Select product
   Quantity: 15.5
   Unit: kg
   Pickup Date: 2025-10-25
   Pickup Time: Morning
   Address: Full address
   GPS Location: 30.0444, 31.2357
   ```
3. Click **Save**
4. QR code auto-generated ✅
5. Status set to `pending` ✅

---

#### 2. Assign Order to Collector (Manual Assignment)

**Steps:**
1. Open pending request
2. Click **Edit**
3. Set **Collector** field
4. Set **Status** = Assigned
5. Click **Save**

**Note:** Normally done via mobile app, manual for emergencies

---

#### 3. Cancel Request

**Steps:**
1. Open request
2. Click **Edit**
3. Set **Status** = Cancelled
4. Add note explaining cancellation
5. Click **Save**

**Effects:**
- Order removed from collector's list
- Customer notified (if Phase 7 complete)
- Can't be reassigned

---

### Bulk Actions

**Select multiple requests** (checkboxes):
- 📤 **Export** - Export to Excel/CSV
- 🗑️ **Archive** - Soft delete (keep in database)
- 📧 **Send Email** - Bulk email (if configured)

---

## 2️⃣ Managing Customers

### View Customers

**Path:** CycleX → Customers

**List View Shows:**
- Name
- Phone
- Email
- Language (🇦🇪 ar / 🇬🇧 en)
- Phone Verified (✅/❌)
- Wallet Balance
- Total Requests
- Registration Date

**Filters:**
- Verified / Unverified
- Has Wallet Balance
- Active / Archived

---

### Customer Profile

**Open customer** to view:

**Sections:**

1. **Contact Information:**
   - Name, Phone, Email
   - Address, City
   - Language preference

2. **CycleX Information:**
   - User Type: Customer
   - Phone Verified: ✅/❌
   - Verification Code (for troubleshooting)
   - FCM Token (for notifications)
   - Registration Date

3. **Activity:**
   - Total Requests
   - Completed Orders
   - Average Rating Given
   - Last Request Date

**Smart Buttons:**
- 📦 **Requests** (23) - View all requests
- 💰 **Wallet** - View wallet details
- 📊 **Statistics** - View charts

---

### Common Admin Tasks

#### 1. Verify Customer Phone (Manual Override)

**When:** Customer reports verification issues

**Steps:**
1. Open customer record
2. Check `Phone Verified` checkbox
3. Save

**Note:** Normally done via SMS verification in app

---

#### 2. View Customer Requests

**Steps:**
1. Open customer
2. Click **Requests** smart button
3. See filtered list of customer's requests

---

#### 3. Check Customer Wallet

**Steps:**
1. Open customer
2. Click **Wallet** smart button
3. View:
   - Current balance
   - Total credits/debits
   - Transaction history

---

## 3️⃣ Managing Collectors

### View Collectors

**Path:** CycleX → Collectors → All Collectors

**List View Shows:**
- Name
- Phone
- Email
- Verified Status (✅/❌)
- Commission Rate (%)
- Working Areas (badges)
- Completed Orders
- Total Earned

**Filters:**
- ⚠️ **Pending Verification** - Needs admin approval
- ✅ **Verified** - Active collectors
- 📍 **By Working Area**

---

### Collector Verification (ADMIN ONLY) ⚠️

**Path:** CycleX → Collectors → Pending Verification

**Critical Admin Task!**

**Steps to Verify Collector:**

1. Go to **Pending Verification** menu
2. Review collector application:
   ```
   Name: Mahmoud Saad
   Phone: +201101234567
   Email: mahmoud.saad@example.com
   Registration Date: 2025-10-15
   Working Areas Requested: Nasr City, Heliopolis
   ```

3. **Verify Information:**
   - Check ID documents (if uploaded)
   - Verify phone number is real
   - Check working areas are realistic

4. **Approve Collector:**
   - Open collector record
   - Check `Collector Verified` checkbox
   - Set `Commission Rate` (default: 15%)
   - Assign `Working Areas` (select 1-5 areas)
   - Click **Save**

5. **Notification Sent:**
   - Collector receives approval notification
   - Can now login and accept orders

---

### Reject Collector Application

**Steps:**
1. Open collector record
2. Add internal note explaining rejection
3. Click **Archive** (or delete if appropriate)
4. Collector notified (if Phase 7 complete)

---

### Modify Collector Settings

**Admin Can Modify:**
- ✅ Commission Rate (%, default 15%)
- ✅ Working Areas (1-5 areas)
- ✅ Verification Status
- ✅ Active/Inactive status

**Example: Increase Commission Rate:**
1. Open collector
2. Edit **Commission Rate** from 15% to 20%
3. Save
4. Future orders will use 20% rate
5. Past commissions unchanged

---

## 4️⃣ Financial Management

### Wallet Overview

**Path:** CycleX → Financial → Wallets

**List View:**
- Customer Name
- Current Balance
- Total Credits
- Total Debits
- Transaction Count
- Last Transaction Date

**Search:**
- By customer name/phone
- Balance > X amount
- Has pending withdrawals

---

### Pending Withdrawals (ADMIN ONLY) ⚠️

**Path:** CycleX → Financial → Pending Withdrawals

**Critical Admin Task!**

**Workflow:**

```
Customer Requests Withdrawal (via app)
          ↓
     Status: Pending
          ↓
   Admin Reviews Request
          ↓
      ┌─────────┐
      ▼         ▼
   Approve   Reject
      ↓         ↓
   Status:   Status:
   Approved  Rejected
      ↓         ↓
   Process   Balance
   Payment   Restored
```

---

### Approve Withdrawal

**Steps:**

1. Go to **Pending Withdrawals**
2. See list:
   ```
   Customer: Ahmed Hassan
   Amount: 500.00 EGP
   Request Date: 2025-10-17 14:30
   Current Balance: 1,250.00 EGP
   ```

3. **Review Request:**
   - Check customer balance is sufficient
   - Verify amount is reasonable
   - Check for fraud patterns

4. **Approve:**
   - Open transaction
   - Click **Approve** button (green)
   - Status changes to `approved`
   - Admin name recorded
   - Approval date recorded

5. **Process Payment:**
   - Transfer money to customer (outside Odoo)
   - Mark as paid (optional manual step)

---

### Reject Withdrawal

**Steps:**

1. Open pending withdrawal
2. Click **Reject** button (red)
3. Dialog appears: **Enter Rejection Reason**
   ```
   Reason: Insufficient documentation
   OR
   Reason: Suspicious activity detected
   ```
4. Click **Confirm**
5. **Effects:**
   - Status = `rejected`
   - Balance restored to customer wallet
   - Customer notified (if Phase 7 complete)
   - Rejection reason saved

---

### Manual Wallet Credit (ADMIN ONLY)

**When:** Bonuses, corrections, promotional credits

**Steps:**

1. Go to **CycleX → Financial → Wallets**
2. Find customer wallet
3. Open wallet
4. Click **Add Credit** button
5. Fill in:
   ```
   Amount: 100.00
   Description: Welcome bonus for new customer
   ```
6. Click **Confirm**

**Effects:**
- Wallet balance increased
- Transaction created
- Customer notified

---

## 5️⃣ Configuration Management

### Categories

**Path:** CycleX → Configuration → Categories

**Actions:**

#### Create Category:
1. Click **Create**
2. Fill in:
   ```
   Name: Plastic
   Arabic Name: بلاستيك
   Description: All plastic materials
   Sequence: 10 (display order)
   Image: Upload category icon
   Active: ✅
   ```
3. Save

#### Edit Category:
- Update names, descriptions
- Change image
- Reorder (sequence number)
- Activate/deactivate

---

### Products

**Path:** CycleX → Configuration → Products

**Actions:**

#### Create Product:
1. Click **Create**
2. Fill in:
   ```
   Name: Plastic Bottles
   Arabic Name: زجاجات بلاستيك
   Category: Plastic
   Price per KG: 3.50 EGP
   Unit of Measure: kg
   Description: PET plastic bottles
   Image: Upload product icon
   ```
3. Save

#### Bulk Price Update:
1. Select multiple products (checkboxes)
2. Click **Action** → **Update Prices**
3. Enter new price
4. Apply to all selected

---

### Working Areas

**Path:** CycleX → Configuration → Working Areas

**Purpose:** Define geographic service areas for collectors

#### Create Working Area:
1. Click **Create**
2. Fill in:
   ```
   Name: Nasr City
   Arabic Name: مدينة نصر
   Active: ✅
   ```
3. Save

#### Assign to Collectors:
- Areas are assigned from collector profile
- Collector → Edit → Working Areas (select 1-5)

---

### System Parameters (ADMIN ONLY) ⚠️

**Path:** Settings → Technical → Parameters → System Parameters

**CycleX Parameters:**

| Parameter Key | Value | Purpose |
|--------------|-------|---------|
| `sms.misr.username` | your_username | SMS Misr API username |
| `sms.misr.password` | your_password | SMS Misr API password |
| `sms.misr.sender` | CycleX | SMS sender name |
| `firebase.server_key` | AAAA...xxx | Firebase FCM server key |
| `cyclex.min_withdrawal` | 10.00 | Minimum withdrawal amount |
| `cyclex.commission_rate_default` | 15.00 | Default commission % |

**How to Add/Edit:**
1. Go to System Parameters
2. Click **Create** (or edit existing)
3. Set Key and Value
4. Save

**⚠️ Security:** Never share these parameters!

---

## 6️⃣ Reports & Analytics

### Requests Analysis

**Path:** CycleX → Reports → Requests Analysis

**Metrics:**
- Total requests by status
- Requests by category
- Requests by working area
- Daily/weekly/monthly trends
- Average order value
- Completion rate

**Filters:**
- Date range
- Status
- Category
- Collector

**Export:** Excel, PDF, CSV

---

### Customer Statistics

**Path:** CycleX → Reports → Customer Statistics

**Metrics:**
- Total customers
- Active vs inactive
- Customers by area
- Top customers (by order count)
- Customer lifetime value
- Registration trends

**Charts:**
- Customer growth over time
- Orders per customer (histogram)
- Geographic distribution

---

### Collector Performance

**Path:** CycleX → Reports → Collector Performance

**Metrics:**
- Total collectors
- Orders completed per collector
- Average completion time
- Commissions earned
- Top performers
- Working area coverage

**KPIs per Collector:**
```
Mahmoud Saad
├── Completed Orders: 45
├── Total Earned: 1,250 EGP
├── Avg Completion Time: 1.5 days
├── Rating: 4.8/5 ⭐
└── Working Areas: Nasr City, Heliopolis
```

---

### Financial Reports

**Path:** CycleX → Reports → Financial Reports

**Metrics:**
- Total revenue (customer payments)
- Total commissions paid
- Profit margin
- Pending withdrawals (amount)
- Wallet balances summary
- Transaction volume

**Export:** Accounting software integration (future)

---

## 7️⃣ Daily Admin Tasks

### Morning Routine (15 minutes)

**1. Check Dashboard:**
```
□ Review pending withdrawals
□ Check pending collector verifications
□ Review yesterday's completed orders
□ Check for any issues/errors
```

**2. Approve Pending Withdrawals:**
```
□ Go to Pending Withdrawals
□ Review each request
□ Approve legitimate withdrawals
□ Reject suspicious ones
□ Process payments externally
```

**3. Verify New Collectors:**
```
□ Go to Pending Verification
□ Review collector applications
□ Check ID documents
□ Verify phone numbers
□ Approve qualified collectors
□ Assign working areas
```

**4. Monitor Active Orders:**
```
□ Check assigned orders
□ Look for overdue orders (3+ days)
□ Contact collectors if needed
□ Check cron job ran (auto-revert)
```

---

### Weekly Routine (30 minutes)

**Monday:**
```
□ Review last week's metrics
□ Generate weekly reports
□ Check collector performance
□ Identify top customers
□ Plan marketing campaigns
```

**Wednesday:**
```
□ Review pending orders
□ Check stock of working areas
□ Balance collector assignments
□ Review customer feedback
□ Address low ratings
```

**Friday:**
```
□ Weekly financial reconciliation
□ Export reports for management
□ Plan next week's goals
□ Review system performance
```

---

## 8️⃣ Troubleshooting Common Issues

### Issue 1: Customer Can't Create Request

**Check:**
1. Go to customer profile
2. Verify `Phone Verified` = ✅
3. Check customer has active status
4. Verify wallet exists
5. Check API logs for errors

**Fix:**
- Manually verify phone if needed
- Check product/category is active
- Review API error codes

---

### Issue 2: Collector Not Seeing Orders

**Check:**
1. Go to collector profile
2. Verify `Collector Verified` = ✅
3. Check `Working Areas` are assigned
4. Verify areas match order locations

**Fix:**
- Verify collector if pending
- Assign correct working areas
- Check orders are status `pending`

---

### Issue 3: Withdrawal Stuck in Pending

**Check:**
1. Go to Pending Withdrawals
2. Find transaction
3. Check amount ≤ wallet balance
4. Verify transaction type = debit

**Fix:**
- Review and approve/reject
- If stuck, check logs
- May need technical intervention

---

### Issue 4: QR Code Not Working

**Check:**
1. Go to request
2. Verify QR code field is filled
3. Check QR code format
4. Verify status is `assigned` (not collected)

**Fix:**
- If QR code missing, contact technical team
- Check collector is scanning correct code
- Verify request not already completed

---

## 9️⃣ Advanced Features

### Chatter (Activity Timeline)

Every record has a **Chatter** (bottom of form):

**Features:**
- 📝 **Log Notes** - Internal notes
- 📧 **Send Message** - Email to customer/collector
- 📅 **Schedule Activity** - Set reminders
- 📎 **Attach Files** - Upload documents

**Use Cases:**
- Log customer phone conversations
- Schedule follow-up calls
- Attach ID documents for collectors
- Track issue resolution

---

### Scheduled Actions (Cron Jobs)

**Path:** Settings → Technical → Automation → Scheduled Actions

**CycleX Cron Jobs:**

#### 1. Auto-Revert Overdue Orders
```
Name: CycleX: Auto-Revert Overdue Orders
Frequency: Every 6 hours
Last Run: [timestamp]
Next Run: [timestamp]
Status: Active ✅
```

**Manual Trigger:**
- Open cron job
- Click **Run Manually**
- Check logs for results

---

#### 2. Process Pending Withdrawals
```
Name: CycleX: Process Pending Withdrawals
Frequency: Daily (midnight)
Last Run: [timestamp]
Next Run: [timestamp]
Status: Active ✅
```

**What It Does:**
- Counts pending withdrawals
- Logs to admin
- Sends notification (if configured)

---

### Database Maintenance

**Path:** Settings → Technical → Database Structure

**Actions:**
- View model definitions
- Check indexes
- Analyze performance
- Export schema

**For Developers:** See `DATABASE_SCHEMA.md`

---

## 🔔 Notifications (Phase 7 - Future)

### When Firebase FCM is Implemented:

**Admin Can:**
- Send custom notifications to customers/collectors
- Broadcast announcements
- Notify about order updates
- Alert about system maintenance

**Future Menu:**
```
CycleX → Notifications
├── Send Notification
├── Broadcast Message
├── Notification History
└── FCM Settings
```

---

## 📱 Mobile App Support

### Helping Mobile Users:

#### Customer Reports Issue with App:

**Check in Odoo:**
1. Find customer by phone
2. Check `Phone Verified` status
3. Check `FCM Token` (if Phase 7)
4. Review request history
5. Check wallet transactions

**Common Fixes:**
- Reset verification status
- Manually approve pending request
- Credit wallet if needed
- Contact technical team for app issues

---

#### Collector Can't Accept Orders:

**Check in Odoo:**
1. Find collector by phone
2. Verify `Collector Verified` = ✅
3. Check `Working Areas` assigned
4. Check pending order count (max 5)
5. Review recent activity

**Common Fixes:**
- Verify collector account
- Assign working areas
- Check if at max capacity (5 orders)

---

## ⚙️ Settings & Configuration

### General Settings:

**Path:** Settings → General Settings

**CycleX Section:**
- Default commission rate: 15%
- Minimum withdrawal: 10 EGP
- Max pending orders per collector: 5
- Order auto-revert days: 3
- Image max size: 5 MB

---

### Language Settings:

**Path:** Settings → Translations → Languages

**Activate Languages:**
1. Activate **Arabic** (العربية)
2. Activate **English** (if not already)
3. Translate custom terms if needed

**User Language:**
- Set in user profile
- API respects user's language preference

---

## 📊 Dashboard Customization

### Customize Your View:

**Path:** CycleX → Dashboard

**Features:**
- 📌 **Pin to Dashboard** - Add favorite reports
- 🎨 **Change Layout** - Drag & drop widgets
- 📈 **Add Charts** - Custom visualizations
- 🔍 **Save Filters** - Quick access to common views

**Example Custom Dashboard:**
```
My CycleX Dashboard
├── Today's Completed Orders (list)
├── Pending Withdrawals (kanban)
├── Revenue Chart (line chart)
└── Top Customers (table)
```

---

## 🎓 Training Checklist

### For New Admins:

**Week 1:**
- [ ] Odoo basics (navigation, forms, lists)
- [ ] CycleX menu structure
- [ ] View requests, customers, collectors
- [ ] Understand status workflow
- [ ] Practice with sample data

**Week 2:**
- [ ] Verify collectors
- [ ] Approve withdrawals
- [ ] Create categories/products
- [ ] Generate reports
- [ ] Handle customer issues

**Week 3:**
- [ ] System parameters
- [ ] Cron jobs management
- [ ] Advanced filtering
- [ ] Data export
- [ ] Backup procedures

---

## 📞 Support Contacts

### Technical Issues:
- Odoo errors → Contact Technical Team
- API issues → Check API_DOCUMENTATION.md
- Mobile app issues → Contact Mobile Team

### Business Questions:
- Pricing → Update products
- Areas → Update working areas
- Policies → Update in documentation

---

## ✅ Quick Reference Card

### Most Common Tasks:

| Task | Path | Frequency |
|------|------|-----------|
| Approve Withdrawal | Financial → Pending Withdrawals | Daily |
| Verify Collector | Collectors → Pending Verification | As needed |
| View Dashboard | CycleX → Dashboard | Daily |
| Check Requests | Recycling Requests → All Requests | Daily |
| Generate Report | Reports → Select report type | Weekly |
| Add Product | Configuration → Products → Create | As needed |

---

**Happy administering! 🎉**

For detailed technical information, see:
- `DATABASE_SCHEMA.md` - Database structure
- `USER_ROLES_PERMISSIONS.md` - Security model
- `API_DOCUMENTATION.md` - API reference

