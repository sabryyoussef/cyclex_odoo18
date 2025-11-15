# -*- coding: utf-8 -*-

import logging
from odoo import http, _
from odoo.http import request
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class CyclexRatingController(http.Controller):
    """
    Rating and Feedback API Controller for CycleX Mobile App
    """
    
    @http.route('/api/cyclex/order/rate/<int:request_id>', type='json', auth='user', methods=['POST'], csrf=False)
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
            partner = request.env.user.partner_id
            
            # Validate user type
            if partner.cyclex_user_type != 'customer':
                return {
                    'success': False,
                    'message': _('Only customers can rate orders'),
                    'error_code': 'INVALID_USER_TYPE'
                }
            
            rating = kwargs.get('rating')
            comments = kwargs.get('comments', '')
            
            # Validation
            if not rating or rating not in ['1', '2', '3', '4', '5']:
                return {
                    'success': False,
                    'message': _('Rating must be between 1 and 5'),
                    'error_code': 'INVALID_RATING'
                }
            
            # Find request
            req = request.env['cyclex.request'].sudo().browse(request_id)
            
            if not req.exists():
                return {
                    'success': False,
                    'message': _('Request not found'),
                    'error_code': 'NOT_FOUND'
                }
            
            # Verify ownership
            if req.customer_id.id != partner.id:
                return {
                    'success': False,
                    'message': _('Access denied'),
                    'error_code': 'ACCESS_DENIED'
                }
            
            # Verify request is collected
            if req.status != 'collected':
                return {
                    'success': False,
                    'message': _('Can only rate collected orders'),
                    'error_code': 'INVALID_STATUS'
                }
            
            # Check if already rated
            if req.rating:
                return {
                    'success': False,
                    'message': _('Order already rated'),
                    'error_code': 'ALREADY_RATED'
                }
            
            # Update rating and comments
            req.sudo().write({
                'rating': rating,
                'comments': comments
            })
            
            # TODO: Send notification to collector
            
            return {
                'success': True,
                'message': _('Rating submitted successfully'),
                'data': {
                    'request_id': req.id,
                    'rating': rating,
                    'collector_name': req.collector_id.name if req.collector_id else None,
                }
            }
            
        except ValidationError as e:
            return {
                'success': False,
                'message': str(e),
                'error_code': 'VALIDATION_ERROR'
            }
        except Exception as e:
            _logger.error(f"Rate order error: {str(e)}")
            return {
                'success': False,
                'message': _('An error occurred while submitting rating'),
                'error_code': 'SERVER_ERROR'
            }

