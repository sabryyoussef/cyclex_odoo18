# -*- coding: utf-8 -*-
{
    'name': 'CycleX - Recycling Management System',
    'version': '18.0.1.0.1',
    'category': 'Sales',
    'summary': 'Recycling mobile application with collector and customer management',
    'description': """
CycleX - Recycling Management System
=====================================
A comprehensive recycling platform that connects customers who want to sell 
recyclable items with collectors who pick them up.

Key Features:
-------------
* Customer mobile app for selling recyclable items
* Collector mobile app for picking up items
* Commission-based revenue model
* Wallet system for customer earnings
* SMS verification via SMS Misr
* Push notifications via Firebase FCM
* QR code-based order verification
* Multi-language support (Arabic/English)
* GPS-based location tracking
* Rating and feedback system

Workflow:
---------
1. Customers register and verify their phone number
2. Customers create requests for recyclable items
3. Collectors view and accept available orders
4. Collectors pick up items and scan QR code
5. Customer wallet is credited automatically
6. Customers can rate and provide feedback
7. Commission is calculated for collectors

Technical Details:
------------------
* Integrated with SMS Misr for OTP verification
* Firebase Cloud Messaging for notifications
* QR code generation for order verification
* REST API for mobile app integration
    """,
    'author': 'CycleX Team',
    'website': 'https://www.cyclex.app',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'web',
        'mail',
        'contacts',
    ],
    'data': [
        # Security
        'security/cyclex_security.xml',
        'security/ir.model.access.csv',
        
        # Data
        'data/cyclex_data.xml',
        'data/cyclex_sequence.xml',
        
        # Views (loaded before menu to ensure actions exist)
        'views/res_partner_views.xml',
        'views/cyclex_working_area_views.xml',
        'views/cyclex_category_views.xml',
        'views/cyclex_product_views.xml',
        'views/cyclex_request_views.xml',
        'views/cyclex_wallet_views.xml',
        'views/cyclex_commission_views.xml',
        
        # Menu (loaded last to reference existing actions)
        'views/cyclex_menu.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'cyclex/static/src/img/icon.png',
        ],
    },
    'images': [
        'static/description/banner.png',
        'static/description/icon.png',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'external_dependencies': {
        'python': ['qrcode', 'requests'],
    },
}

