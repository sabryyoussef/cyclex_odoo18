# -*- coding: utf-8 -*-

import json
import logging
from odoo import http, _
from odoo.http import request
from .auth_controller import CyclexAuthController
from .category_product_controller import CyclexCategoryProductController
from .request_controller import CyclexRequestController
from .wallet_controller import CyclexWalletController
from .collector_controller import CyclexCollectorController

_logger = logging.getLogger(__name__)


class PostmanCompatibilityController(http.Controller):
    """
    Compatibility layer to match Postman collection paths and methods.
    This allows Odoo to accept requests exactly as the mobile app expects.
    """
    
    def _json_response(self, data, status=200):
        """Helper to return JSON response"""
        return request.make_response(
            json.dumps(data),
            headers=[('Content-Type', 'application/json')],
            status=status
        )
    
    def _extract_params(self, kwargs):
        """Extract params from GET query string or POST JSON body"""
        if request.httprequest.method == 'POST':
            try:
                body = json.loads(request.httprequest.data.decode('utf-8'))
                return body
            except:
                return kwargs
        else:
            return kwargs
    
    def _check_auth(self):
        """Check if user is authenticated"""
        # For HTTP routes with auth='none', we need to check session manually
        # Try to get user from session
        try:
            # Set up environment with session user
            if request.session and request.session.uid:
                request.env = request.env(user=request.session.uid)
                return request.env.user
            return None
        except:
            return None
    
    # ==================== AUTHENTICATION ====================
    
    @http.route('/api/cyclex/auth/login', type='http', auth='public', methods=['GET', 'POST'], csrf=False)
    def auth_login(self, **kwargs):
        """POST /auth/login - Login endpoint"""
        try:
            params = self._extract_params(kwargs)
            # Call existing login endpoint
            auth_ctrl = CyclexAuthController()
            result = auth_ctrl.login(**params)
            return self._json_response(result)
        except Exception as e:
            _logger.error(f"Auth login error: {str(e)}")
            return self._json_response({
                'success': False,
                'message': str(e),
                'error_code': 'SERVER_ERROR'
            }, status=500)
    
    @http.route('/api/cyclex/auth/register', type='http', auth='public', methods=['POST'], csrf=False)
    def auth_register(self, **kwargs):
        """POST /auth/register - Sign up endpoint"""
        try:
            params = self._extract_params(kwargs)
            auth_ctrl = CyclexAuthController()
            result = auth_ctrl.register(**params)
            return self._json_response(result)
        except Exception as e:
            _logger.error(f"Auth register error: {str(e)}")
            return self._json_response({
                'success': False,
                'message': str(e),
                'error_code': 'SERVER_ERROR'
            }, status=500)
    
    @http.route('/api/cyclex/auth/verify-otp', type='http', auth='public', methods=['POST'], csrf=False)
    def auth_verify_otp(self, **kwargs):
        """POST /auth/verify-otp - Verify OTP endpoint"""
        try:
            params = self._extract_params(kwargs)
            # Map 'otp' to 'verification_code' if needed
            if 'otp' in params and 'verification_code' not in params:
                params['verification_code'] = params.pop('otp')
            
            auth_ctrl = CyclexAuthController()
            result = auth_ctrl.verify(**params)
            return self._json_response(result)
        except Exception as e:
            _logger.error(f"Auth verify OTP error: {str(e)}")
            return self._json_response({
                'success': False,
                'message': str(e),
                'error_code': 'SERVER_ERROR'
            }, status=500)
    
    @http.route('/api/cyclex/auth/resend-otp', type='http', auth='public', methods=['POST'], csrf=False)
    def auth_resend_otp(self, **kwargs):
        """POST /auth/resend-otp - Resend OTP endpoint"""
        try:
            params = self._extract_params(kwargs)
            auth_ctrl = CyclexAuthController()
            result = auth_ctrl.resend_code(**params)
            return self._json_response(result)
        except Exception as e:
            _logger.error(f"Auth resend OTP error: {str(e)}")
            return self._json_response({
                'success': False,
                'message': str(e),
                'error_code': 'SERVER_ERROR'
            }, status=500)
    
    # ==================== CATALOG ====================
    
    @http.route('/api/cyclex/catalog/categories', type='http', auth='public', methods=['GET', 'POST'], csrf=False)
    def catalog_categories(self, **kwargs):
        """GET /catalog/categories - Get categories list"""
        try:
            # Extract params from query string (GET) or body (POST)
            if request.httprequest.method == 'GET':
                params = {
                    'language': kwargs.get('language', 'en'),
                    'parent_id': kwargs.get('parent_id', False)
                }
            else:
                params = self._extract_params(kwargs)
            
            # Call existing categories endpoint
            cat_ctrl = CyclexCategoryProductController()
            result = cat_ctrl.get_categories(**params)
            return self._json_response(result)
        except Exception as e:
            _logger.error(f"Catalog categories error: {str(e)}")
            return self._json_response({
                'success': False,
                'message': str(e),
                'error_code': 'SERVER_ERROR'
            }, status=500)
    
    @http.route('/api/cyclex/catalog/categories/<string:category_name>/items', type='http', auth='public', methods=['GET', 'POST'], csrf=False)
    def catalog_category_items(self, category_name, **kwargs):
        """GET /catalog/categories/{name}/items - Get products by category name"""
        try:
            # Map category name to ID
            category_map = {
                'PLASTIC': 8,  # Update with actual IDs
                'PAPER': 9,
                'METAL': 10,
                'GLASS': 11,
                'ELECTRONICS': 12
            }
            
            category_id = category_map.get(category_name.upper())
            if not category_id:
                # Try to find by name
                category = request.env['cyclex.category'].sudo().search([
                    ('name', 'ilike', category_name)
                ], limit=1)
                if category:
                    category_id = category.id
                else:
                    return self._json_response({
                        'success': False,
                        'message': _('Category not found'),
                        'error_code': 'NOT_FOUND'
                    }, status=404)
            
            # Extract params
            params = {'category_id': category_id}
            if request.httprequest.method == 'GET':
                params['language'] = kwargs.get('language', 'en')
            else:
                try:
                    body = json.loads(request.httprequest.data.decode('utf-8'))
                    params.update(body)
                except:
                    params.update(kwargs)
            
            # Call existing products endpoint
            cat_ctrl = CyclexCategoryProductController()
            result = cat_ctrl.get_products(**params)
            return self._json_response(result)
        except Exception as e:
            _logger.error(f"Catalog category items error: {str(e)}")
            return self._json_response({
                'success': False,
                'message': str(e),
                'error_code': 'SERVER_ERROR'
            }, status=500)
    
    # ==================== ORDERS/REQUESTS ====================
    
    @http.route('/api/cyclex/orders', type='http', auth='none', methods=['GET', 'POST'], csrf=False)
    def orders_list(self, **kwargs):
        """GET /orders - Get orders list (maps to request/list)"""
        try:
            # Check authentication manually
            user = self._check_auth()
            if not user or user._is_public():
                return self._json_response({
                    'success': False,
                    'message': _('Authentication required'),
                    'error_code': 'AUTH_REQUIRED'
                }, status=401)
            
            params = {}
            if request.httprequest.method == 'GET':
                # GET request - extract from query string
                status = kwargs.get('status', 'all')
                # Map 'active' to 'pending'
                if status == 'active':
                    params['status'] = 'pending'
                elif status == 'all':
                    params = {}  # No filter
                else:
                    params['status'] = status
            else:
                # POST request - extract from body
                try:
                    body = json.loads(request.httprequest.data.decode('utf-8'))
                    params = body
                except:
                    params = kwargs
            
            # Call existing request list endpoint
            req_ctrl = CyclexRequestController()
            result = req_ctrl.list_requests(**params)
            return self._json_response(result)
        except Exception as e:
            _logger.error(f"Orders list error: {str(e)}")
            return self._json_response({
                'success': False,
                'message': str(e),
                'error_code': 'SERVER_ERROR'
            }, status=500)
    
    @http.route('/api/cyclex/orders/<int:order_id>', type='http', auth='none', methods=['GET', 'POST'], csrf=False)
    def orders_details(self, order_id, **kwargs):
        """GET /orders/{id} - Get order details"""
        try:
            # Check authentication manually
            user = self._check_auth()
            if not user or user._is_public():
                return self._json_response({
                    'success': False,
                    'message': _('Authentication required'),
                    'error_code': 'AUTH_REQUIRED'
                }, status=401)
            
            # Call existing request details endpoint
            req_ctrl = CyclexRequestController()
            result = req_ctrl.get_request_details(order_id, **kwargs)
            return self._json_response(result)
        except Exception as e:
            _logger.error(f"Orders details error: {str(e)}")
            return self._json_response({
                'success': False,
                'message': str(e),
                'error_code': 'SERVER_ERROR'
            }, status=500)
    
    @http.route('/api/cyclex/orders/<int:order_id>/rate', type='http', auth='none', methods=['POST'], csrf=False)
    def orders_rate(self, order_id, **kwargs):
        """POST /orders/{id}/rate - Rate an order"""
        try:
            # Check authentication
            user = self._check_auth()
            if not user or user._is_public():
                return self._json_response({
                    'success': False,
                    'message': _('Authentication required'),
                    'error_code': 'AUTH_REQUIRED'
                }, status=401)
            
            if request.httprequest.method == 'POST':
                try:
                    body = json.loads(request.httprequest.data.decode('utf-8'))
                    params = body
                except:
                    params = kwargs
            else:
                params = kwargs
            
            # Call existing rating endpoint
            rating_ctrl = CyclexRatingController()
            result = rating_ctrl.rate_request(order_id, **params)
            return self._json_response(result)
        except Exception as e:
            _logger.error(f"Orders rate error: {str(e)}")
            return self._json_response({
                'success': False,
                'message': str(e),
                'error_code': 'SERVER_ERROR'
            }, status=500)
    
    # ==================== USER/PROFILE ====================
    
    @http.route('/api/cyclex/user/profile', type='http', auth='none', methods=['GET', 'PUT', 'POST'], csrf=False)
    def user_profile(self, **kwargs):
        """GET /user/profile - Get profile, PUT /user/profile - Update profile"""
        try:
            # Check authentication
            user = self._check_auth()
            if not user or user._is_public():
                return self._json_response({
                    'success': False,
                    'message': _('Authentication required'),
                    'error_code': 'AUTH_REQUIRED'
                }, status=401)
            
            if request.httprequest.method in ['PUT', 'POST']:
                # Update profile
                if request.httprequest.method == 'POST':
                    try:
                        body = json.loads(request.httprequest.data.decode('utf-8'))
                        params = body
                    except:
                        params = kwargs
                else:
                    params = kwargs
                
                auth_ctrl = CyclexAuthController()
                result = auth_ctrl.update_profile(**params)
                return self._json_response(result)
            else:
                # GET profile
                auth_ctrl = CyclexAuthController()
                result = auth_ctrl.get_profile(**kwargs)
                return self._json_response(result)
        except Exception as e:
            _logger.error(f"User profile error: {str(e)}")
            return self._json_response({
                'success': False,
                'message': str(e),
                'error_code': 'SERVER_ERROR'
            }, status=500)
    
    # ==================== WALLET ====================
    
    @http.route('/api/cyclex/wallet', type='http', auth='none', methods=['GET', 'POST'], csrf=False)
    def wallet_balance(self, **kwargs):
        """GET /wallet - Get wallet balance"""
        try:
            # Check authentication
            user = self._check_auth()
            if not user or user._is_public():
                return self._json_response({
                    'success': False,
                    'message': _('Authentication required'),
                    'error_code': 'AUTH_REQUIRED'
                }, status=401)
            
            wallet_ctrl = CyclexWalletController()
            result = wallet_ctrl.get_balance(**kwargs)
            return self._json_response(result)
        except Exception as e:
            _logger.error(f"Wallet balance error: {str(e)}")
            return self._json_response({
                'success': False,
                'message': str(e),
                'error_code': 'SERVER_ERROR'
            }, status=500)
    
    @http.route('/api/cyclex/wallet/transactions', type='http', auth='none', methods=['GET', 'POST'], csrf=False)
    def wallet_transactions(self, **kwargs):
        """GET /wallet/transactions - Get wallet transactions"""
        try:
            # Check authentication
            user = self._check_auth()
            if not user or user._is_public():
                return self._json_response({
                    'success': False,
                    'message': _('Authentication required'),
                    'error_code': 'AUTH_REQUIRED'
                }, status=401)
            
            params = {}
            if request.httprequest.method == 'GET':
                params = kwargs  # Query params
            else:
                try:
                    body = json.loads(request.httprequest.data.decode('utf-8'))
                    params = body
                except:
                    params = kwargs
            
            wallet_ctrl = CyclexWalletController()
            result = wallet_ctrl.get_transactions(**params)
            return self._json_response(result)
        except Exception as e:
            _logger.error(f"Wallet transactions error: {str(e)}")
            return self._json_response({
                'success': False,
                'message': str(e),
                'error_code': 'SERVER_ERROR'
            }, status=500)
    
    # ==================== COLLECTOR ====================
    
    @http.route('/api/cyclex/collector/profile', type='http', auth='none', methods=['GET', 'POST'], csrf=False)
    def collector_profile(self, **kwargs):
        """GET /collector/profile - Get collector profile (same as user profile)"""
        try:
            # Check authentication
            user = self._check_auth()
            if not user or user._is_public():
                return self._json_response({
                    'success': False,
                    'message': _('Authentication required'),
                    'error_code': 'AUTH_REQUIRED'
                }, status=401)
            
            auth_ctrl = CyclexAuthController()
            result = auth_ctrl.get_profile(**kwargs)
            return self._json_response(result)
        except Exception as e:
            _logger.error(f"Collector profile error: {str(e)}")
            return self._json_response({
                'success': False,
                'message': str(e),
                'error_code': 'SERVER_ERROR'
            }, status=500)
    
    @http.route('/api/cyclex/collector/orders', type='http', auth='none', methods=['GET', 'POST'], csrf=False)
    def collector_orders(self, **kwargs):
        """GET /collector/orders - Get collector orders (maps to available-orders)"""
        try:
            # Check authentication
            user = self._check_auth()
            if not user or user._is_public():
                return self._json_response({
                    'success': False,
                    'message': _('Authentication required'),
                    'error_code': 'AUTH_REQUIRED'
                }, status=401)
            
            params = {}
            if request.httprequest.method == 'GET':
                # Map status=assigned to available orders
                status = kwargs.get('status')
                if status == 'assigned':
                    # Get assigned orders for this collector
                    # This would need a new endpoint or modify existing
                    params = kwargs
                else:
                    # Get available orders
                    pass
            else:
                try:
                    body = json.loads(request.httprequest.data.decode('utf-8'))
                    params = body
                except:
                    params = kwargs
            
            collector_ctrl = CyclexCollectorController()
            result = collector_ctrl.get_available_orders(**params)
            return self._json_response(result)
        except Exception as e:
            _logger.error(f"Collector orders error: {str(e)}")
            return self._json_response({
                'success': False,
                'message': str(e),
                'error_code': 'SERVER_ERROR'
            }, status=500)
    
    @http.route('/api/cyclex/collector/orders/<int:order_id>/accept', type='http', auth='none', methods=['POST'], csrf=False)
    def collector_accept_order(self, order_id, **kwargs):
        """POST /collector/orders/{id}/accept"""
        try:
            # Check authentication
            user = self._check_auth()
            if not user or user._is_public():
                return self._json_response({
                    'success': False,
                    'message': _('Authentication required'),
                    'error_code': 'AUTH_REQUIRED'
                }, status=401)
            
            collector_ctrl = CyclexCollectorController()
            result = collector_ctrl.accept_order(order_id, **kwargs)
            return self._json_response(result)
        except Exception as e:
            _logger.error(f"Collector accept order error: {str(e)}")
            return self._json_response({
                'success': False,
                'message': str(e),
                'error_code': 'SERVER_ERROR'
            }, status=500)
    
    @http.route('/api/cyclex/collector/orders/<int:order_id>/reject', type='http', auth='none', methods=['POST'], csrf=False)
    def collector_reject_order(self, order_id, **kwargs):
        """POST /collector/orders/{id}/reject"""
        try:
            # Check authentication
            user = self._check_auth()
            if not user or user._is_public():
                return self._json_response({
                    'success': False,
                    'message': _('Authentication required'),
                    'error_code': 'AUTH_REQUIRED'
                }, status=401)
            
            if request.httprequest.method == 'POST':
                try:
                    body = json.loads(request.httprequest.data.decode('utf-8'))
                    params = body
                except:
                    params = kwargs
            else:
                params = kwargs
            
            collector_ctrl = CyclexCollectorController()
            result = collector_ctrl.reject_order(order_id, **params)
            return self._json_response(result)
        except Exception as e:
            _logger.error(f"Collector reject order error: {str(e)}")
            return self._json_response({
                'success': False,
                'message': str(e),
                'error_code': 'SERVER_ERROR'
            }, status=500)
    
    @http.route('/api/cyclex/collector/orders/<int:order_id>/complete', type='http', auth='none', methods=['POST'], csrf=False)
    def collector_complete_order(self, order_id, **kwargs):
        """POST /collector/orders/{id}/complete"""
        try:
            # Check authentication
            user = self._check_auth()
            if not user or user._is_public():
                return self._json_response({
                    'success': False,
                    'message': _('Authentication required'),
                    'error_code': 'AUTH_REQUIRED'
                }, status=401)
            
            if request.httprequest.method == 'POST':
                try:
                    body = json.loads(request.httprequest.data.decode('utf-8'))
                    params = body
                except:
                    params = kwargs
            else:
                params = kwargs
            
            collector_ctrl = CyclexCollectorController()
            result = collector_ctrl.complete_order(order_id, **params)
            return self._json_response(result)
        except Exception as e:
            _logger.error(f"Collector complete order error: {str(e)}")
            return self._json_response({
                'success': False,
                'message': str(e),
                'error_code': 'SERVER_ERROR'
            }, status=500)

