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

#### Checkpoint 1.3: Core Models - Categories & Products ✓
- [ ] Create `cyclex.category` model:
  - [ ] Name (translatable)
  - [ ] Parent category (hierarchical)
  - [ ] Icon/image field
  - [ ] Active status
- [ ] Create root category: "CycleX"
- [ ] Create subcategories (Plastic, Metal, Paper, Glass, etc.)
- [ ] Create `cyclex.product` model:
  - [ ] Name (translatable)
  - [ ] Category (many2one)
  - [ ] Price per kg
  - [ ] Description
  - [ ] Image
  - [ ] Active status

#### Checkpoint 1.4: Core Models - Requests/Orders ✓
- [ ] Create `cyclex.request` model:
  - [ ] Customer (many2one res.partner)
  - [ ] Collector (many2one res.partner, optional)
  - [ ] Category (many2one)
  - [ ] Product (many2one)
  - [ ] Quantity
  - [ ] Weight (kg)
  - [ ] Calculated price
  - [ ] Photos (binary fields, max 2)
  - [ ] GPS location (from customer profile)
  - [ ] Pickup date
  - [ ] Status (draft/pending/assigned/collected/cancelled)
  - [ ] QR code (generated unique identifier)
  - [ ] Rating (selection: 1-5 stars)
  - [ ] Comments (text)
  - [ ] Creation date
  - [ ] Completion date
- [ ] Add computed fields for price calculation
- [ ] Add QR code generation logic

#### Checkpoint 1.5: Core Models - Wallet System ✓
- [ ] Create `cyclex.wallet` model:
  - [ ] User (many2one res.partner)
  - [ ] Balance (float)
  - [ ] Total earned (float)
  - [ ] Total withdrawn (float)
  - [ ] Withdrawal threshold (default: 1000 EGP)
  - [ ] Status (active/frozen)
- [ ] Create `cyclex.wallet.transaction` model:
  - [ ] Wallet (many2one)
  - [ ] Request/Order (many2one)
  - [ ] Amount
  - [ ] Type (credit/debit)
  - [ ] Description
  - [ ] Transaction date
- [ ] Add wallet balance calculation methods
- [ ] Add withdrawal request functionality

#### Checkpoint 1.6: Collector-Specific Models ✓
- [ ] Extend `res.partner` for collector fields:
  - [ ] ID number
  - [ ] Vehicle type (selection)
  - [ ] Working areas (many2many with location/city model)
  - [ ] Approval status (pending/approved/rejected)
  - [ ] Commission rate (%)
  - [ ] Total orders completed
  - [ ] Average rating
- [ ] Create `cyclex.working.area` model:
  - [ ] Name (city/district)
  - [ ] Governorate
  - [ ] Active status
- [ ] Add validation: max 5 working areas per collector

#### Checkpoint 1.7: Commission System ✓
- [ ] Create `cyclex.commission` model:
  - [ ] Collector (many2one)
  - [ ] Request (many2one)
  - [ ] Order value
  - [ ] Commission rate
  - [ ] Commission amount
  - [ ] Status (pending/paid)
  - [ ] Payment date
- [ ] Add commission calculation on order completion
- [ ] Create commission payout tracking

---

### Phase 2: Views & UI (Odoo Backend)

#### Checkpoint 2.1: User Management Views ✓
- [ ] Create tree/list view for customers
- [ ] Create form view for customer details
- [ ] Create tree/list view for collectors
- [ ] Create form view for collector registration approval
- [ ] Add verification status indicators
- [ ] Create search/filter views

#### Checkpoint 2.2: Categories & Products Views ✓
- [ ] Create tree/list view for categories (hierarchical)
- [ ] Create form view for categories
- [ ] Create tree/list view for products
- [ ] Create form view for products
- [ ] Add kanban view for products (with images)

#### Checkpoint 2.3: Requests/Orders Views ✓
- [ ] Create tree/list view for requests (all statuses)
- [ ] Create form view for request details
- [ ] Add status pipeline (kanban view)
- [ ] Create calendar view for pickup dates
- [ ] Add map view for request locations (optional)
- [ ] Create customer-facing order history view

#### Checkpoint 2.4: Wallet & Commission Views ✓
- [ ] Create wallet balance dashboard
- [ ] Create transaction history tree/list view
- [ ] Create withdrawal request form
- [ ] Create commission tracking tree/list view
- [ ] Create commission payout form

#### Checkpoint 2.5: Reporting & Analytics ✓
- [ ] Create dashboard for admin:
  - [ ] Total requests by status
  - [ ] Revenue overview
  - [ ] Commission summary
  - [ ] Top collectors
  - [ ] Category/product popularity
- [ ] Create collector performance reports
- [ ] Create customer activity reports

---

### Phase 3: API Development (Controllers)

#### Checkpoint 3.1: Authentication APIs ✓
- [ ] `/api/cyclex/login` (POST)
  - [ ] Accept phone number & password
  - [ ] Return auth token + user profile
- [ ] `/api/cyclex/register` (POST)
  - [ ] Accept: name, phone, password, confirm_password
  - [ ] Optional: fcm_token, language
  - [ ] Generate 6-digit verification code
  - [ ] Send SMS via SMS Misr
  - [ ] Return success + user_id
- [ ] `/api/cyclex/verify` (POST)
  - [ ] Accept: phone, verification_code
  - [ ] Activate account on success
  - [ ] Return auth token
- [ ] `/api/cyclex/resend-code` (POST)
  - [ ] Resend verification code via SMS

#### Checkpoint 3.2: Categories & Products APIs ✓
- [ ] `/api/cyclex/categories` (GET)
  - [ ] Return hierarchical category list
  - [ ] Filter by parent category
  - [ ] Support language parameter (ar/en)
- [ ] `/api/cyclex/products` (GET)
  - [ ] Return products by category
  - [ ] Include pricing, images
  - [ ] Support search/filter

#### Checkpoint 3.3: Request/Order APIs ✓
- [ ] `/api/cyclex/request/create` (POST)
  - [ ] Accept: category_id, product_id, quantity, weight, photos (base64), pickup_date
  - [ ] Auto-detect GPS from user profile
  - [ ] Calculate price
  - [ ] Generate QR code
  - [ ] Return request details
- [ ] `/api/cyclex/request/list` (GET)
  - [ ] Return user's request history
  - [ ] Filter by status
  - [ ] Pagination support
- [ ] `/api/cyclex/request/details/:id` (GET)
  - [ ] Return full request details including QR code
- [ ] `/api/cyclex/request/cancel/:id` (POST)
  - [ ] Allow cancellation if status is pending

#### Checkpoint 3.4: Collector APIs ✓
- [ ] `/api/cyclex/collector/register` (POST)
  - [ ] Accept: name, phone, id_number, vehicle_type, working_areas
  - [ ] Set status to "pending approval"
  - [ ] Notify admin
- [ ] `/api/cyclex/collector/available-orders` (GET)
  - [ ] Return orders in collector's working areas
  - [ ] Filter by status (pending/available)
- [ ] `/api/cyclex/collector/accept-order/:id` (POST)
  - [ ] Assign order to collector
  - [ ] Set 3-day completion deadline
  - [ ] Notify customer
- [ ] `/api/cyclex/collector/reject-order/:id` (POST)
  - [ ] Reject order assignment
- [ ] `/api/cyclex/collector/scan-qr` (POST)
  - [ ] Validate QR code
  - [ ] Return order details
- [ ] `/api/cyclex/collector/complete-order/:id` (POST)
  - [ ] Mark order as collected
  - [ ] Update wallet balance
  - [ ] Calculate commission
  - [ ] Notify customer

#### Checkpoint 3.5: Wallet APIs ✓
- [ ] `/api/cyclex/wallet/balance` (GET)
  - [ ] Return current balance, total earned, withdrawable amount
- [ ] `/api/cyclex/wallet/transactions` (GET)
  - [ ] Return transaction history
  - [ ] Pagination support
- [ ] `/api/cyclex/wallet/withdraw` (POST)
  - [ ] Accept: amount
  - [ ] Validate minimum threshold
  - [ ] Create withdrawal request

#### Checkpoint 3.6: Rating & Feedback APIs ✓
- [ ] `/api/cyclex/order/rate/:id` (POST)
  - [ ] Accept: rating (1-5), comments
  - [ ] Update order record
  - [ ] Update collector's average rating

---

### Phase 4: Integrations

#### Checkpoint 4.1: SMS Misr Integration ✓
- [ ] Set up SMS Misr API credentials in Odoo settings
- [ ] Create SMS sending service:
  - [ ] Generate 6-digit random code
  - [ ] Format SMS message (Arabic/English)
  - [ ] Send via SMS Misr API
  - [ ] Log SMS status
- [ ] Add error handling and retry logic
- [ ] Create SMS log model for tracking

#### Checkpoint 4.2: Firebase FCM Integration ✓
- [ ] Create Firebase project
- [ ] Add Android app to Firebase
- [ ] Add iOS app to Firebase
- [ ] Download configuration files
- [ ] Set up FCM server key in Odoo
- [ ] Create notification service:
  - [ ] Order status updates
  - [ ] Collector assignment
  - [ ] Order completion
  - [ ] Withdrawal approval
  - [ ] Custom admin notifications
- [ ] Support multilingual notifications

#### Checkpoint 4.3: QR Code Generation ✓
- [ ] Install Python QR code library
- [ ] Generate unique QR codes for each order
- [ ] Store QR as image in order record
- [ ] Create QR validation logic
- [ ] Add QR expiry (optional security)

---

### Phase 5: Business Logic & Rules

#### Checkpoint 5.1: Order Workflow Automation ✓
- [ ] Auto-assign orders to collectors (based on location)
- [ ] Set 3-day deadline on order acceptance
- [ ] Auto-revert unfulfilled orders to "available" after 3 days
- [ ] Send automated notifications at each status change
- [ ] Prevent duplicate order acceptance

#### Checkpoint 5.2: Wallet Logic ✓
- [ ] Auto-credit wallet on order completion
- [ ] Validate withdrawal threshold (1000 EGP)
- [ ] Create withdrawal approval workflow
- [ ] Track wallet transaction history
- [ ] Prevent negative balance

#### Checkpoint 5.3: Commission Calculation ✓
- [ ] Calculate commission on order completion
- [ ] Apply collector-specific commission rates
- [ ] Track unpaid commissions
- [ ] Create commission payout workflow
- [ ] Generate commission reports

#### Checkpoint 5.4: Validation & Security ✓
- [ ] Phone number format validation
- [ ] Password strength requirements
- [ ] Rate limiting for API calls
- [ ] Token expiry and refresh logic
- [ ] Image upload size limits (photos)
- [ ] Prevent duplicate phone number registration
- [ ] Collector working area limit (max 5)

---

### Phase 6: Testing & Documentation

#### Checkpoint 6.1: API Testing (Postman) ✓
- [ ] Create Postman collection for all endpoints
- [ ] Test authentication flow
- [ ] Test customer workflow (register → create request → track order)
- [ ] Test collector workflow (register → accept order → complete)
- [ ] Test wallet operations
- [ ] Test edge cases and error handling
- [ ] Document API responses

#### Checkpoint 6.2: Backend Testing ✓
- [ ] Test model constraints and validations
- [ ] Test computed fields
- [ ] Test workflow transitions
- [ ] Test commission calculations
- [ ] Test SMS sending (sandbox mode)
- [ ] Test Firebase notifications (test devices)

#### Checkpoint 6.3: Documentation ✓
- [ ] API documentation (endpoints, parameters, responses)
- [ ] Database schema documentation
- [ ] User roles and permissions guide
- [ ] Admin dashboard guide
- [ ] Integration setup guides (SMS, Firebase)
- [ ] Mobile app integration guide

---

### Phase 7: Mobile App Coordination

#### Checkpoint 7.1: iOS App (Swift) ✓
- [ ] Share API documentation with iOS team
- [ ] Provide Firebase configuration
- [ ] Coordinate authentication flow
- [ ] Coordinate UI/UX for customer features
- [ ] Coordinate UI/UX for collector features
- [ ] Test API integration
- [ ] Implement QR scanner

#### Checkpoint 7.2: Android App (Kotlin) ✓
- [ ] Share API documentation with Android team
- [ ] Provide Firebase configuration
- [ ] Coordinate authentication flow
- [ ] Coordinate UI/UX for customer features
- [ ] Coordinate UI/UX for collector features
- [ ] Test API integration
- [ ] Implement QR scanner

#### Checkpoint 7.3: Cross-Platform Testing ✓
- [ ] Test notifications on both platforms
- [ ] Test photo upload functionality
- [ ] Test GPS location capture
- [ ] Test QR code generation and scanning
- [ ] Test real-time order status updates
- [ ] Test multilingual support (Arabic/English)

---

### Phase 8: Deployment & Launch

#### Checkpoint 8.1: Staging Environment ✓
- [ ] Set up staging Odoo instance
- [ ] Deploy CycleX module
- [ ] Configure SMS Misr (test mode)
- [ ] Configure Firebase (dev project)
- [ ] Load sample data (categories, products, test users)
- [ ] Conduct UAT (User Acceptance Testing)

#### Checkpoint 8.2: Production Setup ✓
- [ ] Set up production Odoo instance
- [ ] Configure production database
- [ ] Set up SMS Misr production credentials
- [ ] Set up Firebase production project
- [ ] Configure backups
- [ ] Set up monitoring and logging

#### Checkpoint 8.3: Go Live ✓
- [ ] Deploy to production
- [ ] Onboard initial collectors
- [ ] Launch marketing campaign
- [ ] Monitor system performance
- [ ] Provide user support
- [ ] Collect feedback for improvements

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

### External Services
- **SMS Misr:** API credentials required
- **Firebase:** Project setup for Android & iOS
- **GPS/Maps:** Google Maps API (optional for location services)

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

**Last Updated:** October 15, 2025  
**Version:** 1.0  
**Status:** Planning Phase

---

## Notes

- All checkboxes are unchecked for lazy planning - mark them as you progress
- Phases can be executed in parallel where dependencies allow
- Prioritize Phase 1-3 for MVP (Minimum Viable Product)
- Phase 4-5 for production readiness
- Phase 6-8 for launch preparation

**Ready to start building! 🎉**

