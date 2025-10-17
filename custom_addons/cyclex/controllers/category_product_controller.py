# -*- coding: utf-8 -*-

import logging
from odoo import http, _
from odoo.http import request

_logger = logging.getLogger(__name__)


class CyclexCategoryProductController(http.Controller):
    """
    Category and Product API Controller for CycleX Mobile App
    """
    
    @http.route('/api/cyclex/categories', type='json', auth='public', methods=['GET'], csrf=False)
    def get_categories(self, **kwargs):
        """
        Get list of categories (hierarchical)
        
        Optional params:
        - parent_id: Filter by parent category
        - language: 'en' or 'ar'
        
        Returns:
        - success: True/False
        - data: List of categories
        """
        try:
            parent_id = kwargs.get('parent_id', False)
            language = kwargs.get('language', 'en')
            
            # Set context for translation
            context = dict(request.env.context)
            context['lang'] = 'ar_001' if language == 'ar' else 'en_US'
            
            # Build domain
            domain = [('active', '=', True)]
            if parent_id:
                domain.append(('parent_id', '=', parent_id))
            else:
                # Get root categories (no parent)
                domain.append(('parent_id', '=', False))
            
            # Search categories
            categories = request.env['cyclex.category'].with_context(context).sudo().search(domain, order='name')
            
            # Format response
            category_list = []
            for cat in categories:
                category_list.append({
                    'id': cat.id,
                    'name': cat.name,
                    'description': cat.description or '',
                    'parent_id': cat.parent_id.id if cat.parent_id else None,
                    'parent_name': cat.parent_id.name if cat.parent_id else None,
                    'has_children': len(cat.child_ids) > 0,
                    'product_count': cat.product_count,
                    'image': cat.image.decode('utf-8') if cat.image else None,  # Base64
                })
            
            return {
                'success': True,
                'data': {
                    'categories': category_list,
                    'total': len(category_list)
                }
            }
            
        except Exception as e:
            _logger.error(f"Get categories error: {str(e)}")
            return {
                'success': False,
                'message': _('An error occurred while fetching categories'),
                'error_code': 'SERVER_ERROR'
            }
    
    @http.route('/api/cyclex/products', type='json', auth='public', methods=['GET'], csrf=False)
    def get_products(self, **kwargs):
        """
        Get list of products
        
        Optional params:
        - category_id: Filter by category
        - search: Search by name
        - language: 'en' or 'ar'
        
        Returns:
        - success: True/False
        - data: List of products
        """
        try:
            category_id = kwargs.get('category_id')
            search_term = kwargs.get('search', '')
            language = kwargs.get('language', 'en')
            
            # Set context for translation
            context = dict(request.env.context)
            context['lang'] = 'ar_001' if language == 'ar' else 'en_US'
            
            # Build domain
            domain = [('active', '=', True)]
            
            if category_id:
                domain.append(('category_id', '=', category_id))
            
            if search_term:
                domain.append(('name', 'ilike', search_term))
            
            # Search products
            products = request.env['cyclex.product'].with_context(context).sudo().search(domain, order='category_id, name')
            
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
                    'currency': product.currency_id.name,
                    'currency_symbol': product.currency_id.symbol,
                    'image': product.image.decode('utf-8') if product.image else None,  # Base64
                })
            
            return {
                'success': True,
                'data': {
                    'products': product_list,
                    'total': len(product_list)
                }
            }
            
        except Exception as e:
            _logger.error(f"Get products error: {str(e)}")
            return {
                'success': False,
                'message': _('An error occurred while fetching products'),
                'error_code': 'SERVER_ERROR'
            }
    
    @http.route('/api/cyclex/product/<int:product_id>', type='json', auth='public', methods=['GET'], csrf=False)
    def get_product_details(self, product_id, **kwargs):
        """
        Get product details by ID
        
        Returns:
        - success: True/False
        - data: Product details
        """
        try:
            language = kwargs.get('language', 'en')
            
            # Set context for translation
            context = dict(request.env.context)
            context['lang'] = 'ar_001' if language == 'ar' else 'en_US'
            
            product = request.env['cyclex.product'].with_context(context).sudo().browse(product_id)
            
            if not product.exists() or not product.active:
                return {
                    'success': False,
                    'message': _('Product not found'),
                    'error_code': 'NOT_FOUND'
                }
            
            return {
                'success': True,
                'data': {
                    'id': product.id,
                    'name': product.name,
                    'description': product.description or '',
                    'category_id': product.category_id.id,
                    'category_name': product.category_id.name,
                    'price_per_kg': product.price_per_kg,
                    'currency': product.currency_id.name,
                    'currency_symbol': product.currency_id.symbol,
                    'image': product.image.decode('utf-8') if product.image else None,
                    'request_count': product.request_count,
                }
            }
            
        except Exception as e:
            _logger.error(f"Get product details error: {str(e)}")
            return {
                'success': False,
                'message': _('An error occurred while fetching product details'),
                'error_code': 'SERVER_ERROR'
            }

