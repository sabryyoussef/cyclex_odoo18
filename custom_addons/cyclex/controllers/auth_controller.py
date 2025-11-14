# -*- coding: utf-8 -*-

import json
import logging
import re
from odoo import http, _
from odoo.http import request
from odoo.exceptions import ValidationError, UserError

_logger = logging.getLogger(__name__)


class CyclexAuthController(http.Controller):
    """
    Authentication API Controller for CycleX Mobile App
    Handles login, registration, and phone verification
    """
    
    @http.route('/api/cyclex/login', type='http', auth='public', methods=['POST'], csrf=False)
    def login(self, **kwargs):
        """
        User login with phone number and password
        
        Expected params:
        - phone: Phone number
        - password: Password
        - fcm_token: (Optional) Firebase Cloud Messaging token
        
        Returns:
        - success: True/False
        - message: Status message
        - data: User profile and auth token
        """
        try:
            # Parse JSON body
            data = json.loads(request.httprequest.data.decode('utf-8'))
            phone = data.get('phone')
            password = data.get('password')
            fcm_token = data.get('fcm_token')
            
            if not phone or not password:
                return request.make_json_response({
                    'success': False,
                    'message': _('Phone number and password are required'),
                    'error_code': 'MISSING_PARAMS'
                })
            
            # Find user by phone
            partner = request.env['res.partner'].sudo().search([
                ('phone', '=', phone),
                ('is_cyclex_user', '=', True)
            ], limit=1)
            
            if not partner:
                return request.make_json_response({
                    'success': False,
                    'message': _('Invalid phone number or password'),
                    'error_code': 'INVALID_CREDENTIALS'
                })
            
            # Check if phone is verified
            if not partner.phone_verified:
                return request.make_json_response({
                    'success': False,
                    'message': _('Phone number not verified. Please verify your account.'),
                    'error_code': 'PHONE_NOT_VERIFIED',
                    'data': {
                        'user_id': partner.id,
                        'phone': partner.phone
                    }
                })
            
            # Check account status
            if partner.account_status != 'active':
                return request.make_json_response({
                    'success': False,
                    'message': _('Account is %s. Please contact support.') % partner.account_status,
                    'error_code': 'ACCOUNT_SUSPENDED'
                })
            
            # Verify password
            user = request.env['res.users'].sudo().search([
                ('partner_id', '=', partner.id)
            ], limit=1)
            
            if user:
                # Verify password using Odoo's authentication
                try:
                    uid = request.session.authenticate(request.db, user.login, password)
                    if not uid:
                        return request.make_json_response({
                            'success': False,
                            'message': _('Invalid phone number or password'),
                            'error_code': 'INVALID_CREDENTIALS'
                        })
                except Exception as e:
                    return request.make_json_response({
                        'success': False,
                        'message': _('Invalid phone number or password'),
                        'error_code': 'INVALID_CREDENTIALS'
                    })
            else:
                # For partners without user accounts (API-only users)
                # You may want to implement custom password verification here
                pass
            
            # Update FCM token if provided
            if fcm_token:
                partner.sudo().write({'fcm_token': fcm_token})
            
            # Update last login
            partner.sudo().update_last_login()
            
            # Generate response with user data
            return request.make_json_response({
                'success': True,
                'message': _('Login successful'),
                'data': {
                    'user_id': partner.id,
                    'name': partner.name,
                    'phone': partner.phone,
                    'email': partner.email or '',
                    'user_type': partner.cyclex_user_type,
                    'language': partner.preferred_language,
                    'account_status': partner.account_status,
                    'verified': partner.phone_verified,
                    # Customer specific
                    'total_requests': partner.total_requests_created if partner.cyclex_user_type == 'customer' else 0,
                    'total_earnings': partner.total_earnings if partner.cyclex_user_type == 'customer' else 0,
                    # Collector specific
                    'collector_status': partner.collector_approval_status if partner.cyclex_user_type == 'collector' else None,
                    'total_orders': partner.total_requests_completed if partner.cyclex_user_type == 'collector' else 0,
                    'average_rating': partner.average_rating if partner.cyclex_user_type == 'collector' else 0,
                }
            })
            
        except Exception as e:
            _logger.error(f"Login error: {str(e)}")
            return request.make_json_response({
                'success': False,
                'message': _('An error occurred during login'),
                'error_code': 'SERVER_ERROR'
            })
    
    @http.route('/api/cyclex/register', type='http', auth='public', methods=['POST'], csrf=False)
    def register(self, **kwargs):
        """
        Register new user (customer or collector)
        
        Expected params:
        - name: Full name
        - phone: Phone number
        - password: Password
        - confirm_password: Confirm password
        - user_type: 'customer' or 'collector'
        - fcm_token: (Optional) Firebase token
        - language: (Optional) 'en' or 'ar'
        
        For collectors, additional params:
        - id_number: National ID
        - vehicle_type: Type of vehicle
        - working_area_ids: List of working area IDs
        
        Returns:
        - success: True/False
        - message: Status message
        - data: User ID and verification info
        """
        try:
            # Parse JSON body
            data = json.loads(request.httprequest.data.decode('utf-8'))
            name = data.get('name')
            phone = data.get('phone')
            password = data.get('password')
            confirm_password = data.get('confirm_password')
            user_type = data.get('user_type', 'customer')
            fcm_token = data.get('fcm_token')
            language = data.get('language', 'en')
            
            # Validation
            if not all([name, phone, password, confirm_password]):
                return request.make_json_response({
                    'success': False,
                    'message': _('Name, phone, password, and confirm password are required'),
                    'error_code': 'MISSING_PARAMS'
                })
            
            if password != confirm_password:
                return request.make_json_response({
                    'success': False,
                    'message': _('Passwords do not match'),
                    'error_code': 'PASSWORD_MISMATCH'
                })
            
            # Password strength validation
            password_validation = self._validate_password_strength(password)
            if not password_validation['valid']:
                return request.make_json_response({
                    'success': False,
                    'message': password_validation['message'],
                    'error_code': 'WEAK_PASSWORD'
                })
            
            if user_type not in ['customer', 'collector']:
                return request.make_json_response({
                    'success': False,
                    'message': _('Invalid user type'),
                    'error_code': 'INVALID_USER_TYPE'
                })
            
            # Check if phone already exists
            existing = request.env['res.partner'].sudo().search([
                ('phone', '=', phone),
                ('is_cyclex_user', '=', True)
            ], limit=1)
            
            if existing:
                return request.make_json_response({
                    'success': False,
                    'message': _('Phone number already registered'),
                    'error_code': 'PHONE_EXISTS'
                })
            
            # Prepare partner values
            partner_vals = {
                'name': name,
                'phone': phone,
                'cyclex_user_type': user_type,
                'preferred_language': language,
                'fcm_token': fcm_token or False,
                'account_status': 'inactive',  # Will be active after verification
                'phone_verified': False,
                'customer_rank': 1 if user_type == 'customer' else 0,
            }
            
            # Add collector-specific fields
            if user_type == 'collector':
                partner_vals.update({
                    'collector_id_number': data.get('id_number'),
                    'collector_vehicle_type': data.get('vehicle_type'),
                    'collector_approval_status': 'pending',
                })
                
                working_areas = data.get('working_area_ids', [])
                if working_areas:
                    partner_vals['working_area_ids'] = [(6, 0, working_areas)]
            
            # Create partner
            partner = request.env['res.partner'].sudo().create(partner_vals)
            
            # Create user account for authentication
            user_vals = {
                'name': name,
                'login': phone,  # Use phone as login
                'password': password,
                'partner_id': partner.id,
                'groups_id': [(6, 0, [request.env.ref('cyclex.group_cyclex_customer').id])]
            }
            
            if user_type == 'collector':
                user_vals['groups_id'] = [(6, 0, [request.env.ref('cyclex.group_cyclex_collector').id])]
            
            user = request.env['res.users'].sudo().create(user_vals)
            
            # Generate and send verification code
            verification_code = partner.generate_verification_code()
            
            # TODO: Send SMS via SMS Misr
            # For now, return the code in the response (remove in production)
            _logger.info(f"Verification code for {phone}: {verification_code}")
            
            return request.make_json_response({
                'success': True,
                'message': _('Registration successful. Please verify your phone number.'),
                'data': {
                    'user_id': partner.id,
                    'phone': phone,
                    'name': name,
                    'user_type': user_type,
                    'verification_code': verification_code,  # TODO: Remove in production
                    'verification_sent': True
                }
            })
            
        except ValidationError as e:
            return request.make_json_response({
                'success': False,
                'message': str(e),
                'error_code': 'VALIDATION_ERROR'
            })
        except Exception as e:
            _logger.error(f"Registration error: {str(e)}")
            return request.make_json_response({
                'success': False,
                'message': _('An error occurred during registration'),
                'error_code': 'SERVER_ERROR'
            })
    
    @http.route('/api/cyclex/verify', type='http', auth='public', methods=['POST'], csrf=False)
    def verify(self, **kwargs):
        """
        Verify phone number with code
        
        Expected params:
        - phone: Phone number
        - verification_code: 6-digit code
        
        Returns:
        - success: True/False
        - message: Status message
        - data: User profile
        """
        try:
            # Parse JSON body
            data = json.loads(request.httprequest.data.decode('utf-8'))
            phone = data.get('phone')
            code = data.get('verification_code')
            
            if not phone or not code:
                return request.make_json_response({
                    'success': False,
                    'message': _('Phone number and verification code are required'),
                    'error_code': 'MISSING_PARAMS'
                })
            
            # Find user
            partner = request.env['res.partner'].sudo().search([
                ('phone', '=', phone),
                ('is_cyclex_user', '=', True)
            ], limit=1)
            
            if not partner:
                return request.make_json_response({
                    'success': False,
                    'message': _('User not found'),
                    'error_code': 'USER_NOT_FOUND'
                })
            
            if partner.phone_verified:
                return request.make_json_response({
                    'success': False,
                    'message': _('Phone number already verified'),
                    'error_code': 'ALREADY_VERIFIED'
                })
            
            # Verify code
            if partner.verify_code(code):
                # Auto-login after verification
                user = request.env['res.users'].sudo().search([
                    ('partner_id', '=', partner.id)
                ], limit=1)
                
                if user:
                    try:
                        request.session.authenticate(request.db, user.login, data.get('password', ''))
                    except:
                        pass
                
                return request.make_json_response({
                    'success': True,
                    'message': _('Phone verified successfully'),
                    'data': {
                        'user_id': partner.id,
                        'name': partner.name,
                        'phone': partner.phone,
                        'user_type': partner.cyclex_user_type,
                        'account_status': partner.account_status,
                        'verified': True
                    }
                })
            else:
                return request.make_json_response({
                    'success': False,
                    'message': _('Invalid or expired verification code'),
                    'error_code': 'INVALID_CODE'
                })
                
        except Exception as e:
            _logger.error(f"Verification error: {str(e)}")
            return request.make_json_response({
                'success': False,
                'message': _('An error occurred during verification'),
                'error_code': 'SERVER_ERROR'
            })
    
    @http.route('/api/cyclex/resend-code', type='http', auth='public', methods=['POST'], csrf=False)
    def resend_code(self, **kwargs):
        """
        Resend verification code
        
        Expected params:
        - phone: Phone number
        
        Returns:
        - success: True/False
        - message: Status message
        """
        try:
            # Parse JSON body
            data = json.loads(request.httprequest.data.decode('utf-8'))
            phone = data.get('phone')
            
            if not phone:
                return request.make_json_response({
                    'success': False,
                    'message': _('Phone number is required'),
                    'error_code': 'MISSING_PARAMS'
                })
            
            # Find user
            partner = request.env['res.partner'].sudo().search([
                ('phone', '=', phone),
                ('is_cyclex_user', '=', True)
            ], limit=1)
            
            if not partner:
                return request.make_json_response({
                    'success': False,
                    'message': _('User not found'),
                    'error_code': 'USER_NOT_FOUND'
                })
            
            if partner.phone_verified:
                return request.make_json_response({
                    'success': False,
                    'message': _('Phone number already verified'),
                    'error_code': 'ALREADY_VERIFIED'
                })
            
            # Generate new code
            verification_code = partner.generate_verification_code()
            
            # TODO: Send SMS via SMS Misr
            _logger.info(f"Resent verification code for {phone}: {verification_code}")
            
            return request.make_json_response({
                'success': True,
                'message': _('Verification code sent successfully'),
                'data': {
                    'verification_code': verification_code,  # TODO: Remove in production
                    'phone': phone
                }
            })
            
        except Exception as e:
            _logger.error(f"Resend code error: {str(e)}")
            return request.make_json_response({
                'success': False,
                'message': _('An error occurred while resending code'),
                'error_code': 'SERVER_ERROR'
            })
    
    @http.route('/api/cyclex/profile', type='http', auth='user', methods=['GET'], csrf=False)
    def get_profile(self, **kwargs):
        """
        Get current user profile
        
        Returns:
        - success: True/False
        - data: User profile
        """
        try:
            partner = request.env.user.partner_id
            
            if not partner.is_cyclex_user:
                return request.make_json_response({
                    'success': False,
                    'message': _('Not a CycleX user'),
                    'error_code': 'NOT_CYCLEX_USER'
                })
            
            return request.make_json_response({
                'success': True,
                'data': {
                    'user_id': partner.id,
                    'name': partner.name,
                    'phone': partner.phone,
                    'email': partner.email or '',
                    'user_type': partner.cyclex_user_type,
                    'language': partner.preferred_language,
                    'account_status': partner.account_status,
                    'verified': partner.phone_verified,
                    'gps_latitude': partner.gps_latitude,
                    'gps_longitude': partner.gps_longitude,
                    # Customer data
                    'total_requests': partner.total_requests_created if partner.cyclex_user_type == 'customer' else 0,
                    'total_earnings': partner.total_earnings if partner.cyclex_user_type == 'customer' else 0,
                    # Collector data
                    'collector_status': partner.collector_approval_status if partner.cyclex_user_type == 'collector' else None,
                    'total_orders': partner.total_requests_completed if partner.cyclex_user_type == 'collector' else 0,
                    'average_rating': partner.average_rating if partner.cyclex_user_type == 'collector' else 0,
                    'commission_rate': partner.collector_commission_rate if partner.cyclex_user_type == 'collector' else 0,
                }
            })
            
        except Exception as e:
            _logger.error(f"Get profile error: {str(e)}")
            return request.make_json_response({
                'success': False,
                'message': _('An error occurred while fetching profile'),
                'error_code': 'SERVER_ERROR'
            })
    
    @http.route('/api/cyclex/update-profile', type='http', auth='user', methods=['POST'], csrf=False)
    def update_profile(self, **kwargs):
        """
        Update user profile
        
        Expected params:
        - name: (Optional) Name
        - email: (Optional) Email
        - language: (Optional) Preferred language
        - fcm_token: (Optional) FCM token
        - gps_latitude: (Optional) GPS latitude
        - gps_longitude: (Optional) GPS longitude
        
        Returns:
        - success: True/False
        - message: Status message
        """
        try:
            # Parse JSON body
            data = json.loads(request.httprequest.data.decode('utf-8'))
            partner = request.env.user.partner_id
            
            if not partner.is_cyclex_user:
                return request.make_json_response({
                    'success': False,
                    'message': _('Not a CycleX user'),
                    'error_code': 'NOT_CYCLEX_USER'
                })
            
            # Prepare update values
            vals = {}
            
            if 'name' in data and data['name']:
                vals['name'] = data['name']
            
            if 'email' in data:
                vals['email'] = data['email']
            
            if 'language' in data and data['language'] in ['en', 'ar']:
                vals['preferred_language'] = data['language']
            
            if 'fcm_token' in data:
                vals['fcm_token'] = data['fcm_token']
            
            if 'gps_latitude' in data and 'gps_longitude' in data:
                partner.update_gps_location(data['gps_latitude'], data['gps_longitude'])
            
            if vals:
                partner.sudo().write(vals)
            
            return request.make_json_response({
                'success': True,
                'message': _('Profile updated successfully'),
                'data': {
                    'user_id': partner.id,
                    'name': partner.name
                }
            })
            
        except ValidationError as e:
            return request.make_json_response({
                'success': False,
                'message': str(e),
                'error_code': 'VALIDATION_ERROR'
            })
        except Exception as e:
            _logger.error(f"Update profile error: {str(e)}")
            return request.make_json_response({
                'success': False,
                'message': _('An error occurred while updating profile'),
                'error_code': 'SERVER_ERROR'
            })
    
    # ==========================================
    # Helper Methods
    # ==========================================
    
    def _validate_password_strength(self, password):
        """
        Validate password strength
        Requirements:
        - Minimum 8 characters
        - At least one uppercase letter
        - At least one lowercase letter
        - At least one number
        """
        if len(password) < 8:
            return {
                'valid': False,
                'message': _('Password must be at least 8 characters long')
            }
        
        if not re.search(r'[A-Z]', password):
            return {
                'valid': False,
                'message': _('Password must contain at least one uppercase letter')
            }
        
        if not re.search(r'[a-z]', password):
            return {
                'valid': False,
                'message': _('Password must contain at least one lowercase letter')
            }
        
        if not re.search(r'\d', password):
            return {
                'valid': False,
                'message': _('Password must contain at least one number')
            }
        
        return {'valid': True}

