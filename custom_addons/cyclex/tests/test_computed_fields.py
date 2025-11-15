# -*- coding: utf-8 -*-

from odoo.tests.common import TransactionCase
from datetime import timedelta
from odoo import fields


class TestComputedFields(TransactionCase):
    """Test all computed fields"""
    
    def setUp(self):
        super(TestComputedFields, self).setUp()
        self.Partner = self.env['res.partner']
        self.Product = self.env['cyclex.product']
        self.Request = self.env['cyclex.request']
        self.Commission = self.env['cyclex.commission']
        
        # Create test customer
        self.customer = self.Partner.create({
            'name': 'Test Customer',
            'phone': '+201999999999',
            'is_cyclex_user': True,
            'cyclex_user_type': 'customer',
            'phone_verified': True,
        })
        
        # Create test collector
        self.collector = self.Partner.create({
            'name': 'Test Collector',
            'phone': '+201888888888',
            'is_cyclex_user': True,
            'cyclex_user_type': 'collector',
            'phone_verified': True,
            'collector_verified': True,
            'commission_rate': 15.00,
        })
        
        # Get or create test product
        self.product = self.Product.search([], limit=1)
        if not self.product:
            category = self.env['cyclex.category'].create({
                'name': 'Test Category',
                'name_ar': 'فئة اختبار',
            })
            self.product = self.Product.create({
                'name': 'Test Product',
                'name_ar': 'منتج اختبار',
                'category_id': category.id,
                'price_per_kg': 5.00,
                'unit_of_measure': 'kg',
            })
    
    def test_wallet_current_balance(self):
        """Test wallet.current_balance = total_credits - total_debits"""
        wallet = self.customer.wallet_id
        
        # Initial balance should be 0
        self.assertEqual(wallet.current_balance, 0.0)
        self.assertEqual(wallet.total_credits, 0.0)
        self.assertEqual(wallet.total_debits, 0.0)
        
        # Add credits
        wallet.add_credit(100.00, 'Credit 1', request_id=1)
        wallet.add_credit(50.00, 'Credit 2', request_id=2)
        
        self.assertEqual(wallet.total_credits, 150.0)
        self.assertEqual(wallet.current_balance, 150.0)
        
        # Add debit
        wallet.add_debit(30.00, 'Debit 1')
        
        self.assertEqual(wallet.total_debits, 30.0)
        self.assertEqual(wallet.current_balance, 120.0)  # 150 - 30
        
        # Add another debit
        wallet.add_debit(20.00, 'Debit 2')
        
        self.assertEqual(wallet.total_debits, 50.0)
        self.assertEqual(wallet.current_balance, 100.0)  # 150 - 50
    
    def test_wallet_transaction_count(self):
        """Test wallet.transaction_count updates correctly"""
        wallet = self.customer.wallet_id
        
        # Initial count
        self.assertEqual(wallet.transaction_count, 0)
        
        # Add transactions
        wallet.add_credit(100.00, 'Test 1', request_id=1)
        wallet.invalidate_cache(['transaction_count'])
        self.assertEqual(wallet.transaction_count, 1)
        
        wallet.add_credit(50.00, 'Test 2', request_id=2)
        wallet.invalidate_cache(['transaction_count'])
        self.assertEqual(wallet.transaction_count, 2)
        
        wallet.add_debit(20.00, 'Test 3')
        wallet.invalidate_cache(['transaction_count'])
        self.assertEqual(wallet.transaction_count, 3)
    
    def test_request_calculated_price(self):
        """Test request.calculated_price = quantity × price_per_kg"""
        
        # Test 1: Integer quantity
        request1 = self.Request.create({
            'customer_id': self.customer.id,
            'product_id': self.product.id,
            'quantity': 10.0,
            'unit': 'kg',
            'pickup_date': fields.Date.today() + timedelta(days=1),
            'pickup_time': 'morning',
            'location_latitude': 30.0444,
            'location_longitude': 31.2357,
            'address': 'Test address 1',
        })
        
        expected_price1 = 10.0 * self.product.price_per_kg
        self.assertEqual(request1.calculated_price, expected_price1)
        
        # Test 2: Decimal quantity
        request2 = self.Request.create({
            'customer_id': self.customer.id,
            'product_id': self.product.id,
            'quantity': 12.5,
            'unit': 'kg',
            'pickup_date': fields.Date.today() + timedelta(days=1),
            'pickup_time': 'morning',
            'location_latitude': 30.0444,
            'location_longitude': 31.2357,
            'address': 'Test address 2',
        })
        
        expected_price2 = 12.5 * self.product.price_per_kg
        self.assertEqual(request2.calculated_price, expected_price2)
        
        # Test 3: Large quantity
        request3 = self.Request.create({
            'customer_id': self.customer.id,
            'product_id': self.product.id,
            'quantity': 100.0,
            'unit': 'kg',
            'pickup_date': fields.Date.today() + timedelta(days=1),
            'pickup_time': 'morning',
            'location_latitude': 30.0444,
            'location_longitude': 31.2357,
            'address': 'Test address 3',
        })
        
        expected_price3 = 100.0 * self.product.price_per_kg
        self.assertEqual(request3.calculated_price, expected_price3)
    
    def test_commission_amount_calculation(self):
        """Test commission.commission_amount = amount × rate / 100"""
        
        # Create request with known price
        request = self.Request.create({
            'customer_id': self.customer.id,
            'product_id': self.product.id,
            'quantity': 20.0,  # 20 × 5 = 100 EGP
            'unit': 'kg',
            'pickup_date': fields.Date.today() + timedelta(days=1),
            'pickup_time': 'morning',
            'location_latitude': 30.0444,
            'location_longitude': 31.2357,
            'address': 'Test address',
            'status': 'assigned',
            'collector_id': self.collector.id,
        })
        
        # Complete order - creates commission
        request.write({'status': 'collected'})
        
        # Get commission
        commission = self.Commission.search([('request_id', '=', request.id)])
        
        # Verify calculation
        self.assertEqual(commission.amount, 100.0)  # Request price
        self.assertEqual(commission.commission_rate, 15.0)  # Collector rate
        expected_commission = 100.0 * 15.0 / 100.0
        self.assertEqual(commission.commission_amount, expected_commission)  # 15.00
    
    def test_commission_different_rates(self):
        """Test commission with different collector rates"""
        
        # Create collector with 20% rate
        collector_20 = self.Partner.create({
            'name': 'Collector 20%',
            'phone': '+201777777777',
            'is_cyclex_user': True,
            'cyclex_user_type': 'collector',
            'phone_verified': True,
            'collector_verified': True,
            'commission_rate': 20.00,
        })
        
        # Create and complete request
        request = self.Request.create({
            'customer_id': self.customer.id,
            'product_id': self.product.id,
            'quantity': 20.0,  # 100 EGP
            'unit': 'kg',
            'pickup_date': fields.Date.today() + timedelta(days=1),
            'pickup_time': 'morning',
            'location_latitude': 30.0444,
            'location_longitude': 31.2357,
            'address': 'Test address',
            'status': 'assigned',
            'collector_id': collector_20.id,
        })
        
        request.write({'status': 'collected'})
        
        # Get commission
        commission = self.Commission.search([('request_id', '=', request.id)])
        
        # Verify uses collector's custom rate
        self.assertEqual(commission.commission_rate, 20.0)
        self.assertEqual(commission.commission_amount, 20.0)  # 100 × 0.20
    
    def test_total_credits_and_debits(self):
        """Test wallet total_credits and total_debits computation"""
        wallet = self.customer.wallet_id
        
        # Add multiple credits
        amounts_credit = [100.00, 50.00, 25.50, 75.25]
        for i, amount in enumerate(amounts_credit):
            wallet.add_credit(amount, f'Credit {i+1}', request_id=i+1)
        
        expected_total_credits = sum(amounts_credit)
        self.assertEqual(wallet.total_credits, expected_total_credits)  # 250.75
        
        # Add multiple debits
        amounts_debit = [30.00, 20.50]
        for i, amount in enumerate(amounts_debit):
            wallet.add_debit(amount, f'Debit {i+1}')
        
        expected_total_debits = sum(amounts_debit)
        self.assertEqual(wallet.total_debits, expected_total_debits)  # 50.50
        
        # Verify final balance
        expected_balance = expected_total_credits - expected_total_debits
        self.assertEqual(wallet.current_balance, expected_balance)  # 200.25

