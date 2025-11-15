# -*- coding: utf-8 -*-

import json
from odoo import http
from odoo.http import request

class CycleXController(http.Controller):
    """
    Main controller for CycleX API endpoints.
    This will be expanded in Phase 3 with all API methods.
    """
    
    @http.route('/api/cyclex/health', type='http', auth='public', methods=['POST'], csrf=False)
    def health_check(self):
        """Health check endpoint to verify API is running"""
        return request.make_response(
            json.dumps({
                'status': 'ok',
                'message': 'CycleX API is running',
                'version': '1.0.0'
            }),
            headers={'Content-Type': 'application/json'},
            status=200
        )

