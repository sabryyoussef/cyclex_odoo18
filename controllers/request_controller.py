# -*- coding: utf-8 -*-

import json
import logging
from datetime import datetime
from odoo import http, _
from odoo.http import request
from odoo.exceptions import ValidationError, UserError

_logger = logging.getLogger(__name__)


class CyclexRequestController(http.Controller):
    """
    Request/Order API Controller for CycleX Mobile App
    """
    
    @http.route('/api/cyclex/request/create', type='http', auth='user', methods=['POST'], csrf=False)
    def create_request(self, **kwargs):
        """
        Create new recycling request
        
        Expected params:
        - category_id: Category ID
        - product_id: Product ID (optional for custom items)
        - quantity: Quantity
        - weight: Weight in kg (optional)
        - pickup_date: Pickup date (YYYY-MM-DD)
        - pickup_time: Pickup time slot (optional)
        - item_name: Custom item name (for custom items)
        - description: Additional description
        - photo_1: Base64 encoded image (optional)
        - photo_2: Base64 encoded image (optional)
        - gps_latitude: GPS latitude
        - gps_longitude: GPS longitude
        - address: Pickup address
        
        Returns:
        - success: True/False
        - data: Request details
        """
        try:
            # Handle both form data and JSON data
            if request.httprequest.content_type == 'application/json':
                data = json.loads(request.httprequest.data.decode('utf-8'))
            else:
                data = request.params
            
            partner = request.env.user.partner_id
            
            # Validate user type
            if partner.cyclex_user_type != 'customer':
                return request.make_response(
                    json.dumps({
                        'success': False,
                        'message': _('Only customers can create requests'),
                        'error_code': 'INVALID_USER_TYPE'
                    }),
                    headers={'Content-Type': 'application/json'},
                    status=403
                )
            
            # Required fields validation
            required_fields = ['category_id', 'quantity', 'pickup_date', 'gps_latitude', 'gps_longitude']
            for field in required_fields:
                if not data.get(field):
                    return request.make_response(
                        json.dumps({
                            'success': False,
                            'message': _('Missing required field: %s') % field,
                            'error_code': 'MISSING_PARAMS'
                        }),
                        headers={'Content-Type': 'application/json'},
                        status=400
                    )
            
            # Prepare request values
            request_vals = {
                'customer_id': partner.id,
                'category_id': int(data['category_id']),
                'quantity': float(data['quantity']),
                'pickup_date': data['pickup_date'],
                'pickup_time': data.get('pickup_time'),
                'description': data.get('description', ''),
                'gps_latitude': float(data['gps_latitude']),
                'gps_longitude': float(data['gps_longitude']),
                'pickup_address': data.get('address', ''),
                'status': 'pending',
            }
            
            # Handle product or custom item
            if data.get('product_id'):
                request_vals['product_id'] = int(data['product_id'])
            else:
                request_vals['custom_item_name'] = data.get('item_name', 'Custom Item')
            
            # Handle weight
            if data.get('weight'):
                request_vals['weight'] = float(data['weight'])
            
            # Handle photos
            if data.get('photo_1'):
                request_vals['photo_1'] = data['photo_1']
            if data.get('photo_2'):
                request_vals['photo_2'] = data['photo_2']
            
            # Create request
            new_request = request.env['cyclex.request'].sudo().create(request_vals)
            
            # Calculate estimated price if product is specified
            estimated_price = 0
            if new_request.product_id and new_request.weight:
                estimated_price = new_request.product_id.price_per_kg * new_request.weight
            
            return request.make_response(
                json.dumps({
                    'success': True,
                    'message': _('Request created successfully'),
                    'data': {
                        'request_id': new_request.id,
                        'request_number': new_request.name,
                        'status': new_request.status,
                        'estimated_price': estimated_price,
                        'pickup_date': str(new_request.pickup_date),
                        'category': new_request.category_id.name,
                        'product': new_request.product_id.name if new_request.product_id else new_request.custom_item_name,
                    }
                }),
                headers={'Content-Type': 'application/json'},
                status=201
            )
            
        except ValidationError as e:
            return request.make_response(
                json.dumps({
                    'success': False,
                    'message': str(e),
                    'error_code': 'VALIDATION_ERROR'
                }),
                headers={'Content-Type': 'application/json'},
                status=400
            )
        except Exception as e:
            _logger.error(f"Create request error: {str(e)}")
            return request.make_response(
                json.dumps({
                    'success': False,
                    'message': _('An error occurred while creating request'),
                    'error_code': 'SERVER_ERROR'
                }),
                headers={'Content-Type': 'application/json'},
                status=500
            )
    
    @http.route('/api/cyclex/request/list', type='http', auth='user', methods=['POST'], csrf=False)
    def get_requests(self, **kwargs):
        """
        Get user's requests
        
        Optional params:
        - status: Filter by status ('pending', 'assigned', 'collected', 'all')
        - limit: Number of results (default: 20)
        - offset: Pagination offset
        
        Returns:
        - success: True/False
        - data: List of requests
        """
        try:
            # Handle both form data and JSON data
            if request.httprequest.content_type == 'application/json':
                data = json.loads(request.httprequest.data.decode('utf-8'))
            else:
                data = request.params
            
            partner = request.env.user.partner_id
            
            if partner.cyclex_user_type != 'customer':
                return request.make_response(
                    json.dumps({
                        'success': False,
                        'message': _('Only customers can view requests'),
                        'error_code': 'INVALID_USER_TYPE'
                    }),
                    headers={'Content-Type': 'application/json'},
                    status=403
                )
            
            # Get parameters
            status_filter = data.get('status', 'all')
            limit = int(data.get('limit', 20))
            offset = int(data.get('offset', 0))
            
            # Build domain
            domain = [('customer_id', '=', partner.id)]
            if status_filter and status_filter != 'all':
                domain.append(('status', '=', status_filter))
            
            # Search requests
            requests = request.env['cyclex.request'].sudo().search(
                domain,
                order='create_date desc',
                limit=limit,
                offset=offset
            )
            
            total_count = request.env['cyclex.request'].sudo().search_count(domain)
            
            # Format response
            request_list = []
            for req in requests:
                request_list.append({
                    'id': req.id,
                    'request_number': req.name,
                    'status': req.status,
                    'status_display': dict(req._fields['status'].selection).get(req.status),
                    'category': req.category_id.name,
                    'product': req.product_id.name if req.product_id else req.custom_item_name,
                    'quantity': req.quantity,
                    'weight': req.weight,
                    'pickup_date': str(req.pickup_date),
                    'pickup_time': req.pickup_time,
                    'pickup_address': req.pickup_address,
                    'estimated_price': req.estimated_price,
                    'final_price': req.final_price,
                    'collector_name': req.collector_id.name if req.collector_id else None,
                    'created_date': str(req.create_date),
                })
            
            return request.make_response(
                json.dumps({
                    'success': True,
                    'data': {
                        'requests': request_list,
                        'total': total_count,
                        'limit': limit,
                        'offset': offset,
                        'status_filter': status_filter
                    }
                }),
                headers={'Content-Type': 'application/json'},
                status=200
            )
            
        except Exception as e:
            _logger.error(f"Get requests error: {str(e)}")
            return request.make_response(
                json.dumps({
                    'success': False,
                    'message': _('An error occurred while fetching requests'),
                    'error_code': 'SERVER_ERROR'
                }),
                headers={'Content-Type': 'application/json'},
                status=500
            )
    
    @http.route('/api/cyclex/request/details/<int:request_id>', type='http', auth='user', methods=['POST'], csrf=False)
    def get_request_details(self, request_id, **kwargs):
        """
        Get detailed request information
        
        Returns:
        - success: True/False
        - data: Request details with tracking info
        """
        try:
            partner = request.env.user.partner_id
            
            # Get request
            req = request.env['cyclex.request'].sudo().browse(request_id)
            
            if not req.exists():
                return request.make_response(
                    json.dumps({
                        'success': False,
                        'message': _('Request not found'),
                        'error_code': 'NOT_FOUND'
                    }),
                    headers={'Content-Type': 'application/json'},
                    status=404
                )
            
            # Check ownership (customers can only see their own requests)
            if partner.cyclex_user_type == 'customer' and req.customer_id.id != partner.id:
                return request.make_response(
                    json.dumps({
                        'success': False,
                        'message': _('Access denied'),
                        'error_code': 'ACCESS_DENIED'
                    }),
                    headers={'Content-Type': 'application/json'},
                    status=403
                )
            
            # Format detailed response
            request_data = {
                'id': req.id,
                'request_number': req.name,
                'status': req.status,
                'status_display': dict(req._fields['status'].selection).get(req.status),
                'category': {
                    'id': req.category_id.id,
                    'name': req.category_id.name,
                    'icon': req.category_id.icon or ''
                },
                'product': {
                    'id': req.product_id.id if req.product_id else None,
                    'name': req.product_id.name if req.product_id else req.custom_item_name,
                    'price_per_kg': req.product_id.price_per_kg if req.product_id else 0
                },
                'quantity': req.quantity,
                'weight': req.weight,
                'pickup_date': str(req.pickup_date),
                'pickup_time': req.pickup_time,
                'pickup_address': req.pickup_address,
                'gps_latitude': req.gps_latitude,
                'gps_longitude': req.gps_longitude,
                'description': req.description,
                'estimated_price': req.estimated_price,
                'final_price': req.final_price,
                'customer': {
                    'id': req.customer_id.id,
                    'name': req.customer_id.name,
                    'phone': req.customer_id.phone
                },
                'collector': {
                    'id': req.collector_id.id if req.collector_id else None,
                    'name': req.collector_id.name if req.collector_id else None,
                    'phone': req.collector_id.phone if req.collector_id else None,
                    'rating': req.collector_id.average_rating if req.collector_id else 0
                } if req.collector_id else None,
                'photos': {
                    'photo_1': req.photo_1 if req.photo_1 else None,
                    'photo_2': req.photo_2 if req.photo_2 else None
                },
                'created_date': str(req.create_date),
                'assigned_date': str(req.assigned_date) if req.assigned_date else None,
                'collected_date': str(req.collected_date) if req.collected_date else None,
            }
            
            return request.make_response(
                json.dumps({
                    'success': True,
                    'data': request_data
                }),
                headers={'Content-Type': 'application/json'},
                status=200
            )
            
        except Exception as e:
            _logger.error(f"Get request details error: {str(e)}")
            return request.make_response(
                json.dumps({
                    'success': False,
                    'message': _('An error occurred while fetching request details'),
                    'error_code': 'SERVER_ERROR'
                }),
                headers={'Content-Type': 'application/json'},
                status=500
            )