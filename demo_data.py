"""
Demo/Mock Data for CycleX App
Used when API is unavailable or for demonstration
"""

DEMO_CATEGORIES = [
    {
        "id": 1,
        "name": "Plastic Bottles",
        "description": "PET and HDPE plastic bottles",
        "parent_id": None,
        "has_children": False,
        "product_count": 12,
        "image": None
    },
    {
        "id": 2,
        "name": "Paper & Cardboard",
        "description": "Newspapers, magazines, cardboard boxes",
        "parent_id": None,
        "has_children": False,
        "product_count": 8,
        "image": None
    },
    {
        "id": 3,
        "name": "Metal",
        "description": "Aluminum cans, steel items",
        "parent_id": None,
        "has_children": False,
        "product_count": 6,
        "image": None
    },
    {
        "id": 4,
        "name": "Glass",
        "description": "Glass bottles and jars",
        "parent_id": None,
        "has_children": False,
        "product_count": 5,
        "image": None
    },
    {
        "id": 5,
        "name": "Electronics",
        "description": "Small electronic devices",
        "parent_id": None,
        "has_children": False,
        "product_count": 4,
        "image": None
    }
]

DEMO_PRODUCTS = {
    "PLASTIC": [
        {
            "id": 1,
            "name": "PET Bottles (Clear)",
            "description": "Clear PET plastic bottles (water, soda bottles)",
            "category_id": 1,
            "category_name": "Plastic Bottles",
            "price_per_kg": 3.5,
            "currency": "USD",
            "currency_symbol": "$",
            "image": None
        },
        {
            "id": 2,
            "name": "HDPE Bottles (Colored)",
            "description": "HDPE plastic bottles (milk jugs, detergent bottles)",
            "category_id": 1,
            "category_name": "Plastic Bottles",
            "price_per_kg": 2.8,
            "currency": "USD",
            "currency_symbol": "$",
            "image": None
        }
    ],
    "PAPER": [
        {
            "id": 3,
            "name": "Newspapers",
            "description": "Old newspapers and magazines",
            "category_id": 2,
            "category_name": "Paper & Cardboard",
            "price_per_kg": 1.2,
            "currency": "USD",
            "currency_symbol": "$",
            "image": None
        }
    ],
    "METAL": [
        {
            "id": 4,
            "name": "Aluminum Cans",
            "description": "Aluminum beverage cans",
            "category_id": 3,
            "category_name": "Metal",
            "price_per_kg": 4.5,
            "currency": "USD",
            "currency_symbol": "$",
            "image": None
        }
    ],
    "GLASS": [
        {
            "id": 5,
            "name": "Glass Bottles",
            "description": "Clear and colored glass bottles",
            "category_id": 4,
            "category_name": "Glass",
            "price_per_kg": 0.8,
            "currency": "USD",
            "currency_symbol": "$",
            "image": None
        }
    ],
    "ELECTRONICS": [
        {
            "id": 6,
            "name": "Small Electronics",
            "description": "Phones, tablets, small devices",
            "category_id": 5,
            "category_name": "Electronics",
            "price_per_kg": 15.0,
            "currency": "USD",
            "currency_symbol": "$",
            "image": None
        }
    ]
}

DEMO_ORDERS = [
    {
        "id": 1,
        "status": "pending",
        "total_amount": 25.50,
        "currency_symbol": "E£",
        "pickup_date": "2025-11-15",
        "created_at": "2025-11-13 10:30:00",
        "items": [
            {"name": "PET Bottles", "quantity": 5, "weight": 2.5}
        ]
    },
    {
        "id": 2,
        "status": "assigned",
        "total_amount": 18.75,
        "currency_symbol": "E£",
        "pickup_date": "2025-11-14",
        "created_at": "2025-11-12 14:20:00",
        "items": [
            {"name": "Aluminum Cans", "quantity": 10, "weight": 1.5}
        ]
    },
    {
        "id": 3,
        "status": "completed",
        "total_amount": 42.00,
        "currency_symbol": "E£",
        "pickup_date": "2025-11-10",
        "created_at": "2025-11-08 09:15:00",
        "items": [
            {"name": "Mixed Plastic", "quantity": 8, "weight": 4.0}
        ]
    }
]

DEMO_WALLET = {
    "balance": 125.50,
    "total_earned": 450.75,
    "total_withdrawn": 325.25,
    "withdrawal_threshold": 100.0,
    "currency": "EGP",
    "currency_symbol": "E£"
}

DEMO_TRANSACTIONS = [
    {
        "id": 1,
        "type": "credit",
        "amount": 25.50,
        "date": "2025-11-13 10:30:00",
        "description": "Order #1 completed",
        "status": "completed"
    },
    {
        "id": 2,
        "type": "credit",
        "amount": 18.75,
        "date": "2025-11-12 14:20:00",
        "description": "Order #2 completed",
        "status": "completed"
    },
    {
        "id": 3,
        "type": "debit",
        "amount": -50.00,
        "date": "2025-11-10 16:45:00",
        "description": "Withdrawal",
        "status": "completed"
    }
]

DEMO_PROFILE = {
    "user_id": 1,
    "name": "Demo User",
    "phone": "01000000000",
    "email": "demo@example.com",
    "user_type": "customer",
    "language": "en",
    "account_status": "active",
    "verified": True,
    "total_requests": 15,
    "total_earnings": 450.75
}

DEMO_COLLECTOR_ORDERS = [
    {
        "id": 10,
        "distance": 2.5,
        "total_amount": 30.00,
        "pickup_date": "2025-11-15",
        "status": "pending",
        "customer_name": "Ahmed Ali",
        "address": "123 Main St, Cairo"
    },
    {
        "id": 11,
        "distance": 5.2,
        "total_amount": 45.50,
        "pickup_date": "2025-11-16",
        "status": "pending",
        "customer_name": "Sara Mohamed",
        "address": "456 Park Ave, Giza"
    }
]

DEMO_HOME_SUMMARY = {
    "balance": 125.50,
    "total_earnings": 450.75,
    "active_orders_count": 2,
    "total_requests": 15,
    "currency_symbol": "E£"
}

DEMO_COLLECTOR_HOME = {
    "available_orders_count": 5,
    "assigned_orders_count": 2,
    "total_orders_completed": 45,
    "total_earnings": 1250.50,
    "average_rating": 4.5,
    "approval_status": "approved",
    "currency_symbol": "E£"
}

