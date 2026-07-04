# -*- coding: utf-8 -*-

from odoo import http
from odoo.exceptions import ValidationError
from odoo.http import request

from .api_base import CycleXApiBase


class CycleXRequestController(CycleXApiBase):
    """Customer recycling request API endpoints."""

    @http.route('/api/cyclex/request/create', type='http', auth='public', methods=['POST'], csrf=False)
    def request_create(self, **kwargs):
        try:
            user, error = self._authenticate(required_user_type='customer')
            if error:
                return error

            params = self._get_params()
            required = ['category_id', 'product_id', 'quantity', 'weight', 'pickup_date']
            missing = [field for field in required if params.get(field) in (None, '')]
            if missing:
                return self._error(
                    'Missing required fields: %s' % ', '.join(missing),
                    code='missing_fields',
                )

            env = self._env_as_user(user)
            partner = user.partner_id

            vals = {
                'customer_id': partner.id,
                'category_id': int(params['category_id']),
                'product_id': int(params['product_id']),
                'quantity': int(params['quantity']),
                'weight': float(params['weight']),
                'pickup_date': params['pickup_date'],
                'status': 'pending',
            }

            if params.get('photo_1'):
                vals['photo_1'] = self._decode_image(params['photo_1'])
            if params.get('photo_2'):
                vals['photo_2'] = self._decode_image(params['photo_2'])
            if params.get('gps_latitude') and params.get('gps_longitude'):
                vals['gps_latitude'] = float(params['gps_latitude'])
                vals['gps_longitude'] = float(params['gps_longitude'])
            elif partner.gps_latitude and partner.gps_longitude:
                vals['gps_latitude'] = partner.gps_latitude
                vals['gps_longitude'] = partner.gps_longitude

            req = env['cyclex.request'].create(vals)
            return self._success(
                self._serialize_request(req, include_qr=True),
                message='Request created successfully',
                status=201,
            )
        except ValidationError as exc:
            return self._error(str(exc), code='validation_error')
        except Exception as exc:
            return self._handle_exception(exc)

    @http.route('/api/cyclex/request/list', type='http', auth='public', methods=['GET'], csrf=False)
    def request_list(self, **kwargs):
        try:
            user, error = self._authenticate(required_user_type='customer')
            if error:
                return error

            params = self._get_params()
            env = self._env_as_user(user)
            domain = [('customer_id', '=', user.partner_id.id)]

            status = params.get('status')
            if status:
                domain.append(('status', '=', status))

            result = self._paginate(
                env['cyclex.request'],
                domain,
                self._serialize_request,
                page=params.get('page', 1),
                limit=params.get('limit', 20),
                order='create_date desc',
            )
            return self._success(result)
        except Exception as exc:
            return self._handle_exception(exc)

    @http.route('/api/cyclex/request/details/<int:request_id>', type='http', auth='public', methods=['GET'], csrf=False)
    def request_details(self, request_id, **kwargs):
        try:
            user, error = self._authenticate()
            if error:
                return error

            env = self._env_as_user(user)
            req = env['cyclex.request'].browse(request_id)
            if not req.exists():
                return self._error('Request not found', code='not_found', status=404)

            partner = user.partner_id
            if partner.cyclex_user_type == 'customer' and req.customer_id != partner:
                return self._error('Access denied', code='forbidden', status=403)
            if partner.cyclex_user_type == 'collector' and req.collector_id and req.collector_id != partner:
                return self._error('Access denied', code='forbidden', status=403)

            return self._success(self._serialize_request(req, include_qr=True))
        except Exception as exc:
            return self._handle_exception(exc)

    @http.route('/api/cyclex/request/cancel/<int:request_id>', type='http', auth='public', methods=['POST'], csrf=False)
    def request_cancel(self, request_id, **kwargs):
        try:
            user, error = self._authenticate(required_user_type='customer')
            if error:
                return error

            env = self._env_as_user(user)
            req = env['cyclex.request'].browse(request_id)
            if not req.exists():
                return self._error('Request not found', code='not_found', status=404)
            if req.customer_id != user.partner_id:
                return self._error('Access denied', code='forbidden', status=403)
            if req.status != 'pending':
                return self._error(
                    'Only pending requests can be cancelled',
                    code='invalid_status',
                )

            req.action_cancel()
            return self._success(
                self._serialize_request(req),
                message='Request cancelled successfully',
            )
        except ValidationError as exc:
            return self._error(str(exc), code='validation_error')
        except Exception as exc:
            return self._handle_exception(exc)
