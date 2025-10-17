# CycleX Development Plan 🚀

> A recycling mobile application integrated with Odoo backend

---

## 📋 Project Overview

**Project Name:** CycleX  
**Concept:** A recycling mobile application where users sell recyclable items through the app, collectors pick them up and pay users, and the app owner earns commission on each transaction.

**Tech Stack:**
- Backend: Odoo 18
- iOS: Swift
- Android: Kotlin
- Notifications: Firebase FCM
- SMS: SMS Misr Gateway
- Languages: Arabic & English

---

## 🎯 Development Roadmap

### Phase 1: Backend Foundation (Odoo Module Setup)

#### Checkpoint 1.1: Module Initialization ✅
- [x] Create `cyclex` Odoo module structure
- [x] Add module manifest (`__manifest__.py`)
- [x] Design and add CycleX logo
- [x] Create main menu structure
- [x] Set up security groups (Customer, Collector, Admin)
- [x] Initialize `__init__.py` files

#### Checkpoint 1.2: Core Models - User Management ✅
- [x] Extend `res.users` model for CycleX users
- [x] Extend `res.partner` model with custom fields:
  - [x] Phone number (primary login field)
  - [x] FCM token
  - [x] Preferred language (ar/en)
  - [x] User type (customer/collector)
  - [x] Verification status
  - [x] GPS coordinates (latitude/longitude)
- [x] Add verification code field (6-digit)
- [x] Add verification expiry datetime

#### Checkpoint 1.3: Core Models - Categories & Products ✅
- [x] Create `cyclex.category` model:
  - [x] Name (translatable)
  - [x] Parent category (hierarchical)
  - [x] Icon/image field
  - [x] Active status
- [x] Create root category: "Recyclable Materials"
- [x] Create main categories (Plastic, Metal, Paper, Glass, Cardboard, Electronics)
- [x] Create subcategories (Plastic Bottles, Plastic Bags, Aluminum, Iron/Steel, Copper)
- [x] Create `cyclex.product` model:
  - [x] Name (translatable)
  - [x] Category (many2one)
  - [x] Price per kg
  - [x] Description
  - [x] Image
  - [x] Active status
- [x] Create 11 sample products with pricing (0.50 - 45.00 EGP/kg)

#### Checkpoint 1.4: Core Models - Requests/Orders ✅
- [x] Create `cyclex.request` model:
  - [x] Customer (many2one res.partner)
  - [x] Collector (many2one res.partner, optional)
  - [x] Category (many2one)
  - [x] Product (many2one)
  - [x] Quantity
  - [x] Weight (kg)
  - [x] Calculated price
  - [x] Photos (binary fields, max 2)
  - [x] GPS location (from customer profile)
  - [x] Pickup date
  - [x] Status (draft/pending/assigned/collected/cancelled)
  - [x] QR code (generated unique identifier via UUID)
  - [x] Rating (selection: 1-5 stars)
  - [x] Comments (text)
  - [x] Creation date
  - [x] Completion date
- [x] Add computed fields for price calculation (weight × price_per_kg)
- [x] Add QR code generation logic (UUID v4)
- [x] Add business logic methods (submit, assign, collect, cancel)
- [x] Add data validation (weight, quantity, pickup date)

#### Checkpoint 1.5: Core Models - Wallet System ✅
- [x] Create `cyclex.wallet` model:
  - [x] User (many2one res.partner)
  - [x] Balance (monetary, computed & stored)
  - [x] Total earned (monetary, computed & stored)
  - [x] Total withdrawn (monetary, computed & stored)
  - [x] Withdrawal threshold (default: 1000 EGP)
  - [x] Status (active/frozen)
- [x] Create `cyclex.wallet.transaction` model:
  - [x] Wallet (many2one)
  - [x] Customer (related from wallet)
  - [x] Request/Order (many2one)
  - [x] Amount (positive for credit, negative for debit)
  - [x] Type (credit/debit)
  - [x] Description
  - [x] Transaction date
- [x] Add wallet balance calculation methods
- [x] Add withdrawal request functionality
- [x] Add business methods (add_credit, add_debit, freeze, activate)
- [x] Add data validation (amount sign, balance check, withdrawal threshold)
- [x] Integrate with request model (automatic wallet credit on collection)

#### Checkpoint 1.6: Collector-Specific Models ✅
- [x] Extend `res.partner` for collector fields:
  - [x] ID number
  - [x] Vehicle type (selection: bicycle/motorcycle/car/van/truck)
  - [x] Working areas (many2many with cyclex.working.area)
  - [x] Approval status (pending/approved/rejected/suspended)
  - [x] Approval date, approved by, rejection reason
  - [x] Commission rate (%) - Default: 5%, Range: 0-100%
  - [x] Total orders completed (computed from requests)
  - [x] Average rating (computed from customer ratings)
- [x] Create `cyclex.working.area` model:
  - [x] Name (city/district, translatable)
  - [x] Governorate (translatable)
  - [x] Description (translatable)
  - [x] Active status
  - [x] GPS coordinates (center lat/long, radius)
  - [x] Collector count (computed)
- [x] Add validation: max 5 working areas per collector
- [x] Add 12 sample working areas (Cairo, Giza, Alexandria, Qalyubia, Dakahlia)
- [x] Add approval workflow methods (approve, reject, suspend)

#### Checkpoint 1.7: Commission System ✅
- [x] Create `cyclex.commission` model:
  - [x] Collector (many2one)
  - [x] Request (many2one)
  - [x] Customer (related from request)
  - [x] Order value
  - [x] Commission rate
  - [x] Commission amount (computed: value × rate / 100)
  - [x] Status (pending/paid)
  - [x] Payment date
  - [x] Create date (indexed)
  - [x] Notes field
- [x] Add commission calculation on order completion (automatic)
- [x] Create commission payout tracking (mark paid/pending)
- [x] Add business methods (create_commission_for_request, mark_paid, mark_pending)
- [x] Add data validation (order value > 0, rate 0-100%, unique per request)
- [x] Integrate with request model (automatic commission on collection)

---

### Phase 2: Views & UI (Odoo Backend) ✅

#### Checkpoint 2.1: User Management Views ✅
- [x] Create tree/list view for customers
- [x] Create form view for customer details
- [x] Create tree/list view for collectors
- [x] Create form view for collector registration approval
- [x] Add verification status indicators
- [x] Create search/filter views
- [x] Add kanban views for both customers and collectors
- [x] Add visual badges and ribbons

#### Checkpoint 2.2: Categories & Products Views ✅
- [x] Create tree/list view for categories (hierarchical)
- [x] Create form view for categories
- [x] Create tree/list view for products
- [x] Create form view for products
- [x] Add kanban view for products (with images)
- [x] Add kanban view for categories
- [x] Add search/filter views
- [x] Add graph view for product popularity

#### Checkpoint 2.3: Requests/Orders Views ✅
- [x] Create tree/list view for requests (all statuses)
- [x] Create form view for request details
- [x] Add status pipeline (kanban view with drag & drop)
- [x] Create calendar view for pickup dates
- [x] Add graph and pivot views for analytics
- [x] Create unassigned requests action
- [x] Add comprehensive search with date filters

#### Checkpoint 2.4: Wallet & Commission Views ✅
- [x] Create wallet balance dashboard
- [x] Create transaction history tree/list view
- [x] Create wallet kanban view
- [x] Create commission tracking tree/list view
- [x] Create commission payout form
- [x] Add commission kanban pipeline (pending/paid)
- [x] Add graph and pivot views for both wallets and commissions
- [x] Add comprehensive search and filters

#### Checkpoint 2.5: Reporting & Analytics ✅
- [x] Create dashboard for admin:
  - [x] Total requests by status (graph + pivot)
  - [x] Commission analysis (graph + pivot)
  - [x] Transaction trends (graph + pivot)
  - [x] Top collectors report
  - [x] Category/product popularity (pie chart)
- [x] Create collector performance reports
- [x] Create customer activity reports
- [x] Add dedicated Reporting menu section
- [x] Create 6 analytical reports with visualizations

---

### Phase 3: API Development (Controllers) ✅

#### Checkpoint 3.1: Authentication APIs ✅
- [x] `/api/cyclex/login` (POST)
  - [x] Accept phone number & password
  - [x] Return auth token + user profile
- [x] `/api/cyclex/register` (POST)
  - [x] Accept: name, phone, password, confirm_password
  - [x] Optional: fcm_token, language
  - [x] Generate 6-digit verification code
  - [x] Send SMS via SMS Misr (TODO: Integration)
  - [x] Return success + user_id
- [x] `/api/cyclex/verify` (POST)
  - [x] Accept: phone, verification_code
  - [x] Activate account on success
  - [x] Return auth token
- [x] `/api/cyclex/resend-code` (POST)
  - [x] Resend verification code via SMS
- [x] `/api/cyclex/profile` (GET)
  - [x] Get current user profile
- [x] `/api/cyclex/update-profile` (POST)
  - [x] Update user information

#### Checkpoint 3.2: Categories & Products APIs ✅
- [x] `/api/cyclex/categories` (GET)
  - [x] Return hierarchical category list
  - [x] Filter by parent category
  - [x] Support language parameter (ar/en)
- [x] `/api/cyclex/products` (GET)
  - [x] Return products by category
  - [x] Include pricing, images
  - [x] Support search/filter
- [x] `/api/cyclex/product/<id>` (GET)
  - [x] Get product details by ID

#### Checkpoint 3.3: Request/Order APIs ✅
- [x] `/api/cyclex/request/create` (POST)
  - [x] Accept: category_id, product_id, quantity, weight, photos (base64), pickup_date
  - [x] Auto-detect GPS from user profile
  - [x] Calculate price
  - [x] Generate QR code
  - [x] Return request details
- [x] `/api/cyclex/request/list` (GET)
  - [x] Return user's request history
  - [x] Filter by status
  - [x] Pagination support
- [x] `/api/cyclex/request/details/<id>` (GET)
  - [x] Return full request details including QR code
- [x] `/api/cyclex/request/cancel/<id>` (POST)
  - [x] Allow cancellation if status is pending

#### Checkpoint 3.4: Collector APIs ✅
- [x] `/api/cyclex/collector/register` (POST)
  - [x] Accept: name, phone, id_number, vehicle_type, working_areas
  - [x] Set status to "pending approval"
  - [x] Notify admin (TODO)
- [x] `/api/cyclex/collector/available-orders` (GET)
  - [x] Return orders in collector's working areas
  - [x] Filter by status (pending/available)
- [x] `/api/cyclex/collector/accept-order/<id>` (POST)
  - [x] Assign order to collector
  - [x] Set 3-day completion deadline
  - [x] Notify customer (TODO)
- [x] `/api/cyclex/collector/reject-order/<id>` (POST)
  - [x] Reject order assignment
- [x] `/api/cyclex/collector/scan-qr` (POST)
  - [x] Validate QR code
  - [x] Return order details
- [x] `/api/cyclex/collector/complete-order/<id>` (POST)
  - [x] Mark order as collected
  - [x] Update wallet balance
  - [x] Calculate commission
  - [x] Notify customer (TODO)

#### Checkpoint 3.5: Wallet APIs ✅
- [x] `/api/cyclex/wallet/balance` (GET)
  - [x] Return current balance, total earned, withdrawable amount
- [x] `/api/cyclex/wallet/transactions` (GET)
  - [x] Return transaction history
  - [x] Pagination support
- [x] `/api/cyclex/wallet/withdraw` (POST)
  - [x] Accept: amount
  - [x] Validate minimum threshold
  - [x] Create withdrawal request

#### Checkpoint 3.6: Rating & Feedback APIs ✅
- [x] `/api/cyclex/order/rate/<id>` (POST)
  - [x] Accept: rating (1-5), comments
  - [x] Update order record
  - [x] Update collector's average rating

---

### Phase 4: QR Code Generation (Odoo) ✅

#### Checkpoint 4.1: QR Code Implementation ✅
- [x] Install Python QR code library (`qrcode`, `pillow`)
- [x] Generate unique QR codes for each order (based on UUID)
- [x] Store QR as image (Binary field) in order record
- [x] Create QR validation logic in collector scan endpoint
- [x] Add QR display in backend order form view
- [x] Add QR code to order details API response
- [x] Add security measures (order ID validation)

---

### Phase 5: Business Logic & Rules (Odoo)

#### Checkpoint 5.1: Order Workflow Automation
- [ ] Auto-assign orders to collectors (based on location/working areas)
- [ ] Set 3-day deadline on order acceptance
- [ ] Auto-revert unfulfilled orders to "available" after 3 days
- [ ] Send automated notifications at each status change (placeholders ready)
- [ ] Prevent duplicate order acceptance
- [ ] Add scheduled actions for deadline monitoring

#### Checkpoint 5.2: Wallet Logic
- [ ] Auto-credit wallet on order completion
- [ ] Validate withdrawal threshold (1000 EGP)
- [ ] Create withdrawal approval workflow
- [ ] Track wallet transaction history
- [ ] Prevent negative balance
- [ ] Add withdrawal request notifications (placeholders ready)

#### Checkpoint 5.3: Commission Calculation
- [ ] Calculate commission on order completion
- [ ] Apply collector-specific commission rates
- [ ] Track unpaid commissions
- [ ] Create commission payout workflow
- [ ] Generate commission reports
- [ ] Add commission analytics dashboard

#### Checkpoint 5.4: Validation & Security
- [ ] Phone number format validation
- [ ] Password strength requirements
- [ ] Rate limiting for API calls
- [ ] Token expiry and refresh logic
- [ ] Image upload size limits (photos)
- [ ] Prevent duplicate phone number registration
- [ ] Collector working area limit (max 5)
- [ ] Add input sanitization for all APIs

---

### Phase 6: Testing & Documentation (Odoo)

#### Checkpoint 6.1: API Testing (Postman/Insomnia)
- [ ] Create Postman collection for all 22 endpoints
- [ ] Test authentication flow (login, register, verify, resend)
- [ ] Test customer workflow (register → create request → track order → rate)
- [ ] Test collector workflow (register → accept order → scan QR → complete)
- [ ] Test wallet operations (balance, transactions, withdraw)
- [ ] Test edge cases and error handling
- [ ] Document all API responses with examples

#### Checkpoint 6.2: Backend Testing
- [ ] Test model constraints and validations
- [ ] Test computed fields (balances, ratings, commission)
- [ ] Test workflow transitions (draft → pending → assigned → collected)
- [ ] Test commission calculations
- [ ] Test QR code generation and validation
- [ ] Test scheduled actions (cron jobs)
- [ ] Load testing with sample data

#### Checkpoint 6.3: Documentation
- [ ] Complete API documentation (already started: API_DOCUMENTATION.md)
- [ ] Database schema documentation with ERD
- [ ] User roles and permissions guide
- [ ] Admin dashboard usage guide
- [ ] Backend workflow documentation
- [ ] Mobile app integration guide
- [ ] Deployment guide

---

### Phase 7: External Integrations (Final Odoo Stage)

#### Checkpoint 7.1: SMS Misr Integration
- [ ] Set up SMS Misr API credentials in Odoo system parameters
- [ ] Create `cyclex.sms` service model:
  - [ ] Generate 6-digit random code
  - [ ] Format SMS message (Arabic/English templates)
  - [ ] Send via SMS Misr REST API
  - [ ] Log SMS status (sent/failed/delivered)
- [ ] Integrate with registration endpoint
- [ ] Integrate with resend-code endpoint
- [ ] Add error handling and retry logic
- [ ] Create SMS log model for tracking and debugging
- [ ] Add SMS balance monitoring

#### Checkpoint 7.2: Firebase FCM Integration
- [ ] Create Firebase project (Console setup)
- [ ] Add Android app to Firebase
- [ ] Add iOS app to Firebase
- [ ] Download configuration files (google-services.json, GoogleService-Info.plist)
- [ ] Install `firebase-admin` Python library
- [ ] Set up FCM server key in Odoo system parameters
- [ ] Create `cyclex.notification` service model:
  - [ ] Order status updates (pending → assigned → collected)
  - [ ] Collector assignment notifications
  - [ ] Order completion notifications
  - [ ] Withdrawal approval/rejection notifications
  - [ ] Custom admin broadcast notifications
- [ ] Support multilingual notifications (ar/en based on user preference)
- [ ] Add notification history tracking
- [ ] Test with real devices (Android & iOS)

---

### Phase 8: Mobile App Development (Outside Odoo - Special Phase)

> **Note:** This phase is handled by mobile development teams and runs in parallel with Odoo backend work.

#### Checkpoint 8.1: iOS App (Swift)
- [ ] Share complete API documentation with iOS team
- [ ] Provide Firebase configuration files
- [ ] Set up project structure (MVVM/Clean Architecture)
- [ ] Implement authentication flow (login, register, verify)
- [ ] Implement customer features:
  - [ ] Browse categories and products
  - [ ] Create recycling requests
  - [ ] Upload photos (camera/gallery)
  - [ ] Track order status
  - [ ] View wallet balance and transactions
  - [ ] Rate completed orders
- [ ] Implement collector features:
  - [ ] Register as collector
  - [ ] View available orders
  - [ ] Accept/reject orders
  - [ ] Scan QR codes
  - [ ] Complete orders
  - [ ] View commission earnings
- [ ] Implement QR code scanner (AVFoundation)
- [ ] Implement push notifications (Firebase Cloud Messaging)
- [ ] Implement GPS location capture
- [ ] Implement multilingual support (Arabic/English)
- [ ] Test API integration

#### Checkpoint 8.2: Android App (Kotlin)
- [ ] Share complete API documentation with Android team
- [ ] Provide Firebase configuration files
- [ ] Set up project structure (MVVM/Clean Architecture)
- [ ] Implement authentication flow (login, register, verify)
- [ ] Implement customer features:
  - [ ] Browse categories and products
  - [ ] Create recycling requests
  - [ ] Upload photos (camera/gallery)
  - [ ] Track order status
  - [ ] View wallet balance and transactions
  - [ ] Rate completed orders
- [ ] Implement collector features:
  - [ ] Register as collector
  - [ ] View available orders
  - [ ] Accept/reject orders
  - [ ] Scan QR codes
  - [ ] Complete orders
  - [ ] View commission earnings
- [ ] Implement QR code scanner (CameraX + ML Kit)
- [ ] Implement push notifications (Firebase Cloud Messaging)
- [ ] Implement GPS location capture
- [ ] Implement multilingual support (Arabic/English)
- [ ] Test API integration

#### Checkpoint 8.3: Mobile Testing & QA
- [ ] Test notifications on both platforms (iOS & Android)
- [ ] Test photo upload functionality (compression, formats)
- [ ] Test GPS location capture accuracy
- [ ] Test QR code generation and scanning
- [ ] Test real-time order status updates
- [ ] Test multilingual support (UI + API responses)
- [ ] Test offline functionality (if applicable)
- [ ] Test different screen sizes and orientations
- [ ] Performance testing (battery, memory, network)
- [ ] Security testing (token storage, secure communication)

---

### Phase 9: Deployment & Launch

#### Checkpoint 9.1: Staging Environment
- [ ] Set up staging Odoo instance (dedicated server/cloud)
- [ ] Deploy CycleX module to staging
- [ ] Configure SMS Misr in test mode
- [ ] Configure Firebase dev project
- [ ] Load sample data (categories, products, test users, working areas)
- [ ] Deploy staging mobile apps (TestFlight for iOS, Firebase App Distribution for Android)
- [ ] Conduct UAT (User Acceptance Testing) with internal team
- [ ] Fix identified bugs and issues

#### Checkpoint 9.2: Production Setup
- [ ] Set up production Odoo instance (scalable infrastructure)
- [ ] Configure production database with replication
- [ ] Set up SMS Misr production credentials
- [ ] Set up Firebase production project
- [ ] Configure SSL certificates (HTTPS)
- [ ] Configure automated backups (daily database + filestore)
- [ ] Set up monitoring and logging (server, database, API)
- [ ] Set up error tracking (Sentry or similar)
- [ ] Configure CDN for static assets (optional)

#### Checkpoint 9.3: Go Live
- [ ] Deploy to production
- [ ] Submit iOS app to App Store
- [ ] Submit Android app to Google Play Store
- [ ] Onboard initial collectors (pilot program)
- [ ] Launch marketing campaign (social media, ads)
- [ ] Monitor system performance (server load, API response times)
- [ ] Provide user support (help desk, in-app chat)
- [ ] Collect user feedback for improvements
- [ ] Plan v2 features based on feedback

---

## 🔧 Technical Requirements

### Odoo Configuration
- Odoo version: 18
- Python version: 3.10+
- Required Odoo modules: `base`, `web`, `mail`
- External Python libraries:
  - `qrcode`
  - `requests` (for SMS API)
  - `firebase-admin` (for FCM)

### External Services (Phase 7 - Final Odoo Stage)
- **SMS Misr:** API credentials required for OTP verification
- **Firebase FCM:** Project setup for Android & iOS push notifications
- **GPS/Maps:** Built-in device GPS (no API key required for basic location capture)

### Security Considerations
- [ ] HTTPS for all API endpoints
- [ ] JWT token-based authentication
- [ ] Phone number encryption
- [ ] Rate limiting on SMS sending
- [ ] Input validation and sanitization
- [ ] Role-based access control (RBAC)

---

## 📊 Success Metrics

- [ ] Customer registration rate
- [ ] Order completion rate
- [ ] Collector approval time
- [ ] Average order processing time
- [ ] Customer satisfaction (ratings)
- [ ] Revenue and commission tracking
- [ ] App retention rate

---

## 🚨 Known Risks & Mitigation

| Risk | Impact | Mitigation |
|------|--------|------------|
| SMS gateway downtime | High | Implement fallback OTP via email |
| Collector no-shows | Medium | 3-day deadline + auto-reassignment |
| Fraudulent requests | High | QR validation + photo verification |
| Wallet withdrawal abuse | Medium | Threshold limits + admin approval |
| GPS inaccuracy | Low | Manual address entry option |

---

## 📞 Contact & Support

- **Backend Developer:** (Odoo team)
- **Mobile Team:** (iOS/Android developers)
- **Project Manager:** (Coordination)
- **Admin Dashboard:** Access via Odoo web interface

---

**Last Updated:** October 17, 2025  
**Version:** 2.1  
**Status:** Phase 4 Completed ✅ | Phase 5 (Business Logic) Next

---

## 📝 Phase Organization Notes

### Odoo Backend Phases (Sequential)
1. **Phase 1-3:** ✅ **COMPLETED** - Backend Foundation, Views/UI, API Development
2. **Phase 4:** QR Code Generation (Next up)
3. **Phase 5:** Business Logic & Rules
4. **Phase 6:** Testing & Documentation
5. **Phase 7:** External Integrations (SMS Misr + Firebase) - *Final Odoo stage*

### Non-Odoo Phases (Can run in parallel)
6. **Phase 8:** Mobile App Development (iOS & Android) - *Special Phase - Outside Odoo*
7. **Phase 9:** Deployment & Launch

### Key Points
- ✅ **Phase 1-4 are complete:** Full backend + APIs + QR Code generation
- 🎯 **Current focus:** Phase 5 (Business Logic & Rules)
- 📱 **Mobile development (Phase 8)** can start now! All APIs ready + QR codes working
- 🔌 **Integrations (Phase 7)** are deliberately at the end of Odoo work
- 🚀 **MVP readiness:** Complete Phase 1-6 for full backend functionality
- 🎉 **Production ready:** Complete Phase 1-7 for integrated system

**Let's continue building! 💪**

