# -*- coding: utf-8 -*-

from odoo import http

from .api_base import CycleXApiBase


class CycleXController(CycleXApiBase):
    """Main controller for CycleX API endpoints."""

    @http.route('/api/cyclex/health', type='http', auth='public', methods=['GET'], csrf=False)
    def health_check(self, **kwargs):
        """Health check endpoint to verify API is running."""
        return self._success({
            'status': 'ok',
            'message': 'CycleX API is running',
            'version': '1.0.0',
        })
