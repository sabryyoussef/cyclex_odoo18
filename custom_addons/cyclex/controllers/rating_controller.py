# -*- coding: utf-8 -*-

from odoo import http
from odoo.exceptions import ValidationError
from odoo.http import request

from .api_base import CycleXApiBase


class CycleXRatingController(CycleXApiBase):
    """Rating and feedback API endpoints."""

    @http.route('/api/cyclex/order/rate/<int:request_id>', type='http', auth='public', methods=['POST'], csrf=False)
    def rate_order(self, request_id, **kwargs):
        try:
            user, error = self._authenticate(required_user_type='customer')
            if error:
                return error

            params = self._get_params()
            rating = params.get('rating')
            if not rating:
                return self._error('Rating is required', code='missing_fields')

            rating = str(rating)
            if rating not in ('1', '2', '3', '4', '5'):
                return self._error('Rating must be between 1 and 5', code='invalid_rating')

            env = self._env_as_user(user)
            req = env['cyclex.request'].browse(request_id)
            if not req.exists():
                return self._error('Order not found', code='not_found', status=404)
            if req.customer_id != user.partner_id:
                return self._error('Access denied', code='forbidden', status=403)
            if req.status != 'collected':
                return self._error(
                    'Only collected orders can be rated',
                    code='invalid_status',
                )
            if req.rating:
                return self._error('Order has already been rated', code='already_rated')

            req.write({
                'rating': rating,
                'comments': params.get('comments', ''),
            })

            return self._success(
                self._serialize_request(req),
                message='Rating submitted successfully',
            )
        except ValidationError as exc:
            return self._error(str(exc), code='validation_error')
        except Exception as exc:
            return self._handle_exception(exc)
