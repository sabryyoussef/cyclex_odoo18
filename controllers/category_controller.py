# -*- coding: utf-8 -*-

import json
import logging
from odoo import http, _
from odoo.http import request
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class CyclexCategoryController(http.Controller):
    """
    Category API Controller for CycleX Mobile App
    """
    
    @http.route('/api/cyclex/categories', type='http', auth='user', methods=['POST'], csrf=False)
    def get_categories(self, **kwargs):
        """
        Get all active categories
        
        Returns:
        - success: True/False
        - data: List of categories with products count
        """
        try:
            # Get all active categories
            categories = request.env['cyclex.category'].sudo().search([
                ('active', '=', True)
            ], order='sequence, name')
            
            category_list = []
            for category in categories:
                # Count products in category
                product_count = request.env['cyclex.product'].sudo().search_count([
                    ('category_id', '=', category.id),
                    ('active', '=', True)
                ])
                
                category_list.append({
                    'id': category.id,
                    'name': category.name,
                    'description': category.description or '',
                    'icon': category.icon or '',
                    'color': category.color or '#007bff',
                    'sequence': category.sequence,
                    'product_count': product_count,
                    'active': category.active,
                })
            
            return request.make_response(
                json.dumps({
                    'success': True,
                    'data': {
                        'categories': category_list,
                        'total': len(category_list)
                    }
                }),
                headers={'Content-Type': 'application/json'},
                status=200
            )
            
        except Exception as e:
            _logger.error(f"Get categories error: {str(e)}")
            return request.make_response(
                json.dumps({
                    'success': False,
                    'message': _('An error occurred while fetching categories'),
                    'error_code': 'SERVER_ERROR'
                }),
                headers={'Content-Type': 'application/json'},
                status=500
            )
    
    @http.route('/api/cyclex/products', type='http', auth='user', methods=['POST'], csrf=False)
    def get_products(self, **kwargs):
        """
        Get products by category
        
        Expected params:
        - category_id: Category ID (optional, if not provided returns all products)
        - limit: Number of results (default: 50)
        - offset: Pagination offset
        
        Returns:
        - success: True/False
        - data: List of products
        """
        try:
            # Handle both form data and JSON data
            if request.httprequest.content_type == 'application/json':
                data = json.loads(request.httprequest.data.decode('utf-8'))
            else:
                data = request.params
            
            category_id = data.get('category_id')
            limit = int(data.get('limit', 50))
            offset = int(data.get('offset', 0))
            
            # Build domain
            domain = [('active', '=', True)]
            if category_id:
                domain.append(('category_id', '=', int(category_id)))
            
            # Search products
            products = request.env['cyclex.product'].sudo().search(
                domain,
                order='sequence, name',
                limit=limit,
                offset=offset
            )
            
            total_count = request.env['cyclex.product'].sudo().search_count(domain)
            
            # Format response
            product_list = []
            for product in products:
                product_list.append({
                    'id': product.id,
                    'name': product.name,
                    'description': product.description or '',
                    'category_id': product.category_id.id,
                    'category_name': product.category_id.name,
                    'price_per_kg': product.price_per_kg,
                    'unit': product.unit or 'kg',
                    'image': product.image or '',
                    'sequence': product.sequence,
                    'active': product.active,
                })
            
            return request.make_response(
                json.dumps({
                    'success': True,
                    'data': {
                        'products': product_list,
                        'total': total_count,
                        'limit': limit,
                        'offset': offset,
                        'category_id': category_id
                    }
                }),
                headers={'Content-Type': 'application/json'},
                status=200
            )
            
        except Exception as e:
            _logger.error(f"Get products error: {str(e)}")
            return request.make_response(
                json.dumps({
                    'success': False,
                    'message': _('An error occurred while fetching products'),
                    'error_code': 'SERVER_ERROR'
                }),
                headers={'Content-Type': 'application/json'},
                status=500
            )
