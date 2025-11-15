#!/usr/bin/env python3
"""
Populate CycleX Demo Data
Run this from Odoo shell: python3 odoo-bin shell -c odoo.conf -d edu_demo
Then: exec(open('/home/sabry3/edu_demo/custom_addons/cyclex/scripts/populate_demo_data.py').read())
"""

import logging
from datetime import datetime, timedelta

_logger = logging.getLogger(__name__)

def populate_demo_data(env):
    """Populate demo categories, products, and sample orders"""
    
    _logger.info("=" * 80)
    _logger.info("Starting CycleX Demo Data Population")
    _logger.info("=" * 80)
    
    # ====================
    # 1. CREATE CATEGORIES
    # ====================
    _logger.info("\n📦 Creating Categories...")
    
    Category = env['cyclex.category'].sudo()
    
    categories_data = [
        {
            'name': 'Plastic',
            'name_ar': 'بلاستيك',
            'description': 'PET and HDPE plastic bottles, containers',
            'description_ar': 'زجاجات وحاويات بلاستيك PET و HDPE',
            'price_per_kg': 3.50,
            'active': True,
        },
        {
            'name': 'Paper',
            'name_ar': 'ورق',
            'description': 'Newspapers, magazines, cardboard boxes',
            'description_ar': 'صحف، مجلات، صناديق كرتون',
            'price_per_kg': 1.20,
            'active': True,
        },
        {
            'name': 'Metal',
            'name_ar': 'معادن',
            'description': 'Aluminum cans, steel items',
            'description_ar': 'علب ألمنيوم، معادن حديدية',
            'price_per_kg': 4.50,
            'active': True,
        },
        {
            'name': 'Glass',
            'name_ar': 'زجاج',
            'description': 'Glass bottles and jars',
            'description_ar': 'زجاجات وبرطمانات زجاجية',
            'price_per_kg': 0.80,
            'active': True,
        },
        {
            'name': 'Electronics',
            'name_ar': 'إلكترونيات',
            'description': 'Small electronic devices',
            'description_ar': 'أجهزة إلكترونية صغيرة',
            'price_per_kg': 15.00,
            'active': True,
        },
    ]
    
    categories = {}
    for cat_data in categories_data:
        existing = Category.search([('name', '=', cat_data['name'])], limit=1)
        if existing:
            _logger.info(f"  ✓ Category '{cat_data['name']}' already exists (ID: {existing.id})")
            categories[cat_data['name']] = existing
        else:
            category = Category.create(cat_data)
            _logger.info(f"  ✓ Created category '{cat_data['name']}' (ID: {category.id})")
            categories[cat_data['name']] = category
    
    # ====================
    # 2. CREATE PRODUCTS
    # ====================
    _logger.info("\n🔹 Creating Products...")
    
    Product = env['cyclex.product'].sudo()
    
    products_data = [
        # Plastic Products
        {
            'name': 'PET Bottles (Clear)',
            'name_ar': 'زجاجات PET (شفاف)',
            'description': 'Clear PET plastic bottles (water, soda)',
            'category_id': categories['Plastic'].id,
            'price_per_kg': 3.80,
            'active': True,
        },
        {
            'name': 'HDPE Bottles (Colored)',
            'name_ar': 'زجاجات HDPE (ملون)',
            'description': 'HDPE plastic bottles (milk, detergent)',
            'category_id': categories['Plastic'].id,
            'price_per_kg': 3.20,
            'active': True,
        },
        {
            'name': 'Plastic Bags',
            'name_ar': 'أكياس بلاستيك',
            'description': 'Clean plastic shopping bags',
            'category_id': categories['Plastic'].id,
            'price_per_kg': 2.50,
            'active': True,
        },
        
        # Paper Products
        {
            'name': 'Newspapers',
            'name_ar': 'صحف',
            'description': 'Old newspapers and magazines',
            'category_id': categories['Paper'].id,
            'price_per_kg': 1.20,
            'active': True,
        },
        {
            'name': 'Cardboard Boxes',
            'name_ar': 'صناديق كرتون',
            'description': 'Corrugated cardboard boxes',
            'category_id': categories['Paper'].id,
            'price_per_kg': 1.50,
            'active': True,
        },
        {
            'name': 'Office Paper',
            'name_ar': 'ورق مكتب',
            'description': 'White office paper',
            'category_id': categories['Paper'].id,
            'price_per_kg': 2.00,
            'active': True,
        },
        
        # Metal Products
        {
            'name': 'Aluminum Cans',
            'name_ar': 'علب ألمنيوم',
            'description': 'Aluminum beverage cans',
            'category_id': categories['Metal'].id,
            'price_per_kg': 5.00,
            'active': True,
        },
        {
            'name': 'Copper Wire',
            'name_ar': 'أسلاك نحاس',
            'description': 'Copper electrical wire',
            'category_id': categories['Metal'].id,
            'price_per_kg': 25.00,
            'active': True,
        },
        
        # Glass Products
        {
            'name': 'Glass Bottles (Clear)',
            'name_ar': 'زجاجات زجاج (شفاف)',
            'description': 'Clear glass bottles',
            'category_id': categories['Glass'].id,
            'price_per_kg': 0.90,
            'active': True,
        },
        {
            'name': 'Glass Bottles (Colored)',
            'name_ar': 'زجاجات زجاج (ملون)',
            'description': 'Colored glass bottles',
            'category_id': categories['Glass'].id,
            'price_per_kg': 0.70,
            'active': True,
        },
        
        # Electronics
        {
            'name': 'Mobile Phones',
            'name_ar': 'هواتف محمولة',
            'description': 'Old mobile phones',
            'category_id': categories['Electronics'].id,
            'price_per_kg': 20.00,
            'active': True,
        },
        {
            'name': 'Small Appliances',
            'name_ar': 'أجهزة صغيرة',
            'description': 'Small electronic appliances',
            'category_id': categories['Electronics'].id,
            'price_per_kg': 12.00,
            'active': True,
        },
    ]
    
    products = []
    for prod_data in products_data:
        existing = Product.search([
            ('name', '=', prod_data['name']),
            ('category_id', '=', prod_data['category_id'])
        ], limit=1)
        
        if existing:
            _logger.info(f"  ✓ Product '{prod_data['name']}' already exists (ID: {existing.id})")
            products.append(existing)
        else:
            product = Product.create(prod_data)
            _logger.info(f"  ✓ Created product '{prod_data['name']}' (ID: {product.id})")
            products.append(product)
    
    # ====================
    # 3. CREATE TEST USER
    # ====================
    _logger.info("\n👤 Ensuring Test User...")
    
    Partner = env['res.partner'].sudo()
    User = env['res.users'].sudo()
    
    test_phone = '01000111111'
    test_partner = Partner.search([('phone', '=', test_phone)], limit=1)
    
    if test_partner:
        _logger.info(f"  ✓ Test user exists: {test_partner.name} (ID: {test_partner.id})")
    else:
        _logger.info(f"  ⚠ Test user not found - please register manually")
    
    # ====================
    # 4. SUMMARY
    # ====================
    _logger.info("\n" + "=" * 80)
    _logger.info("✅ DEMO DATA POPULATION COMPLETE!")
    _logger.info("=" * 80)
    _logger.info(f"Categories created: {len(categories)}")
    _logger.info(f"Products created: {len(products)}")
    _logger.info("\n📊 Summary by Category:")
    for cat_name, cat_obj in categories.items():
        prod_count = Product.search_count([('category_id', '=', cat_obj.id)])
        _logger.info(f"  • {cat_name}: {prod_count} products")
    
    _logger.info("\n🔗 Test in Streamlit:")
    _logger.info("  URL: http://localhost:8501")
    _logger.info(f"  Phone: {test_phone}")
    _logger.info("  Password: Test1234")
    _logger.info("  OTP: 123456")
    _logger.info("=" * 80)
    
    return {
        'categories': categories,
        'products': products,
        'success': True
    }


# If running directly in Odoo shell
if __name__ == '__main__' or 'env' in dir():
    try:
        result = populate_demo_data(env)
        print("\n✅ Demo data populated successfully!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

