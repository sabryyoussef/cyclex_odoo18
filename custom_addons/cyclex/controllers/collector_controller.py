# -*- coding: utf-8 -*-

import logging
from odoo import http, _, fields
from odoo.http import request
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class CyclexCollectorController(http.Controller):
    """
    Collector API Controller for CycleX Mobile App
    """
    
    @http.route('/api/cyclex/collector/register', type='json', auth='public', methods=['POST'], csrf=False)
    def register_collector(self, **kwargs):
        """
        Register as a collector (extends auth/register with collector-specific fields)
        
        Expected params:
        - name, phone, password (from base registration)
        - id_number: National ID
        - vehicle_type: Type of vehicle
        - working_area_ids: List of working area IDs (max 5)
        
        Returns:
        - success: True/False
        - message: Status message
        """
        # This should call the main register API with user_type='collector'
        kwargs['user_type'] = 'collector'
        
        # Call the auth register endpoint
        auth_controller = request.env.ref('cyclex.controller_auth').sudo()
        return auth_controller.register(**kwargs)
    
    @http.route('/api/cyclex/collector/available-orders', type='json', auth='user', methods=['GET'], csrf=False)
    def get_available_orders(self, **kwargs):
        """
        Get available orders in collector's working areas
        
        Optional params:
        - limit: Number of results (default: 20)
        - offset: Pagination offset
        
        Returns:
        - success: True/False
        - data: List of available orders
        """
        try:
            partner = request.env.user.partner_id
            
            # Validate user type
            if partner.cyclex_user_type != 'collector':
                return {
                    'success': False,
                    'message': _('Only collectors can access this endpoint'),
                    'error_code': 'INVALID_USER_TYPE'
                }
            
            # Check approval status
            if partner.collector_approval_status != 'approved':
                return {
                    'success': False,
                    'message': _('Collector account not approved yet'),
                    'error_code': 'NOT_APPROVED'
                }
            
            limit = int(kwargs.get('limit', 20))
            offset = int(kwargs.get('offset', 0))
            
            # Get available requests (pending status, in collector's working areas)
            domain = [
                ('status', '=', 'pending'),
                '|', 
                ('collector_id', '=', False),
                ('collector_id', '=', partner.id)
            ]
            
            # TODO: Filter by working areas based on customer location
            
            requests = request.env['cyclex.request'].sudo().search(
                domain,
                order='create_date desc',
                limit=limit,
                offset=offset
            )
            
            total_count = request.env['cyclex.request'].sudo().search_count(domain)
            
            # Format response
            order_list = []
            for req in requests:
                order_list.append({
                    'id': req.id,
                    'request_number': req.name,
                    'product_name': req.product_id.name,
                    'category_name': req.category_id.name,
                    'weight': req.weight,
                    'calculated_price': req.calculated_price,
                    'currency_symbol': req.currency_id.symbol,
                    'pickup_date': str(req.pickup_date),
                    'customer_name': req.customer_id.name,
                    'customer_phone': req.customer_id.phone,
                    'customer_address': {
                        'street': req.customer_id.street or '',
                        'city': req.customer_id.city or '',
                        'latitude': req.customer_id.gps_latitude,
                        'longitude': req.customer_id.gps_longitude,
                    },
                    'distance': None,  # TODO: Calculate based on collector location
                })
            
            return {
                'success': True,
                'data': {
                    'orders': order_list,
                    'total': total_count,
                    'limit': limit,
                    'offset': offset
                }
            }
            
        except Exception as e:
            _logger.error(f"Get available orders error: {str(e)}")
            return {
                'success': False,
                'message': _('An error occurred while fetching orders'),
                'error_code': 'SERVER_ERROR'
            }
    
    @http.route('/api/cyclex/collector/accept-order/<int:request_id>', type='json', auth='user', methods=['POST'], csrf=False)
    def accept_order(self, request_id, **kwargs):
        """
        Accept an order assignment
        
        Returns:
        - success: True/False
        - message: Status message
        """
        try:
            partner = request.env.user.partner_id
            
            if partner.cyclex_user_type != 'collector':
                return {
                    'success': False,
                    'message': _('Only collectors can accept orders'),
                    'error_code': 'INVALID_USER_TYPE'
                }
            
            req = request.env['cyclex.request'].sudo().browse(request_id)
            
            if not req.exists():
                return {
                    'success': False,
                    'message': _('Request not found'),
                    'error_code': 'NOT_FOUND'
                }
            
            if req.status != 'pending':
                return {
                    'success': False,
                    'message': _('Request is not available'),
                    'error_code': 'NOT_AVAILABLE'
                }
            
            # Assign collector
            req.sudo().write({
                'collector_id': partner.id,
                'status': 'assigned'
            })
            
            return {
                'success': True,
                'message': _('Order accepted successfully'),
                'data': {
                    'request_id': req.id,
                    'status': req.status,
                    'deadline': str(fields.Date.today() + fields.timedelta(days=3))
                }
            }
            
        except ValidationError as e:
            return {
                'success': False,
                'message': str(e),
                'error_code': 'VALIDATION_ERROR'
            }
        except Exception as e:
            _logger.error(f"Accept order error: {str(e)}")
            return {
                'success': False,
                'message': _('An error occurred while accepting order'),
                'error_code': 'SERVER_ERROR'
            }
    
    @http.route('/api/cyclex/collector/reject-order/<int:request_id>', type='json', auth='user', methods=['POST'], csrf=False)
    def reject_order(self, request_id, **kwargs):
        """
        Reject an order
        
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
            
            # Remove collector assignment
            if req.collector_id.id == partner.id:
                req.sudo().write({
                    'collector_id': False,
                    'status': 'pending'
                })
            
            return {
                'success': True,
                'message': _('Order rejected successfully')
            }
            
        except Exception as e:
            _logger.error(f"Reject order error: {str(e)}")
            return {
                'success': False,
                'message': _('An error occurred'),
                'error_code': 'SERVER_ERROR'
            }
    
    @http.route('/api/cyclex/collector/scan-qr', type='json', auth='user', methods=['POST'], csrf=False)
    def scan_qr(self, **kwargs):
        """
        Scan QR code to validate order
        
        Expected params:
        - qr_code: QR code string
        
        Returns:
        - success: True/False
        - data: Order details if valid
        """
        try:
            partner = request.env.user.partner_id
            qr_code = kwargs.get('qr_code')
            
            if not qr_code:
                return {
                    'success': False,
                    'message': _('QR code is required'),
                    'error_code': 'MISSING_PARAMS'
                }
            
            # Find request by QR code
            req = request.env['cyclex.request'].sudo().search([
                ('qr_code', '=', qr_code)
            ], limit=1)
            
            if not req:
                return {
                    'success': False,
                    'message': _('Invalid QR code'),
                    'error_code': 'INVALID_QR'
                }
            
            # Verify collector assignment
            if req.collector_id.id != partner.id:
                return {
                    'success': False,
                    'message': _('This order is not assigned to you'),
                    'error_code': 'NOT_ASSIGNED'
                }
            
            return {
                'success': True,
                'message': _('QR code valid'),
                'data': {
                    'request_id': req.id,
                    'request_number': req.name,
                    'customer_name': req.customer_id.name,
                    'product_name': req.product_id.name,
                    'weight': req.weight,
                    'calculated_price': req.calculated_price,
                    'currency_symbol': req.currency_id.symbol,
                    'status': req.status
                }
            }
            
        except Exception as e:
            _logger.error(f"Scan QR error: {str(e)}")
            return {
                'success': False,
                'message': _('An error occurred'),
                'error_code': 'SERVER_ERROR'
            }
    
    @http.route('/api/cyclex/collector/complete-order/<int:request_id>', type='json', auth='user', methods=['POST'], csrf=False)
    def complete_order(self, request_id, **kwargs):
        """
        Mark order as collected (completes the transaction)
        
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
            
            # Verify collector
            if req.collector_id.id != partner.id:
                return {
                    'success': False,
                    'message': _('This order is not assigned to you'),
                    'error_code': 'NOT_ASSIGNED'
                }
            
            # Mark as collected (this will trigger wallet credit and commission creation)
            req.action_mark_collected()
            
            return {
                'success': True,
                'message': _('Order completed successfully'),
                'data': {
                    'request_id': req.id,
                    'status': req.status,
                    'payment_amount': req.calculated_price,
                    'commission_earned': (req.calculated_price * partner.collector_commission_rate) / 100,
                }
            }
            
        except ValidationError as e:
            return {
                'success': False,
                'message': str(e),
                'error_code': 'VALIDATION_ERROR'
            }
        except Exception as e:
            _logger.error(f"Complete order error: {str(e)}")
            return {
                'success': False,
                'message': _('An error occurred'),
                'error_code': 'SERVER_ERROR'
            }

