# -*- coding: utf-8 -*-

from odoo import http
from odoo.exceptions import ValidationError
from odoo.http import request

from .api_base import CycleXApiBase


class CycleXCollectorController(CycleXApiBase):
    """Collector API endpoints."""

    @http.route('/api/cyclex/collector/register', type='http', auth='public', methods=['POST'], csrf=False)
    def collector_register(self, **kwargs):
        try:
            params = self._get_params()
            required = ['name', 'phone', 'password', 'id_number', 'vehicle_type']
            missing = [field for field in required if not params.get(field)]
            if missing:
                return self._error(
                    'Missing required fields: %s' % ', '.join(missing),
                    code='missing_fields',
                )

            if not params.get('confirm_password'):
                params['confirm_password'] = params['password']
            if params['password'] != params['confirm_password']:
                return self._error('Passwords do not match', code='password_mismatch')

            working_area_ids = params.get('working_area_ids') or params.get('working_areas') or []
            if isinstance(working_area_ids, str):
                working_area_ids = [int(x) for x in working_area_ids.split(',') if x.strip()]
            elif isinstance(working_area_ids, list):
                working_area_ids = [int(x) for x in working_area_ids if str(x).strip()]
            params['working_area_ids'] = working_area_ids

            if len(working_area_ids) > 5:
                return self._error(
                    'A collector can have a maximum of 5 working areas',
                    code='validation_error',
                )

            partner, user = self._create_cyclex_user(params, user_type='collector')
            code = partner.generate_verification_code()
            self._send_verification_sms(partner, code)

            return self._success({
                'user_id': partner.id,
                'phone': partner.phone,
                'collector_approval_status': partner.collector_approval_status,
                'working_areas': [
                    self._serialize_working_area(area)
                    for area in partner.working_area_ids
                ],
                'verification_required': True,
            }, message='Collector registration submitted for approval', status=201)
        except ValidationError as exc:
            return self._error(str(exc), code='validation_error')
        except Exception as exc:
            return self._handle_exception(exc)

    @http.route('/api/cyclex/collector/available-orders', type='http', auth='public', methods=['GET'], csrf=False)
    def available_orders(self, **kwargs):
        try:
            user, error = self._authenticate(required_user_type='collector')
            if error:
                return error

            params = self._get_params()
            env = self._env_as_user(user)
            domain = [('status', '=', 'pending')]

            status_filter = params.get('status')
            if status_filter == 'assigned':
                domain = [
                    ('status', '=', 'assigned'),
                    ('collector_id', '=', user.partner_id.id),
                ]

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

    @http.route('/api/cyclex/collector/accept-order/<int:request_id>', type='http', auth='public', methods=['POST'], csrf=False)
    def accept_order(self, request_id, **kwargs):
        try:
            user, error = self._authenticate(required_user_type='collector')
            if error:
                return error

            env = self._env_as_user(user)
            req = env['cyclex.request'].browse(request_id)
            if not req.exists():
                return self._error('Order not found', code='not_found', status=404)
            if req.status != 'pending':
                return self._error('Order is not available for acceptance', code='invalid_status')

            req.action_assign_collector(user.partner_id.id)
            return self._success(
                self._serialize_request(req, include_qr=True),
                message='Order accepted successfully',
            )
        except ValidationError as exc:
            return self._error(str(exc), code='validation_error')
        except Exception as exc:
            return self._handle_exception(exc)

    @http.route('/api/cyclex/collector/reject-order/<int:request_id>', type='http', auth='public', methods=['POST'], csrf=False)
    def reject_order(self, request_id, **kwargs):
        try:
            user, error = self._authenticate(required_user_type='collector')
            if error:
                return error

            env = self._env_as_user(user)
            req = env['cyclex.request'].browse(request_id)
            if not req.exists():
                return self._error('Order not found', code='not_found', status=404)
            if req.collector_id != user.partner_id:
                return self._error('Access denied', code='forbidden', status=403)

            req.action_reject_by_collector()
            return self._success(
                self._serialize_request(req),
                message='Order rejected successfully',
            )
        except ValidationError as exc:
            return self._error(str(exc), code='validation_error')
        except Exception as exc:
            return self._handle_exception(exc)

    @http.route('/api/cyclex/collector/scan-qr', type='http', auth='public', methods=['POST'], csrf=False)
    def scan_qr(self, **kwargs):
        try:
            user, error = self._authenticate(required_user_type='collector')
            if error:
                return error

            params = self._get_params()
            qr_code = params.get('qr_code')
            if not qr_code:
                return self._error('QR code is required', code='missing_fields')

            env = self._env_as_user(user)
            req = env['cyclex.request'].search([('qr_code', '=', qr_code)], limit=1)
            if not req:
                return self._error('Invalid QR code', code='invalid_qr', status=404)

            if req.collector_id and req.collector_id != user.partner_id:
                return self._error(
                    'This order is assigned to another collector',
                    code='forbidden',
                    status=403,
                )

            return self._success({
                'valid': True,
                'request': self._serialize_request(req, include_qr=True),
            })
        except Exception as exc:
            return self._handle_exception(exc)

    @http.route('/api/cyclex/collector/complete-order/<int:request_id>', type='http', auth='public', methods=['POST'], csrf=False)
    def complete_order(self, request_id, **kwargs):
        try:
            user, error = self._authenticate(required_user_type='collector')
            if error:
                return error

            env = self._env_as_user(user)
            req = env['cyclex.request'].browse(request_id)
            if not req.exists():
                return self._error('Order not found', code='not_found', status=404)
            if req.collector_id != user.partner_id:
                return self._error('Access denied', code='forbidden', status=403)

            req.action_mark_collected()
            return self._success(
                self._serialize_request(req),
                message='Order completed successfully',
            )
        except ValidationError as exc:
            return self._error(str(exc), code='validation_error')
        except Exception as exc:
            return self._handle_exception(exc)
