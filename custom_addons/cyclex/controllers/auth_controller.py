# -*- coding: utf-8 -*-

from odoo import http
from odoo.exceptions import ValidationError
from odoo.http import request

from .api_base import CycleXApiBase


class CycleXAuthController(CycleXApiBase):
    """Authentication and registration API endpoints."""

    @http.route('/api/cyclex/login', type='http', auth='public', methods=['POST'], csrf=False)
    def login(self, **kwargs):
        try:
            params = self._get_params()
            phone = self._normalize_phone(params.get('phone'))
            password = params.get('password')

            if not phone or not password:
                return self._error('Phone and password are required', code='missing_fields')

            user = self._authenticate_credentials(phone, password)
            if not user:
                return self._error('Invalid phone number or password', code='invalid_credentials', status=401)

            partner = user.partner_id
            if not partner.phone_verified:
                return self._error(
                    'Phone number is not verified',
                    code='phone_not_verified',
                    status=403,
                )
            if partner.account_status != 'active':
                return self._error(
                    'Account is not active',
                    code='account_inactive',
                    status=403,
                )

            if params.get('fcm_token'):
                partner.sudo().write({'fcm_token': params['fcm_token']})

            return self._issue_auth_response(user, message='Login successful')
        except Exception as exc:
            return self._handle_exception(exc)

    @http.route('/api/cyclex/register', type='http', auth='public', methods=['POST'], csrf=False)
    def register(self, **kwargs):
        try:
            params = self._get_params()
            required = ['name', 'phone', 'password', 'confirm_password']
            missing = [field for field in required if not params.get(field)]
            if missing:
                return self._error(
                    'Missing required fields: %s' % ', '.join(missing),
                    code='missing_fields',
                )

            if params['password'] != params['confirm_password']:
                return self._error('Passwords do not match', code='password_mismatch')

            if len(params['password']) < 6:
                return self._error(
                    'Password must be at least 6 characters',
                    code='weak_password',
                )

            partner, user = self._create_cyclex_user(params, user_type='customer')
            code = partner.generate_verification_code()
            self._send_verification_sms(partner, code)

            return self._success({
                'user_id': partner.id,
                'phone': partner.phone,
                'verification_required': True,
            }, message='Registration successful. Please verify your phone number.', status=201)
        except ValidationError as exc:
            return self._error(str(exc), code='validation_error')
        except Exception as exc:
            return self._handle_exception(exc)

    @http.route('/api/cyclex/verify', type='http', auth='public', methods=['POST'], csrf=False)
    def verify(self, **kwargs):
        try:
            params = self._get_params()
            phone = self._normalize_phone(params.get('phone'))
            code = params.get('verification_code')

            if not phone or not code:
                return self._error(
                    'Phone and verification code are required',
                    code='missing_fields',
                )

            partner = request.env['res.partner'].sudo().search([
                ('phone', '=', phone),
                ('is_cyclex_user', '=', True),
            ], limit=1)
            if not partner:
                return self._error('User not found', code='not_found', status=404)

            if not partner.verify_code(str(code).strip()):
                return self._error('Invalid or expired verification code', code='invalid_code')

            user = request.env['res.users'].sudo().search([
                ('partner_id', '=', partner.id),
            ], limit=1)
            if not user:
                return self._error('User account not found', code='not_found', status=404)

            return self._issue_auth_response(user, message='Phone verified successfully')
        except Exception as exc:
            return self._handle_exception(exc)

    @http.route('/api/cyclex/resend-code', type='http', auth='public', methods=['POST'], csrf=False)
    def resend_code(self, **kwargs):
        try:
            params = self._get_params()
            phone = self._normalize_phone(params.get('phone'))

            if not phone:
                return self._error('Phone number is required', code='missing_fields')

            partner = request.env['res.partner'].sudo().search([
                ('phone', '=', phone),
                ('is_cyclex_user', '=', True),
            ], limit=1)
            if not partner:
                return self._error('User not found', code='not_found', status=404)

            if partner.phone_verified:
                return self._error('Phone is already verified', code='already_verified')

            code = partner.generate_verification_code()
            self._send_verification_sms(partner, code)

            return self._success(message='Verification code sent successfully')
        except Exception as exc:
            return self._handle_exception(exc)
