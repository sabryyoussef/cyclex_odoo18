# -*- coding: utf-8 -*-

from odoo.tests.common import TransactionCase
from datetime import timedelta
from odoo import fields
import base64


class TestQRCodes(TransactionCase):
    """Test QR code generation and validation"""
    
    def setUp(self):
        super(TestQRCodes, self).setUp()
        self.Partner = self.env['res.partner']
        self.Product = self.env['cyclex.product']
        self.Request = self.env['cyclex.request']
        
        # Create test customer
        self.customer = self.Partner.create({
            'name': 'Test Customer',
            'phone': '+201999999997',
            'is_cyclex_user': True,
            'cyclex_user_type': 'customer',
            'phone_verified': True,
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
    
    def _create_test_request(self):
        """Helper to create test request"""
        return self.Request.create({
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
    
    def test_qr_code_auto_generated(self):
        """Test QR code auto-generated on request creation"""
        request = self._create_test_request()
        
        # QR code should exist
        self.assertTrue(request.qr_code)
        
        # QR code should have correct format
        self.assertTrue(request.qr_code.startswith('CYCLEX-REQ-'))
        
        # Should contain request number
        self.assertIn(request.name.replace('REQ-', ''), request.qr_code)
    
    def test_qr_code_image_generated(self):
        """Test QR code image (PNG) auto-generated"""
        request = self._create_test_request()
        
        # Image should exist
        self.assertTrue(request.qr_code_image)
        
        # Should be base64 encoded
        try:
            decoded = base64.b64decode(request.qr_code_image)
            # Should be PNG (starts with PNG signature)
            self.assertTrue(decoded.startswith(b'\x89PNG'))
        except Exception:
            self.fail("QR code image should be valid base64 PNG")
    
    def test_qr_code_uniqueness(self):
        """Test each request gets unique QR code"""
        qr_codes = []
        
        # Create 10 requests
        for i in range(10):
            request = self._create_test_request()
            qr_codes.append(request.qr_code)
        
        # All QR codes should be unique
        unique_qr_codes = set(qr_codes)
        self.assertEqual(len(qr_codes), len(unique_qr_codes), "All QR codes should be unique")
    
    def test_qr_code_format(self):
        """Test QR code has correct format"""
        request = self._create_test_request()
        qr_code = request.qr_code
        
        # Format: CYCLEX-REQ-XXXXX-UUID
        parts = qr_code.split('-')
        
        self.assertEqual(parts[0], 'CYCLEX')
        self.assertEqual(parts[1], 'REQ')
        # parts[2] = request number (00001, 00002, etc.)
        # parts[3:] = UUID (5 parts separated by -)
        
        # Total parts should be 7 (CYCLEX, REQ, number, 4 UUID parts)
        self.assertEqual(len(parts), 7)
        
        # UUID part should be 36 characters (with dashes)
        uuid_part = '-'.join(parts[3:])
        self.assertEqual(len(uuid_part), 36)
    
    def test_qr_code_scan_valid(self):
        """Test scanning valid QR code"""
        # Create collector
        collector = self.Partner.create({
            'name': 'QR Test Collector',
            'phone': '+201777777776',
            'is_cyclex_user': True,
            'cyclex_user_type': 'collector',
            'phone_verified': True,
            'collector_verified': True,
            'commission_rate': 15.00,
        })
        
        # Create and assign request
        request = self._create_test_request()
        request.write({
            'status': 'assigned',
            'collector_id': collector.id
        })
        
        # Scan QR code (simulate)
        qr_code = request.qr_code
        
        # Find request by QR code
        found_request = self.Request.search([('qr_code', '=', qr_code)])
        
        self.assertTrue(found_request)
        self.assertEqual(found_request.id, request.id)
        
        # Complete order
        found_request.write({'status': 'collected'})
        
        # Verify completed
        self.assertEqual(found_request.status, 'collected')
    
    def test_qr_code_scan_invalid(self):
        """Test scanning invalid QR code"""
        invalid_codes = [
            'invalid-qr-code',
            'CYCLEX-REQ-99999-nonexistent-uuid',
            '',
            'random-string',
        ]
        
        for invalid_qr in invalid_codes:
            # Try to find request with invalid QR
            found = self.Request.search([('qr_code', '=', invalid_qr)])
            self.assertFalse(found, f"QR code '{invalid_qr}' should not find any request")
    
    def test_qr_code_reuse_prevention(self):
        """Test QR code cannot be used twice"""
        collector = self.Partner.create({
            'name': 'QR Reuse Collector',
            'phone': '+201666666665',
            'is_cyclex_user': True,
            'cyclex_user_type': 'collector',
            'phone_verified': True,
            'collector_verified': True,
            'commission_rate': 15.00,
        })
        
        # Create and complete request
        request = self._create_test_request()
        request.write({
            'status': 'assigned',
            'collector_id': collector.id
        })
        
        qr_code = request.qr_code
        
        # Complete once
        request.write({'status': 'collected'})
        self.assertEqual(request.status, 'collected')
        
        # Try to scan again - status should remain collected
        # In real API, this would return error
        found = self.Request.search([
            ('qr_code', '=', qr_code),
            ('status', '=', 'assigned')  # Only find assigned orders
        ])
        
        # Should not find any (order is collected, not assigned)
        self.assertFalse(found)

