# -*- coding: utf-8 -*-

import base64
import logging
from odoo import http, _, fields
from odoo.http import request
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class CyclexRequestController(http.Controller):
    """
    Request/Order API Controller for CycleX Mobile App
    """
    
    @http.route('/api/cyclex/request/create', type='json', auth='user', methods=['POST'], csrf=False)
    def create_request(self, **kwargs):
        """
        Create a new recycling request
        
        Expected params:
        - category_id: Category ID
        - product_id: Product ID
        - quantity: Quantity of items
        - weight: Weight in kg
        - pickup_date: Preferred pickup date (YYYY-MM-DD)
        - photo_1: (Optional) Base64 encoded photo
        - photo_2: (Optional) Base64 encoded photo
        - gps_latitude: (Optional) GPS latitude
        - gps_longitude: (Optional) GPS longitude
        
        Returns:
        - success: True/False
        - message: Status message
        - data: Request details including QR code
        """
        try:
            partner = request.env.user.partner_id
            
            # Validate user type
            if partner.cyclex_user_type != 'customer':
                return {
                    'success': False,
                    'message': _('Only customers can create requests'),
                    'error_code': 'INVALID_USER_TYPE'
                }
            
            # Get parameters
            category_id = kwargs.get('category_id')
            product_id = kwargs.get('product_id')
            quantity = kwargs.get('quantity')
            weight = kwargs.get('weight')
            pickup_date = kwargs.get('pickup_date')
            
            # Validation
            if not all([category_id, product_id, quantity, weight, pickup_date]):
                return {
                    'success': False,
                    'message': _('All fields are required'),
                    'error_code': 'MISSING_PARAMS'
                }
            
            # Update GPS if provided
            if 'gps_latitude' in kwargs and 'gps_longitude' in kwargs:
                partner.sudo().update_gps_location(kwargs['gps_latitude'], kwargs['gps_longitude'])
            
            # Prepare request values
            request_vals = {
                'customer_id': partner.id,
                'category_id': category_id,
                'product_id': product_id,
                'quantity': quantity,
                'weight': weight,
                'pickup_date': pickup_date,
                'status': 'pending',
            }
            
            # Add photos if provided (with size validation)
            if 'photo_1' in kwargs and kwargs['photo_1']:
                photo_validation = self._validate_image_size(kwargs['photo_1'])
                if not photo_validation['valid']:
                    return {
                        'success': False,
                        'message': photo_validation['message'],
                        'error_code': 'IMAGE_TOO_LARGE'
                    }
                request_vals['photo_1'] = kwargs['photo_1']  # Base64
            
            if 'photo_2' in kwargs and kwargs['photo_2']:
                photo_validation = self._validate_image_size(kwargs['photo_2'])
                if not photo_validation['valid']:
                    return {
                        'success': False,
                        'message': photo_validation['message'],
                        'error_code': 'IMAGE_TOO_LARGE'
                    }
                request_vals['photo_2'] = kwargs['photo_2']  # Base64
            
            # Create request (QR code is auto-generated in create method)
            new_request = request.env['cyclex.request'].sudo().create(request_vals)
            
            return {
                'success': True,
                'message': _('Request created successfully'),
                'data': {
                    'request_id': new_request.id,
                    'request_number': new_request.name,
                    'status': new_request.status,
                    'calculated_price': new_request.calculated_price,
                    'currency_symbol': new_request.currency_id.symbol,
                    'qr_code': new_request.qr_code,
                    'qr_code_image': new_request.qr_code_image.decode('utf-8') if new_request.qr_code_image else None,
                    'pickup_date': str(new_request.pickup_date),
                    'product_name': new_request.product_id.name,
                    'category_name': new_request.category_id.name,
                }
            }
            
        except ValidationError as e:
            return {
                'success': False,
                'message': str(e),
                'error_code': 'VALIDATION_ERROR'
            }
        except Exception as e:
            _logger.error(f"Create request error: {str(e)}")
            return {
                'success': False,
                'message': _('An error occurred while creating request'),
                'error_code': 'SERVER_ERROR'
            }
    
    @http.route('/api/cyclex/request/list', type='json', auth='user', methods=['GET'], csrf=False)
    def list_requests(self, **kwargs):
        """
        Get user's request history
        
        Optional params:
        - status: Filter by status
        - limit: Number of results (default: 20)
        - offset: Pagination offset (default: 0)
        
        Returns:
        - success: True/False
        - data: List of requests
        """
        try:
            partner = request.env.user.partner_id
            
            status_filter = kwargs.get('status')
            limit = int(kwargs.get('limit', 20))
            offset = int(kwargs.get('offset', 0))
            
            # Build domain based on user type
            if partner.cyclex_user_type == 'customer':
                domain = [('customer_id', '=', partner.id)]
            elif partner.cyclex_user_type == 'collector':
                domain = [('collector_id', '=', partner.id)]
            else:
                return {
                    'success': False,
                    'message': _('Invalid user type'),
                    'error_code': 'INVALID_USER_TYPE'
                }
            
            # Add status filter if provided
            if status_filter:
                domain.append(('status', '=', status_filter))
            
            # Search requests
            requests = request.env['cyclex.request'].sudo().search(
                domain, 
                order='create_date desc',
                limit=limit,
                offset=offset
            )
            
            # Get total count
            total_count = request.env['cyclex.request'].sudo().search_count(domain)
            
            # Format response
            request_list = []
            for req in requests:
                request_list.append({
                    'id': req.id,
                    'request_number': req.name,
                    'status': req.status,
                    'product_name': req.product_id.name,
                    'category_name': req.category_id.name,
                    'quantity': req.quantity,
                    'weight': req.weight,
                    'calculated_price': req.calculated_price,
                    'currency_symbol': req.currency_id.symbol,
                    'pickup_date': str(req.pickup_date),
                    'create_date': str(req.create_date),
                    'collector_name': req.collector_id.name if req.collector_id else None,
                    'rating': req.rating if req.rating else None,
                })
            
            return {
                'success': True,
                'data': {
                    'requests': request_list,
                    'total': total_count,
                    'limit': limit,
                    'offset': offset
                }
            }
            
        except Exception as e:
            _logger.error(f"List requests error: {str(e)}")
            return {
                'success': False,
                'message': _('An error occurred while fetching requests'),
                'error_code': 'SERVER_ERROR'
            }
    
    @http.route('/api/cyclex/request/details/<int:request_id>', type='json', auth='user', methods=['GET'], csrf=False)
    def get_request_details(self, request_id, **kwargs):
        """
        Get request details by ID
        
        Returns:
        - success: True/False
        - data: Full request details including QR code
        """
        try:
            partner = request.env.user.partner_id
            
            req = request.env['cyclex.request'].sudo().browse(request_id)
            
            if not req.exists():
                return {
                    'success': False,
                    'message': _('Request not found'),
                    'error_code': 'NOT_FOUND'
                }
            
            # Verify ownership
            if partner.cyclex_user_type == 'customer' and req.customer_id.id != partner.id:
                return {
                    'success': False,
                    'message': _('Access denied'),
                    'error_code': 'ACCESS_DENIED'
                }
            
            if partner.cyclex_user_type == 'collector' and req.collector_id.id != partner.id:
                return {
                    'success': False,
                    'message': _('Access denied'),
                    'error_code': 'ACCESS_DENIED'
                }
            
            return {
                'success': True,
                'data': {
                    'id': req.id,
                    'request_number': req.name,
                    'status': req.status,
                    'customer_name': req.customer_id.name,
                    'customer_phone': req.customer_id.phone,
                    'collector_name': req.collector_id.name if req.collector_id else None,
                    'collector_phone': req.collector_id.phone if req.collector_id else None,
                    'category_id': req.category_id.id,
                    'category_name': req.category_id.name,
                    'product_id': req.product_id.id,
                    'product_name': req.product_id.name,
                    'quantity': req.quantity,
                    'weight': req.weight,
                    'calculated_price': req.calculated_price,
                    'currency_symbol': req.currency_id.symbol,
                    'pickup_date': str(req.pickup_date),
                    'create_date': str(req.create_date),
                    'completion_date': str(req.completion_date) if req.completion_date else None,
                    'qr_code': req.qr_code,
                    'qr_code_image': req.qr_code_image.decode('utf-8') if req.qr_code_image else None,
                    'rating': req.rating if req.rating else None,
                    'comments': req.comments or '',
                    'photo_1': req.photo_1.decode('utf-8') if req.photo_1 else None,
                    'photo_2': req.photo_2.decode('utf-8') if req.photo_2 else None,
                    'customer_address': {
                        'street': req.customer_id.street or '',
                        'city': req.customer_id.city or '',
                        'latitude': req.customer_id.gps_latitude,
                        'longitude': req.customer_id.gps_longitude,
                    }
                }
            }
            
        except Exception as e:
            _logger.error(f"Get request details error: {str(e)}")
            return {
                'success': False,
                'message': _('An error occurred while fetching request details'),
                'error_code': 'SERVER_ERROR'
            }
    
    @http.route('/api/cyclex/request/cancel/<int:request_id>', type='json', auth='user', methods=['POST'], csrf=False)
    def cancel_request(self, request_id, **kwargs):
        """
        Cancel a request
        
        Returns:
        - success: True/False
        - message: Status message
        """
        try:
            partner = request.env.user.partner_id
            
            req = request.env['cyclex.request'].sudo().browse(request_id)
            
            if not req.exists():
                return {
                    'success': False,
                    'message': _('Request not found'),
                    'error_code': 'NOT_FOUND'
                }
            
            # Verify ownership (only customer can cancel)
            if req.customer_id.id != partner.id:
                return {
                    'success': False,
                    'message': _('Only the customer can cancel this request'),
                    'error_code': 'ACCESS_DENIED'
                }
            
            # Cancel request
            req.action_cancel()
            
            return {
                'success': True,
                'message': _('Request cancelled successfully'),
                'data': {
                    'request_id': req.id,
                    'status': req.status
                }
            }
            
        except ValidationError as e:
            return {
                'success': False,
                'message': str(e),
                'error_code': 'VALIDATION_ERROR'
            }
        except Exception as e:
            _logger.error(f"Cancel request error: {str(e)}")
            return {
                'success': False,
                'message': _('An error occurred while cancelling request'),
                'error_code': 'SERVER_ERROR'
            }
    
    # ==========================================
    # Helper Methods
    # ==========================================
    
    def _validate_image_size(self, base64_image):
        """
        Validate image size (max 5MB)
        
        Args:
            base64_image: Base64 encoded image string
            
        Returns:
            dict: {'valid': bool, 'message': str}
        """
        if not base64_image:
            return {'valid': True}
        
        # Calculate size in bytes (base64 is about 1.37x larger than original)
        size_bytes = len(base64_image) * 3 / 4
        max_size_mb = 5
        max_size_bytes = max_size_mb * 1024 * 1024
        
        if size_bytes > max_size_bytes:
            actual_size_mb = size_bytes / (1024 * 1024)
            return {
                'valid': False,
                'message': _('Image size (%.2f MB) exceeds maximum allowed size of %d MB') % (actual_size_mb, max_size_mb)
            }
        
        return {'valid': True}

