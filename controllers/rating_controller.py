# -*- coding: utf-8 -*-

import json
import logging
from odoo import http, _
from odoo.http import request
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class CyclexRatingController(http.Controller):
    """
    Rating and Feedback API Controller for CycleX Mobile App
    """
    
    @http.route('/api/cyclex/order/rate/<int:request_id>', type='http', auth='user', methods=['POST'], csrf=False)
    def rate_order(self, request_id, **kwargs):
        """
        Rate and provide feedback for a completed order
        
        Expected params:
        - rating: Rating (1-5)
        - comments: (Optional) Customer comments/feedback
        
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
            if partner.cyclex_user_type != 'customer':
                return request.make_response(
                    json.dumps({
                        'success': False,
                        'message': _('Only customers can rate orders'),
                        'error_code': 'INVALID_USER_TYPE'
                    }),
                    headers={'Content-Type': 'application/json'},
                    status=403
                )
            
            rating = data.get('rating')
            comments = data.get('comments', '')
            
            # Validation
            if not rating or rating not in ['1', '2', '3', '4', '5']:
                return request.make_response(
                    json.dumps({
                        'success': False,
                        'message': _('Rating must be between 1 and 5'),
                        'error_code': 'INVALID_RATING'
                    }),
                    headers={'Content-Type': 'application/json'},
                    status=400
                )
            
            # Find request
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
            
            # Verify ownership
            if req.customer_id.id != partner.id:
                return request.make_response(
                    json.dumps({
                        'success': False,
                        'message': _('Access denied'),
                        'error_code': 'ACCESS_DENIED'
                    }),
                    headers={'Content-Type': 'application/json'},
                    status=403
                )
            
            # Verify request is collected
            if req.status != 'collected':
                return request.make_response(
                    json.dumps({
                        'success': False,
                        'message': _('Can only rate collected orders'),
                        'error_code': 'INVALID_STATUS'
                    }),
                    headers={'Content-Type': 'application/json'},
                    status=400
                )
            
            # Check if already rated
            if req.rating:
                return request.make_response(
                    json.dumps({
                        'success': False,
                        'message': _('Order already rated'),
                        'error_code': 'ALREADY_RATED'
                    }),
                    headers={'Content-Type': 'application/json'},
                    status=409
                )
            
            # Update rating and comments
            req.sudo().write({
                'rating': rating,
                'comments': comments
            })
            
            # TODO: Send notification to collector
            
            return request.make_response(
                json.dumps({
                    'success': True,
                    'message': _('Rating submitted successfully'),
                    'data': {
                        'request_id': req.id,
                        'rating': rating,
                        'collector_name': req.collector_id.name if req.collector_id else None,
                    }
                }),
                headers={'Content-Type': 'application/json'},
                status=200
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
            _logger.error(f"Rate order error: {str(e)}")
            return request.make_response(
                json.dumps({
                    'success': False,
                    'message': _('An error occurred while submitting rating'),
                    'error_code': 'SERVER_ERROR'
                }),
                headers={'Content-Type': 'application/json'},
                status=500
            )

