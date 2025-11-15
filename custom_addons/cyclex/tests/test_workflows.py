# -*- coding: utf-8 -*-

from odoo.tests.common import TransactionCase
from datetime import timedelta
from odoo import fields


class TestWorkflows(TransactionCase):
    """Test workflow transitions and business logic"""
    
    def setUp(self):
        super(TestWorkflows, self).setUp()
        self.Partner = self.env['res.partner']
        self.Product = self.env['cyclex.product']
        self.Request = self.env['cyclex.request']
        self.Wallet = self.env['cyclex.wallet']
        self.Transaction = self.env['cyclex.wallet.transaction']
        
        # Create test customer
        self.customer = self.Partner.create({
            'name': 'Test Customer',
            'phone': '+201999999998',
            'is_cyclex_user': True,
            'cyclex_user_type': 'customer',
            'phone_verified': True,
        })
        
        # Create test collector
        self.collector = self.Partner.create({
            'name': 'Test Collector',
            'phone': '+201888888887',
            'is_cyclex_user': True,
            'cyclex_user_type': 'collector',
            'phone_verified': True,
            'collector_verified': True,
            'commission_rate': 15.00,
        })
        
        # Get test product
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
    
    def test_request_workflow_complete(self):
        """Test complete request workflow: pending → assigned → collected"""
        
        # Step 1: Create request (auto status = pending)
        request = self.Request.create({
            'customer_id': self.customer.id,
            'product_id': self.product.id,
            'quantity': 10.0,
            'unit': 'kg',
            'pickup_date': fields.Date.today() + timedelta(days=1),
            'pickup_time': 'morning',
            'location_latitude': 30.0444,
            'location_longitude': 31.2357,
            'address': 'Test address',
        })
        
        self.assertEqual(request.status, 'pending')
        self.assertFalse(request.collector_id)
        
        # Step 2: Assign to collector
        request.write({
            'status': 'assigned',
            'collector_id': self.collector.id
        })
        
        self.assertEqual(request.status, 'assigned')
        self.assertEqual(request.collector_id.id, self.collector.id)
        
        # Step 3: Complete order
        request.write({'status': 'collected'})
        
        self.assertEqual(request.status, 'collected')
        self.assertTrue(request.collection_date)
        
        # Verify wallet credited
        wallet = self.customer.wallet_id
        self.assertEqual(wallet.current_balance, request.calculated_price)
        
        # Verify commission created
        commission = self.Commission.search([('request_id', '=', request.id)])
        self.assertTrue(commission)
        self.assertEqual(commission.collector_id.id, self.collector.id)
    
    def test_request_reject_workflow(self):
        """Test reject workflow: assigned → pending"""
        
        # Create and assign request
        request = self.Request.create({
            'customer_id': self.customer.id,
            'product_id': self.product.id,
            'quantity': 10.0,
            'unit': 'kg',
            'pickup_date': fields.Date.today() + timedelta(days=1),
            'pickup_time': 'morning',
            'location_latitude': 30.0444,
            'location_longitude': 31.2357,
            'address': 'Test address',
            'status': 'assigned',
            'collector_id': self.collector.id,
        })
        
        self.assertEqual(request.status, 'assigned')
        
        # Reject order (back to pending)
        request.write({
            'status': 'pending',
            'collector_id': False
        })
        
        self.assertEqual(request.status, 'pending')
        self.assertFalse(request.collector_id)
    
    def test_withdrawal_approval_workflow(self):
        """Test withdrawal: pending → approved"""
        
        wallet = self.customer.wallet_id
        
        # Add balance
        wallet.add_credit(100.00, 'Test credit', request_id=1)
        
        # Request withdrawal
        wallet.add_debit(50.00, 'Withdrawal request')
        
        # Get transaction
        transaction = self.Transaction.search([
            ('wallet_id', '=', wallet.id),
            ('transaction_type', '=', 'debit')
        ], limit=1)
        
        # Should be pending
        self.assertEqual(transaction.withdrawal_status, 'pending')
        
        # Approve withdrawal
        transaction.action_approve_withdrawal()
        
        # Verify approved
        self.assertEqual(transaction.withdrawal_status, 'approved')
        self.assertTrue(transaction.approved_by)
        self.assertTrue(transaction.approval_date)
        
        # Balance should remain deducted
        self.assertEqual(wallet.current_balance, 50.0)
    
    def test_withdrawal_rejection_workflow(self):
        """Test withdrawal: pending → rejected (balance restored)"""
        
        wallet = self.customer.wallet_id
        
        # Add balance
        wallet.add_credit(100.00, 'Test credit', request_id=1)
        initial_balance = wallet.current_balance
        
        # Request withdrawal
        wallet.add_debit(50.00, 'Withdrawal request')
        
        # Balance deducted
        self.assertEqual(wallet.current_balance, 50.0)
        
        # Get transaction
        transaction = self.Transaction.search([
            ('wallet_id', '=', wallet.id),
            ('transaction_type', '=', 'debit')
        ], limit=1)
        
        # Reject withdrawal
        transaction.action_reject_withdrawal()
        
        # Verify rejected
        self.assertEqual(transaction.withdrawal_status, 'rejected')
        self.assertTrue(transaction.rejection_reason)
        
        # Balance should be restored
        wallet.invalidate_cache(['current_balance', 'total_debits'])
        self.assertEqual(wallet.current_balance, initial_balance)  # Back to 100.0
    
    def test_order_completion_auto_credit(self):
        """Test wallet auto-credited on order completion"""
        
        wallet = self.customer.wallet_id
        initial_balance = wallet.current_balance
        
        # Create and complete request
        request = self.Request.create({
            'customer_id': self.customer.id,
            'product_id': self.product.id,
            'quantity': 10.0,
            'unit': 'kg',
            'pickup_date': fields.Date.today() + timedelta(days=1),
            'pickup_time': 'morning',
            'location_latitude': 30.0444,
            'location_longitude': 31.2357,
            'address': 'Test address',
            'status': 'assigned',
            'collector_id': self.collector.id,
        })
        
        # Complete order
        request.write({'status': 'collected'})
        
        # Verify wallet credited
        wallet.invalidate_cache(['current_balance'])
        expected_balance = initial_balance + request.calculated_price
        self.assertEqual(wallet.current_balance, expected_balance)
        
        # Verify transaction created
        transaction = self.Transaction.search([
            ('wallet_id', '=', wallet.id),
            ('transaction_type', '=', 'credit'),
            ('reference', 'ilike', request.name)
        ])
        self.assertTrue(transaction)
        self.assertEqual(transaction.amount, request.calculated_price)
    
    def test_commission_auto_created(self):
        """Test commission auto-created on order completion"""
        
        # Create and complete request
        request = self.Request.create({
            'customer_id': self.customer.id,
            'product_id': self.product.id,
            'quantity': 20.0,
            'unit': 'kg',
            'pickup_date': fields.Date.today() + timedelta(days=1),
            'pickup_time': 'morning',
            'location_latitude': 30.0444,
            'location_longitude': 31.2357,
            'address': 'Test address',
            'status': 'assigned',
            'collector_id': self.collector.id,
        })
        
        # Before completion - no commission
        commission_before = self.Commission.search([('request_id', '=', request.id)])
        self.assertFalse(commission_before)
        
        # Complete order
        request.write({'status': 'collected'})
        
        # After completion - commission created
        commission_after = self.Commission.search([('request_id', '=', request.id)])
        self.assertTrue(commission_after)
        self.assertEqual(commission_after.collector_id.id, self.collector.id)
        self.assertEqual(commission_after.amount, request.calculated_price)

