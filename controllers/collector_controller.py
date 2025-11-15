# -*- coding: utf-8 -*-

import json
import logging
from odoo import http, _
from odoo.http import request
from odoo.exceptions import ValidationError, UserError

_logger = logging.getLogger(__name__)


class CyclexCollectorController(http.Controller):
    """
    Collector API Controller for CycleX Mobile App
    """
    
    @http.route('/api/cyclex/collector/available-orders', type='http', auth='user', methods=['POST'], csrf=False)
    def get_available_orders(self, **kwargs):
        """
        Get available orders for collectors
        
        Optional params:
        - limit: Number of results (default: 20)
        - offset: Pagination offset
        
        Returns:
        - success: True/False
        - data: List of available requests
        """
        try:
            # Handle both form data and JSON data
            if request.httprequest.content_type == 'application/json':
                data = json.loads(request.httprequest.data.decode('utf-8'))
            else:
                data = request.params
            
            partner = request.env.user.partner_id
            
            # Validate user type
            if partner.cyclex_user_type != 'collector':
                return request.make_response(
                    json.dumps({
                        'success': False,
                        'message': _('Only collectors can view available orders'),
                        'error_code': 'INVALID_USER_TYPE'
                    }),
                    headers={'Content-Type': 'application/json'},
                    status=403
                )
            
            # Check collector approval status
            if partner.collector_approval_status != 'approved':
                return request.make_response(
                    json.dumps({
                        'success': False,
                        'message': _('Collector account not approved'),
                        'error_code': 'NOT_APPROVED'
                    }),
                    headers={'Content-Type': 'application/json'},
                    status=403
                )
            
            # Get parameters
            limit = int(data.get('limit', 20))
            offset = int(data.get('offset', 0))
            
            # Search available requests (pending status, no collector assigned)
            requests = request.env['cyclex.request'].sudo().search([
                ('status', '=', 'pending'),
                ('collector_id', '=', False)
            ], order='create_date desc', limit=limit, offset=offset)
            
            total_count = request.env['cyclex.request'].sudo().search_count([
                ('status', '=', 'pending'),
                ('collector_id', '=', False)
            ])
            
            # Format response
            request_list = []
            for req in requests:
                request_list.append({
                    'id': req.id,
                    'request_number': req.name,
                    'customer_name': req.customer_id.name,
                    'customer_phone': req.customer_id.phone,
                    'category': req.category_id.name,
                    'product': req.product_id.name if req.product_id else req.custom_item_name,
                    'quantity': req.quantity,
                    'weight': req.weight,
                    'pickup_date': str(req.pickup_date),
                    'pickup_time': req.pickup_time,
                    'pickup_address': req.pickup_address,
                    'gps_latitude': req.gps_latitude,
                    'gps_longitude': req.gps_longitude,
                    'estimated_price': req.estimated_price,
                    'distance': 0,  # TODO: Calculate distance from collector location
                    'created_date': str(req.create_date),
                })
            
            return request.make_response(
                json.dumps({
                    'success': True,
                    'data': {
                        'requests': request_list,
                        'total': total_count,
                        'limit': limit,
                        'offset': offset
                    }
                }),
                headers={'Content-Type': 'application/json'},
                status=200
            )
            
        except Exception as e:
            _logger.error(f"Get available orders error: {str(e)}")
            return request.make_response(
                json.dumps({
                    'success': False,
                    'message': _('An error occurred while fetching available orders'),
                    'error_code': 'SERVER_ERROR'
                }),
                headers={'Content-Type': 'application/json'},
                status=500
            )
    
    @http.route('/api/cyclex/collector/accept-order/<int:request_id>', type='http', auth='user', methods=['POST'], csrf=False)
    def accept_order(self, request_id, **kwargs):
        """
        Accept an available order
        
        Returns:
        - success: True/False
        - message: Status message
        """
        try:
            partner = request.env.user.partner_id
            
            # Validate user type
            if partner.cyclex_user_type != 'collector':
                return request.make_response(
                    json.dumps({
                        'success': False,
                        'message': _('Only collectors can accept orders'),
                        'error_code': 'INVALID_USER_TYPE'
                    }),
                    headers={'Content-Type': 'application/json'},
                    status=403
                )
            
            # Check collector approval status
            if partner.collector_approval_status != 'approved':
                return request.make_response(
                    json.dumps({
                        'success': False,
                        'message': _('Collector account not approved'),
                        'error_code': 'NOT_APPROVED'
                    }),
                    headers={'Content-Type': 'application/json'},
                    status=403
                )
            
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
            
            # Check if request is still available
            if req.status != 'pending' or req.collector_id:
                return request.make_response(
                    json.dumps({
                        'success': False,
                        'message': _('Request is no longer available'),
                        'error_code': 'NOT_AVAILABLE'
                    }),
                    headers={'Content-Type': 'application/json'},
                    status=409
                )
            
            # Assign request to collector
            req.sudo().write({
                'collector_id': partner.id,
                'status': 'assigned',
                'assigned_date': request.env.cr.now()
            })
            
            # TODO: Send notification to customer
            
            return request.make_response(
                json.dumps({
                    'success': True,
                    'message': _('Order accepted successfully'),
                    'data': {
                        'request_id': req.id,
                        'request_number': req.name,
                        'customer_name': req.customer_id.name,
                        'pickup_address': req.pickup_address
                    }
                }),
                headers={'Content-Type': 'application/json'},
                status=200
            )
            
        except Exception as e:
            _logger.error(f"Accept order error: {str(e)}")
            return request.make_response(
                json.dumps({
                    'success': False,
                    'message': _('An error occurred while accepting order'),
                    'error_code': 'SERVER_ERROR'
                }),
                headers={'Content-Type': 'application/json'},
                status=500
            )
    
    @http.route('/api/cyclex/collector/complete-order/<int:request_id>', type='http', auth='user', methods=['POST'], csrf=False)
    def complete_order(self, request_id, **kwargs):
        """
        Complete/finish an assigned order
        
        Expected params:
        - final_weight: Final weight collected
        - notes: Collection notes (optional)
        
        Returns:
        - success: True/False
        - message: Status message
        """
        try:
            # Handle both form data and JSON data
            if request.httprequest.content_type == 'application/json':
                data = json.loads(request.httprequest.data.decode('utf-8'))
            else:
                data = request.params
            
            partner = request.env.user.partner_id
            
            # Validate user type
            if partner.cyclex_user_type != 'collector':
                return request.make_response(
                    json.dumps({
                        'success': False,
                        'message': _('Only collectors can complete orders'),
                        'error_code': 'INVALID_USER_TYPE'
                    }),
                    headers={'Content-Type': 'application/json'},
                    status=403
                )
            
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
            
            # Check if collector owns this request
            if req.collector_id.id != partner.id:
                return request.make_response(
                    json.dumps({
                        'success': False,
                        'message': _('Access denied'),
                        'error_code': 'ACCESS_DENIED'
                    }),
                    headers={'Content-Type': 'application/json'},
                    status=403
                )
            
            # Check if request is in correct status
            if req.status != 'assigned':
                return request.make_response(
                    json.dumps({
                        'success': False,
                        'message': _('Request cannot be completed in current status'),
                        'error_code': 'INVALID_STATUS'
                    }),
                    headers={'Content-Type': 'application/json'},
                    status=400
                )
            
            # Get final weight
            final_weight = float(data.get('final_weight', req.weight or 0))
            notes = data.get('notes', '')
            
            # Calculate final price
            final_price = 0
            if req.product_id and final_weight:
                final_price = req.product_id.price_per_kg * final_weight
            
            # Update request
            req.sudo().write({
                'status': 'collected',
                'final_weight': final_weight,
                'final_price': final_price,
                'collection_notes': notes,
                'collected_date': request.env.cr.now()
            })
            
            # TODO: Create wallet transaction for customer
            # TODO: Create commission record for collector
            # TODO: Send notification to customer
            
            return request.make_response(
                json.dumps({
                    'success': True,
                    'message': _('Order completed successfully'),
                    'data': {
                        'request_id': req.id,
                        'final_weight': final_weight,
                        'final_price': final_price,
                        'commission': final_price * 0.1  # TODO: Get from settings
                    }
                }),
                headers={'Content-Type': 'application/json'},
                status=200
            )
            
        except Exception as e:
            _logger.error(f"Complete order error: {str(e)}")
            return request.make_response(
                json.dumps({
                    'success': False,
                    'message': _('An error occurred while completing order'),
                    'error_code': 'SERVER_ERROR'
                }),
                headers={'Content-Type': 'application/json'},
                status=500
            )
    
    @http.route('/api/cyclex/collector/scan-qr', type='http', auth='user', methods=['POST'], csrf=False)
    def scan_qr(self, **kwargs):
        """
        Scan QR code to verify request
        
        Expected params:
        - qr_code: QR code data
        
        Returns:
        - success: True/False
        - data: Request details if valid
        """
        try:
            # Handle both form data and JSON data
            if request.httprequest.content_type == 'application/json':
                data = json.loads(request.httprequest.data.decode('utf-8'))
            else:
                data = request.params
            
            partner = request.env.user.partner_id
            
            # Validate user type
            if partner.cyclex_user_type != 'collector':
                return request.make_response(
                    json.dumps({
                        'success': False,
                        'message': _('Only collectors can scan QR codes'),
                        'error_code': 'INVALID_USER_TYPE'
                    }),
                    headers={'Content-Type': 'application/json'},
                    status=403
                )
            
            qr_code = data.get('qr_code')
            if not qr_code:
                return request.make_response(
                    json.dumps({
                        'success': False,
                        'message': _('QR code is required'),
                        'error_code': 'MISSING_PARAMS'
                    }),
                    headers={'Content-Type': 'application/json'},
                    status=400
                )
            
            # TODO: Implement QR code validation logic
            # For now, assume QR code contains request ID
            try:
                request_id = int(qr_code)
                req = request.env['cyclex.request'].sudo().browse(request_id)
                
                if not req.exists():
                    return request.make_response(
                        json.dumps({
                            'success': False,
                            'message': _('Invalid QR code'),
                            'error_code': 'INVALID_QR'
                        }),
                        headers={'Content-Type': 'application/json'},
                        status=404
                    )
                
                # Check if collector is assigned to this request
                if req.collector_id.id != partner.id:
                    return request.make_response(
                        json.dumps({
                            'success': False,
                            'message': _('This request is not assigned to you'),
                            'error_code': 'NOT_ASSIGNED'
                        }),
                        headers={'Content-Type': 'application/json'},
                        status=403
                    )
                
                return request.make_response(
                    json.dumps({
                        'success': True,
                        'message': _('QR code verified successfully'),
                        'data': {
                            'request_id': req.id,
                            'request_number': req.name,
                            'customer_name': req.customer_id.name,
                            'product': req.product_id.name if req.product_id else req.custom_item_name,
                            'quantity': req.quantity,
                            'estimated_weight': req.weight
                        }
                    }),
                    headers={'Content-Type': 'application/json'},
                    status=200
                )
                
            except ValueError:
                return request.make_response(
                    json.dumps({
                        'success': False,
                        'message': _('Invalid QR code format'),
                        'error_code': 'INVALID_QR'
                    }),
                    headers={'Content-Type': 'application/json'},
                    status=400
                )
            
        except Exception as e:
            _logger.error(f"Scan QR error: {str(e)}")
            return request.make_response(
                json.dumps({
                    'success': False,
                    'message': _('An error occurred while scanning QR code'),
                    'error_code': 'SERVER_ERROR'
                }),
                headers={'Content-Type': 'application/json'},
                status=500
            )