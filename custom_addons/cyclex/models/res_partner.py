# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import random
import string
from datetime import datetime, timedelta


class ResPartner(models.Model):
    _inherit = 'res.partner'

    # ==========================================
    # User Type & Authentication Fields
    # ==========================================
    
    cyclex_user_type = fields.Selection([
        ('customer', 'Customer'),
        ('collector', 'Collector'),
    ], string='CycleX User Type', tracking=True,
       help="Type of CycleX user: Customer (sells items) or Collector (picks up items)")
    
    is_cyclex_user = fields.Boolean(
        string='Is CycleX User',
        compute='_compute_is_cyclex_user',
        store=True,
        help="Indicates if this partner is a CycleX user"
    )
    
    # Phone Authentication (primary login method)
    phone_verified = fields.Boolean(
        string='Phone Verified',
        default=False,
        tracking=True,
        help="Indicates if the phone number has been verified via SMS"
    )
    
    verification_code = fields.Char(
        string='Verification Code',
        size=6,
        help="6-digit verification code sent via SMS"
    )
    
    verification_code_expiry = fields.Datetime(
        string='Verification Code Expiry',
        help="Expiry time for the verification code"
    )
    
    last_verification_sent = fields.Datetime(
        string='Last Verification Sent',
        help="Timestamp of last verification code sent"
    )
    
    # ==========================================
    # Mobile App Fields
    # ==========================================
    
    fcm_token = fields.Char(
        string='FCM Token',
        help="Firebase Cloud Messaging token for push notifications"
    )
    
    preferred_language = fields.Selection([
        ('en', 'English'),
        ('ar', 'Arabic'),
    ], string='Preferred Language', default='en',
       help="User's preferred language for app and notifications")
    
    # ==========================================
    # Location Fields
    # ==========================================
    
    gps_latitude = fields.Float(
        string='GPS Latitude',
        digits=(10, 7),
        help="GPS latitude coordinate for user's location"
    )
    
    gps_longitude = fields.Float(
        string='GPS Longitude',
        digits=(10, 7),
        help="GPS longitude coordinate for user's location"
    )
    
    location_last_updated = fields.Datetime(
        string='Location Last Updated',
        help="Timestamp when GPS coordinates were last updated"
    )
    
    # ==========================================
    # Collector-Specific Fields
    # ==========================================
    
    collector_id_number = fields.Char(
        string='ID Number',
        help="National ID or identification number for collector"
    )
    
    collector_vehicle_type = fields.Selection([
        ('bicycle', 'Bicycle'),
        ('motorcycle', 'Motorcycle'),
        ('car', 'Car'),
        ('van', 'Van'),
        ('truck', 'Truck'),
    ], string='Vehicle Type',
       help="Type of vehicle used by collector")
    
    collector_approval_status = fields.Selection([
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('suspended', 'Suspended'),
    ], string='Collector Status', default='pending', tracking=True,
       help="Approval status for collector registration")
    
    collector_approval_date = fields.Date(
        string='Approval Date',
        tracking=True,
        help="Date when collector was approved"
    )
    
    collector_approved_by = fields.Many2one(
        'res.users',
        string='Approved By',
        tracking=True,
        help="User who approved the collector"
    )
    
    collector_rejection_reason = fields.Text(
        string='Rejection Reason',
        help="Reason for rejecting collector registration"
    )
    
    working_area_ids = fields.Many2many(
        'cyclex.working.area',
        'partner_working_area_rel',
        'partner_id',
        'area_id',
        string='Working Areas',
        help="Areas where the collector operates (max 5)"
    )
    
    working_area_count = fields.Integer(
        string='Working Areas Count',
        compute='_compute_working_area_count',
        store=True
    )
    
    collector_commission_rate = fields.Float(
        string='Commission Rate (%)',
        default=5.0,
        digits=(5, 2),
        help="Commission percentage for this collector"
    )
    
    # ==========================================
    # Statistics & Performance Fields
    # ==========================================
    
    total_requests_created = fields.Integer(
        string='Total Requests Created',
        compute='_compute_request_statistics',
        store=True,
        help="Total number of requests created by customer"
    )
    
    total_requests_completed = fields.Integer(
        string='Total Requests Completed',
        compute='_compute_request_statistics',
        store=True,
        help="Total number of requests completed by collector"
    )
    
    average_rating = fields.Float(
        string='Average Rating',
        compute='_compute_average_rating',
        store=True,
        digits=(2, 1),
        help="Average rating from customers"
    )
    
    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        compute='_compute_currency_id',
        store=True,
        help="Currency for monetary fields"
    )
    
    total_earnings = fields.Monetary(
        string='Total Earnings',
        compute='_compute_wallet_statistics',
        currency_field='currency_id',
        help="Total earnings for customer"
    )
    
    total_commissions = fields.Monetary(
        string='Total Commissions',
        compute='_compute_commission_statistics',
        currency_field='currency_id',
        help="Total commissions earned by collector"
    )
    
    # ==========================================
    # Account Status Fields
    # ==========================================
    
    account_status = fields.Selection([
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('suspended', 'Suspended'),
        ('banned', 'Banned'),
    ], string='Account Status', default='inactive', tracking=True,
       help="Status of the user account")
    
    suspension_reason = fields.Text(
        string='Suspension Reason',
        help="Reason for account suspension or ban"
    )
    
    suspension_date = fields.Datetime(
        string='Suspension Date',
        tracking=True
    )
    
    last_login_date = fields.Datetime(
        string='Last Login',
        help="Last login timestamp from mobile app"
    )
    
    registration_date = fields.Datetime(
        string='Registration Date',
        default=fields.Datetime.now,
        help="Date when user registered in CycleX"
    )
    
    # ==========================================
    # Computed Fields
    # ==========================================
    
    @api.depends('cyclex_user_type')
    def _compute_is_cyclex_user(self):
        for partner in self:
            partner.is_cyclex_user = bool(partner.cyclex_user_type)
    
    @api.depends('company_id')
    def _compute_currency_id(self):
        for partner in self:
            partner.currency_id = partner.company_id.currency_id or self.env.company.currency_id
    
    @api.depends('working_area_ids')
    def _compute_working_area_count(self):
        for partner in self:
            partner.working_area_count = len(partner.working_area_ids)
    
    @api.depends('cyclex_user_type')
    def _compute_request_statistics(self):
        Request = self.env['cyclex.request']
        for partner in self:
            if partner.cyclex_user_type == 'customer':
                partner.total_requests_created = Request.search_count([
                    ('customer_id', '=', partner.id)
                ])
                partner.total_requests_completed = 0
            elif partner.cyclex_user_type == 'collector':
                partner.total_requests_created = 0
                partner.total_requests_completed = Request.search_count([
                    ('collector_id', '=', partner.id),
                    ('status', '=', 'collected')
                ])
            else:
                partner.total_requests_created = 0
                partner.total_requests_completed = 0
    
    @api.depends('cyclex_user_type')
    def _compute_average_rating(self):
        Request = self.env['cyclex.request']
        for partner in self:
            if partner.cyclex_user_type == 'collector':
                requests = Request.search([
                    ('collector_id', '=', partner.id),
                    ('rating', '>', 0)
                ])
                if requests:
                    partner.average_rating = sum(requests.mapped('rating')) / len(requests)
                else:
                    partner.average_rating = 0.0
            else:
                partner.average_rating = 0.0
    
    def _compute_wallet_statistics(self):
        Wallet = self.env['cyclex.wallet']
        for partner in self:
            if partner.cyclex_user_type == 'customer':
                wallet = Wallet.search([('user_id', '=', partner.id)], limit=1)
                partner.total_earnings = wallet.total_earned if wallet else 0.0
            else:
                partner.total_earnings = 0.0
    
    def _compute_commission_statistics(self):
        Commission = self.env['cyclex.commission']
        for partner in self:
            if partner.cyclex_user_type == 'collector':
                commissions = Commission.search([('collector_id', '=', partner.id)])
                partner.total_commissions = sum(commissions.mapped('commission_amount'))
            else:
                partner.total_commissions = 0.0
    
    # ==========================================
    # Constraints
    # ==========================================
    
    @api.constrains('working_area_ids')
    def _check_working_area_limit(self):
        for partner in self:
            if partner.cyclex_user_type == 'collector' and len(partner.working_area_ids) > 5:
                raise ValidationError(_('A collector can have a maximum of 5 working areas.'))
    
    @api.constrains('phone')
    def _check_phone_unique(self):
        for partner in self:
            if partner.phone and partner.is_cyclex_user:
                duplicate = self.search([
                    ('phone', '=', partner.phone),
                    ('is_cyclex_user', '=', True),
                    ('id', '!=', partner.id)
                ], limit=1)
                if duplicate:
                    raise ValidationError(_('This phone number is already registered in CycleX.'))
    
    @api.constrains('gps_latitude', 'gps_longitude')
    def _check_gps_coordinates(self):
        for partner in self:
            if partner.gps_latitude:
                if not (-90 <= partner.gps_latitude <= 90):
                    raise ValidationError(_('Latitude must be between -90 and 90 degrees.'))
            if partner.gps_longitude:
                if not (-180 <= partner.gps_longitude <= 180):
                    raise ValidationError(_('Longitude must be between -180 and 180 degrees.'))
    
    @api.constrains('collector_commission_rate')
    def _check_commission_rate(self):
        for partner in self:
            if partner.cyclex_user_type == 'collector':
                if partner.collector_commission_rate < 0 or partner.collector_commission_rate > 100:
                    raise ValidationError(_('Commission rate must be between 0 and 100.'))
    
    # ==========================================
    # Business Methods
    # ==========================================
    
    def generate_verification_code(self):
        """Generate a 6-digit verification code"""
        self.ensure_one()
        code = ''.join(random.choices(string.digits, k=6))
        self.write({
            'verification_code': code,
            'verification_code_expiry': fields.Datetime.now() + timedelta(minutes=10),
            'last_verification_sent': fields.Datetime.now(),
        })
        return code
    
    def verify_code(self, code):
        """Verify the provided code"""
        self.ensure_one()
        if not self.verification_code:
            return False
        if self.verification_code_expiry < fields.Datetime.now():
            return False
        if self.verification_code == code:
            self.write({
                'phone_verified': True,
                'account_status': 'active',
                'verification_code': False,
                'verification_code_expiry': False,
            })
            return True
        return False
    
    def update_gps_location(self, latitude, longitude):
        """Update GPS coordinates"""
        self.ensure_one()
        self.write({
            'gps_latitude': latitude,
            'gps_longitude': longitude,
            'location_last_updated': fields.Datetime.now(),
        })
    
    def action_approve_collector(self):
        """Approve collector registration"""
        self.ensure_one()
        if self.cyclex_user_type != 'collector':
            raise ValidationError(_('Only collectors can be approved.'))
        self.write({
            'collector_approval_status': 'approved',
            'collector_approval_date': fields.Date.today(),
            'collector_approved_by': self.env.user.id,
            'account_status': 'active',
        })
        # TODO: Send notification to collector
        return True
    
    def action_reject_collector(self):
        """Reject collector registration"""
        self.ensure_one()
        if self.cyclex_user_type != 'collector':
            raise ValidationError(_('Only collectors can be rejected.'))
        return {
            'name': _('Reject Collector'),
            'type': 'ir.actions.act_window',
            'res_model': 'cyclex.collector.reject.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_collector_id': self.id}
        }
    
    def action_suspend_user(self):
        """Suspend user account"""
        self.ensure_one()
        return {
            'name': _('Suspend User'),
            'type': 'ir.actions.act_window',
            'res_model': 'cyclex.user.suspend.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_user_id': self.id}
        }
    
    def action_view_requests(self):
        """View user's requests"""
        self.ensure_one()
        if self.cyclex_user_type == 'customer':
            domain = [('customer_id', '=', self.id)]
        elif self.cyclex_user_type == 'collector':
            domain = [('collector_id', '=', self.id)]
        else:
            domain = []
        
        return {
            'name': _('Requests'),
            'type': 'ir.actions.act_window',
            'res_model': 'cyclex.request',
            'view_mode': 'tree,form',
            'domain': domain,
            'context': {'create': False}
        }
    
    def action_view_wallet(self):
        """View customer's wallet"""
        self.ensure_one()
        if self.cyclex_user_type != 'customer':
            raise ValidationError(_('Only customers have wallets.'))
        
        wallet = self.env['cyclex.wallet'].search([('user_id', '=', self.id)], limit=1)
        if not wallet:
            wallet = self.env['cyclex.wallet'].create({'user_id': self.id})
        
        return {
            'name': _('Wallet'),
            'type': 'ir.actions.act_window',
            'res_model': 'cyclex.wallet',
            'view_mode': 'form',
            'res_id': wallet.id,
            'target': 'current',
        }
    
    def action_view_commissions(self):
        """View collector's commissions"""
        self.ensure_one()
        if self.cyclex_user_type != 'collector':
            raise ValidationError(_('Only collectors have commissions.'))
        
        return {
            'name': _('Commissions'),
            'type': 'ir.actions.act_window',
            'res_model': 'cyclex.commission',
            'view_mode': 'tree,form',
            'domain': [('collector_id', '=', self.id)],
            'context': {'create': False}
        }
    
    def update_last_login(self):
        """Update last login timestamp"""
        self.ensure_one()
        self.write({'last_login_date': fields.Datetime.now()})
    
    @api.model
    def create_cyclex_user(self, vals):
        """Helper method to create a CycleX user with proper defaults"""
        if 'is_company' not in vals:
            vals['is_company'] = False
        if 'customer_rank' not in vals:
            vals['customer_rank'] = 1
        if 'registration_date' not in vals:
            vals['registration_date'] = fields.Datetime.now()
        if 'account_status' not in vals:
            vals['account_status'] = 'inactive'  # Will be active after verification
        
        return self.create(vals)


class ResUsers(models.Model):
    _inherit = 'res.users'
    
    cyclex_user_type = fields.Selection(
        related='partner_id.cyclex_user_type',
        readonly=False,
        store=True
    )
    
    is_cyclex_user = fields.Boolean(
        related='partner_id.is_cyclex_user',
        store=True
    )

