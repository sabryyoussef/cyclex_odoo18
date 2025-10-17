# CycleX - Recycling Management System

## Overview

CycleX is a comprehensive recycling management platform built on Odoo 18 that connects customers who want to sell recyclable items with collectors who pick them up.

## Features

- 📱 **Mobile Applications**: Native iOS (Swift) and Android (Kotlin) apps
- 💰 **Wallet System**: Automatic earnings tracking and withdrawal management
- 📞 **SMS Verification**: Secure phone-based authentication via SMS Misr
- 🔔 **Push Notifications**: Real-time updates via Firebase Cloud Messaging
- 📷 **QR Code Verification**: Secure order confirmation
- 🌐 **Multilingual**: Arabic and English support
- 📍 **GPS Tracking**: Automatic location detection
- ⭐ **Rating System**: Customer feedback and performance tracking

## Installation

1. Copy the `cyclex` module to your Odoo addons directory
2. Update the app list in Odoo
3. Install the CycleX module
4. Configure SMS Misr credentials in Settings
5. Configure Firebase credentials in Settings

## Configuration

### SMS Misr Setup
Navigate to **CycleX > Configuration > Settings** and configure:
- SMS Misr Username
- SMS Misr Password
- Sender Name

### Firebase Setup
Navigate to **CycleX > Configuration > Settings** and configure:
- Firebase Server Key
- Firebase Project ID

## Module Structure

```
cyclex/
├── __init__.py
├── __manifest__.py
├── controllers/
│   ├── __init__.py
│   └── main.py
├── models/
│   ├── __init__.py
│   ├── res_partner.py
│   ├── cyclex_category.py
│   ├── cyclex_product.py
│   ├── cyclex_request.py
│   ├── cyclex_wallet.py
│   ├── cyclex_commission.py
│   └── cyclex_working_area.py
├── views/
│   ├── cyclex_menu.xml
│   ├── res_partner_views.xml
│   ├── cyclex_category_views.xml
│   ├── cyclex_product_views.xml
│   ├── cyclex_request_views.xml
│   ├── cyclex_wallet_views.xml
│   └── cyclex_commission_views.xml
├── security/
│   ├── cyclex_security.xml
│   └── ir.model.access.csv
├── data/
│   └── cyclex_data.xml
└── static/
    └── description/
        ├── icon.svg
        ├── icon.png
        ├── banner.png
        └── index.html
```

## User Roles

### Customer
- Create and track recycling requests
- View wallet balance and transactions
- Rate and review collectors

### Collector
- View and accept available orders
- Scan QR codes for verification
- Track commissions and earnings

### Manager
- Manage categories and products
- Approve collector registrations
- View reports and analytics

### Administrator
- Full system access
- Configure integrations
- Manage system settings

## API Endpoints

Health check endpoint is available at:
```
GET /api/cyclex/health
```

Additional API endpoints will be added in Phase 3 of development.

## Dependencies

- Odoo 18
- Python packages:
  - `qrcode`
  - `requests`
  - `firebase-admin` (optional, for FCM)

## Support

For issues and questions, please contact the development team.

## License

LGPL-3

## Version

1.0.0

