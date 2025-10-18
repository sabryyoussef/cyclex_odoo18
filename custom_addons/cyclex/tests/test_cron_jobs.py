# -*- coding: utf-8 -*-

from odoo.tests.common import TransactionCase
from datetime import timedelta
from odoo import fields


class TestCronJobs(TransactionCase):
    """Test scheduled actions (cron jobs)"""
    
    def setUp(self):
        super(TestCronJobs, self).setUp()
        self.Partner = self.env['res.partner']
        self.Product = self.env['cyclex.product']
        self.Request = self.env['cyclex.request']
        self.Wallet = self.env['cyclex.wallet']
        
        # Create test customer
        self.customer = self.Partner.create({
            'name': 'Cron Test Customer',
            'phone': '+201999999996',
            'is_cyclex_user': True,
            'cyclex_user_type': 'customer',
            'phone_verified': True,
        })
        
        # Create test collector
        self.collector = self.Partner.create({
            'name': 'Cron Test Collector',
            'phone': '+201888888886',
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
    
    def test_auto_revert_overdue_orders(self):
        """Test cron job: Auto-revert orders older than 3 days"""
        
        # Create assigned order
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
        self.assertTrue(request.collector_id)
        
        # Simulate 4 days old (manually update write_date)
        old_date = fields.Datetime.now() - timedelta(days=4)
        self.env.cr.execute(
            "UPDATE cyclex_request SET write_date = %s WHERE id = %s",
            (old_date, request.id)
        )
        self.env.cr.commit()
        
        # Run cron job
        self.Request._cron_auto_revert_overdue_orders()
        
        # Verify order reverted
        request.invalidate_cache()
        self.assertEqual(request.status, 'pending')
        self.assertFalse(request.collector_id)
    
    def test_auto_revert_does_not_affect_recent(self):
        """Test cron job doesn't revert recent orders"""
        
        # Create assigned order (recent)
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
        
        # Run cron job
        self.Request._cron_auto_revert_overdue_orders()
        
        # Verify order NOT reverted (still recent)
        request.invalidate_cache()
        self.assertEqual(request.status, 'assigned')
        self.assertTrue(request.collector_id)
    
    def test_auto_revert_only_assigned_orders(self):
        """Test cron job only affects assigned orders"""
        
        # Create pending order (old)
        request_pending = self.Request.create({
            'customer_id': self.customer.id,
            'product_id': self.product.id,
            'quantity': 10.0,
            'unit': 'kg',
            'pickup_date': fields.Date.today() + timedelta(days=1),
            'pickup_time': 'morning',
            'location_latitude': 30.0444,
            'location_longitude': 31.2357,
            'address': 'Test address 1',
            'status': 'pending',
        })
        
        # Create collected order (old)
        request_collected = self.Request.create({
            'customer_id': self.customer.id,
            'product_id': self.product.id,
            'quantity': 10.0,
            'unit': 'kg',
            'pickup_date': fields.Date.today() + timedelta(days=1),
            'pickup_time': 'morning',
            'location_latitude': 30.0444,
            'location_longitude': 31.2357,
            'address': 'Test address 2',
            'status': 'collected',
        })
        
        # Make both old
        old_date = fields.Datetime.now() - timedelta(days=4)
        for req in [request_pending, request_collected]:
            self.env.cr.execute(
                "UPDATE cyclex_request SET write_date = %s WHERE id = %s",
                (old_date, req.id)
            )
        self.env.cr.commit()
        
        # Run cron job
        self.Request._cron_auto_revert_overdue_orders()
        
        # Verify statuses unchanged (only assigned orders revert)
        request_pending.invalidate_cache()
        request_collected.invalidate_cache()
        
        self.assertEqual(request_pending.status, 'pending')
        self.assertEqual(request_collected.status, 'collected')
    
    def test_pending_withdrawals_notification(self):
        """Test cron job: Notify about pending withdrawals"""
        
        wallet = self.customer.wallet_id
        
        # Add balance and request withdrawal
        wallet.add_credit(100.00, 'Test credit', request_id=1)
        wallet.add_debit(50.00, 'Withdrawal 1')
        wallet.add_debit(30.00, 'Withdrawal 2')
        
        # Verify 2 pending withdrawals
        pending_count = self.env['cyclex.wallet.transaction'].search_count([
            ('transaction_type', '=', 'debit'),
            ('withdrawal_status', '=', 'pending')
        ])
        
        self.assertEqual(pending_count, 2)
        
        # Run cron job (should log the count)
        result = self.Wallet._cron_notify_pending_withdrawals()
        
        # Should return True
        self.assertTrue(result)
        
        # Note: Actual notification would be logged, not testable here
    
    def test_cron_jobs_exist(self):
        """Test cron jobs are properly configured"""
        Cron = self.env['ir.cron']
        
        # Check Auto-Revert cron exists
        auto_revert = Cron.search([
            ('name', '=', 'CycleX: Auto-Revert Overdue Orders')
        ])
        self.assertTrue(auto_revert, "Auto-revert cron job should exist")
        self.assertEqual(auto_revert.interval_number, 6)
        self.assertEqual(auto_revert.interval_type, 'hours')
        self.assertTrue(auto_revert.active)
        
        # Check Pending Withdrawals cron exists
        withdrawals = Cron.search([
            ('name', '=', 'CycleX: Process Pending Withdrawals')
        ])
        self.assertTrue(withdrawals, "Pending withdrawals cron job should exist")
        self.assertEqual(withdrawals.interval_number, 1)
        self.assertEqual(withdrawals.interval_type, 'days')
        self.assertTrue(withdrawals.active)

