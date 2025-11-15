# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request

class CycleXController(http.Controller):
    """
    Main controller for CycleX API endpoints.
    This will be expanded in Phase 3 with all API methods.
    """
    
    @http.route('/api/cyclex/health', type='json', auth='public', methods=['GET'], csrf=False)
    def health_check(self):
        """Health check endpoint to verify API is running"""
        return {
            'status': 'ok',
            'message': 'CycleX API is running',
            'version': '1.0.0'
        }

