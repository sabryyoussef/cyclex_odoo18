# -*- coding: utf-8 -*-

import base64
import json
import logging

from odoo import fields, http
from odoo.exceptions import AccessDenied, UserError, ValidationError
from odoo.http import request

_logger = logging.getLogger(__name__)


class CycleXApiBase(http.Controller):
    """Shared helpers for CycleX REST API controllers."""

    # -------------------------------------------------------------------------
    # Request / response helpers
    # -------------------------------------------------------------------------

    def _get_json_body(self):
        if not request.httprequest.data:
            return {}
        try:
            return json.loads(request.httprequest.data.decode('utf-8'))
        except (json.JSONDecodeError, UnicodeDecodeError):
            return {}

    def _get_params(self):
        body = self._get_json_body()
        if body:
            return body
        return dict(request.params)

    def _json_response(self, data, status=200):
        return request.make_json_response(data, status=status)

    def _success(self, data=None, message='Success', status=200):
        payload = {'status': True, 'message': message}
        if data is not None:
            payload['data'] = data
        return self._json_response(payload, status=status)

    def _error(self, message, code='error', status=400, data=None):
        payload = {'status': False, 'message': message, 'code': code}
        if data is not None:
            payload['data'] = data
        return self._json_response(payload, status=status)

    def _handle_exception(self, exc):
        if isinstance(exc, (ValidationError, UserError)):
            return self._error(str(exc), code='validation_error', status=400)
        if isinstance(exc, AccessDenied):
            return self._error(str(exc), code='access_denied', status=403)
        _logger.exception('CycleX API error')
        return self._error('Internal server error', code='server_error', status=500)

    # -------------------------------------------------------------------------
    # Authentication helpers
    # -------------------------------------------------------------------------

    def _extract_bearer_token(self):
        auth_header = request.httprequest.headers.get('Authorization', '')
        if auth_header.startswith('Bearer '):
            return auth_header[7:].strip()
        params = self._get_params()
        return params.get('token') or request.params.get('token')

    def _authenticate(self, required_user_type=None):
        token = self._extract_bearer_token()
        user = request.env['cyclex.api.token'].sudo().get_user_from_token(token)
        if not user:
            return None, self._error(
                'Invalid or expired authentication token',
                code='unauthorized',
                status=401,
            )

        partner = user.partner_id
        if partner.account_status in ('suspended', 'banned'):
            return None, self._error(
                'Account is suspended or banned',
                code='account_suspended',
                status=403,
            )
        if required_user_type and partner.cyclex_user_type != required_user_type:
            return None, self._error(
                'You do not have permission to access this resource',
                code='forbidden',
                status=403,
            )
        if required_user_type == 'collector' and partner.collector_approval_status != 'approved':
            return None, self._error(
                'Collector account is not approved yet',
                code='collector_not_approved',
                status=403,
            )
        return user, None

    def _env_as_user(self, user):
        return request.env(user=user)

    def _authenticate_credentials(self, phone, password):
        db = request.db
        credential = {'login': phone, 'password': password, 'type': 'password'}
        try:
            auth_info = request.session.authenticate(db, credential)
            uid = auth_info.get('uid') if isinstance(auth_info, dict) else auth_info
            if not uid:
                return None
            user = request.env['res.users'].sudo().browse(uid)
            if not user.partner_id.is_cyclex_user:
                return None
            return user
        except AccessDenied:
            return None

    # -------------------------------------------------------------------------
    # Serialization helpers
    # -------------------------------------------------------------------------

    def _image_to_base64(self, image_field):
        if not image_field:
            return False
        if isinstance(image_field, bytes):
            return base64.b64encode(image_field).decode('utf-8')
        return image_field

    def _decode_image(self, image_data):
        if not image_data:
            return False
        if isinstance(image_data, str) and image_data.startswith('data:'):
            image_data = image_data.split(',', 1)[1]
        return image_data

    def _serialize_partner(self, partner):
        return {
            'id': partner.id,
            'name': partner.name,
            'phone': partner.phone,
            'user_type': partner.cyclex_user_type,
            'phone_verified': partner.phone_verified,
            'account_status': partner.account_status,
            'preferred_language': partner.preferred_language,
            'gps_latitude': partner.gps_latitude,
            'gps_longitude': partner.gps_longitude,
            'average_rating': partner.average_rating,
            'total_requests_created': partner.total_requests_created,
            'total_requests_completed': partner.total_requests_completed,
            'collector_approval_status': partner.collector_approval_status,
            'working_area_ids': partner.working_area_ids.ids,
        }

    def _serialize_category(self, category, include_children=False):
        data = {
            'id': category.id,
            'name': category.name,
            'parent_id': category.parent_id.id if category.parent_id else False,
            'description': category.description or '',
            'product_count': category.product_count,
            'image': self._image_to_base64(category.image),
        }
        if include_children:
            data['children'] = [
                self._serialize_category(child)
                for child in category.child_ids.filtered('active')
            ]
        return data

    def _serialize_product(self, product):
        return {
            'id': product.id,
            'name': product.name,
            'category_id': product.category_id.id,
            'category_name': product.category_id.name,
            'description': product.description or '',
            'price_per_kg': product.price_per_kg,
            'currency': product.currency_id.name,
            'image': self._image_to_base64(product.image),
        }

    def _serialize_request(self, req, include_qr=False):
        data = {
            'id': req.id,
            'name': req.name,
            'status': req.status,
            'customer_id': req.customer_id.id,
            'customer_name': req.customer_id.name,
            'collector_id': req.collector_id.id if req.collector_id else False,
            'collector_name': req.collector_id.name if req.collector_id else False,
            'category_id': req.category_id.id,
            'category_name': req.category_id.name,
            'product_id': req.product_id.id,
            'product_name': req.product_id.name,
            'quantity': req.quantity,
            'weight': req.weight,
            'calculated_price': req.calculated_price,
            'currency': req.currency_id.name,
            'pickup_date': fields.Date.to_string(req.pickup_date),
            'gps_latitude': req.gps_latitude,
            'gps_longitude': req.gps_longitude,
            'rating': req.rating,
            'comments': req.comments or '',
            'create_date': fields.Datetime.to_string(req.create_date),
            'completion_date': fields.Datetime.to_string(req.completion_date) if req.completion_date else False,
            'completion_deadline': fields.Datetime.to_string(req.completion_deadline) if req.completion_deadline else False,
            'has_photo_1': bool(req.photo_1),
            'has_photo_2': bool(req.photo_2),
        }
        if include_qr:
            data['qr_code'] = req.qr_code
        return data

    def _serialize_transaction(self, transaction):
        return {
            'id': transaction.id,
            'amount': transaction.amount,
            'transaction_type': transaction.transaction_type,
            'description': transaction.description,
            'transaction_date': fields.Datetime.to_string(transaction.transaction_date),
            'request_id': transaction.request_id.id if transaction.request_id else False,
        }

    def _serialize_working_area(self, area):
        return {
            'id': area.id,
            'name': area.name,
            'governorate': area.governorate,
            'description': area.description or '',
        }

    def _paginate(self, model, domain, serializer, page=1, limit=20, order=None):
        page = max(int(page or 1), 1)
        limit = min(max(int(limit or 20), 1), 100)
        offset = (page - 1) * limit
        total = model.search_count(domain)
        records = model.search(domain, limit=limit, offset=offset, order=order)
        return {
            'items': [serializer(record) for record in records],
            'pagination': {
                'page': page,
                'limit': limit,
                'total': total,
                'pages': (total + limit - 1) // limit if limit else 0,
            },
        }

    # -------------------------------------------------------------------------
    # User management helpers
    # -------------------------------------------------------------------------

    def _normalize_phone(self, phone):
        return (phone or '').strip().replace(' ', '')

    def _send_verification_sms(self, partner, code):
        """Placeholder for SMS Misr integration (Phase 4)."""
        _logger.info(
            'CycleX verification code for %s: %s',
            partner.phone,
            code,
        )
        return True

    def _create_cyclex_user(self, vals, user_type='customer'):
        Partner = request.env['res.partner'].sudo()
        Users = request.env['res.users'].sudo()

        phone = self._normalize_phone(vals.get('phone'))
        if not phone:
            raise ValidationError('Phone number is required.')

        existing = Partner.search([
            ('phone', '=', phone),
            ('is_cyclex_user', '=', True),
        ], limit=1)
        if existing:
            raise ValidationError('This phone number is already registered.')

        partner_vals = {
            'name': vals.get('name'),
            'phone': phone,
            'cyclex_user_type': user_type,
            'preferred_language': vals.get('language', 'en'),
            'fcm_token': vals.get('fcm_token'),
        }
        if user_type == 'collector':
            partner_vals.update({
                'collector_id_number': vals.get('id_number'),
                'collector_vehicle_type': vals.get('vehicle_type'),
                'collector_approval_status': 'pending',
            })
            if vals.get('working_area_ids'):
                partner_vals['working_area_ids'] = [(6, 0, vals['working_area_ids'])]

        partner = Partner.create_cyclex_user(partner_vals)

        group_xml_id = (
            'cyclex.group_cyclex_collector'
            if user_type == 'collector'
            else 'cyclex.group_cyclex_customer'
        )
        group = request.env.ref(group_xml_id)

        user = Users.create({
            'name': vals.get('name'),
            'login': phone,
            'password': vals.get('password'),
            'partner_id': partner.id,
            'groups_id': [(6, 0, [group.id])],
        })

        if user_type == 'customer':
            request.env['cyclex.wallet'].sudo().create_wallet_for_customer(partner.id)

        return partner, user

    def _issue_auth_response(self, user, message='Success'):
        token_record = request.env['cyclex.api.token'].sudo().create_token_for_user(user)
        user.partner_id.update_last_login()
        return self._success({
            'token': token_record.token,
            'expires_at': fields.Datetime.to_string(token_record.expiry_date),
            'user': self._serialize_partner(user.partner_id),
        }, message=message)
