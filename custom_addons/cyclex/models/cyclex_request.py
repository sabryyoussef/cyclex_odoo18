# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import uuid
from datetime import datetime, timedelta


class CyclexRequest(models.Model):
    _name = 'cyclex.request'
    _description = 'CycleX Recycling Request'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc'

    name = fields.Char(
        string='Request Number',
        required=True,
        copy=False,
        readonly=True,
        index=True,
        default=lambda self: _('New')
    )
    
    customer_id = fields.Many2one(
        'res.partner',
        string='Customer',
        required=True,
        domain=[('cyclex_user_type', '=', 'customer')],
        tracking=True
    )
    
    collector_id = fields.Many2one(
        'res.partner',
        string='Collector',
        domain=[('cyclex_user_type', '=', 'collector')],
        tracking=True
    )
    
    category_id = fields.Many2one(
        'cyclex.category',
        string='Category',
        required=True
    )
    
    product_id = fields.Many2one(
        'cyclex.product',
        string='Product',
        required=True,
        domain="[('category_id', '=', category_id)]"
    )
    
    quantity = fields.Integer(
        string='Quantity',
        required=True,
        default=1
    )
    
    weight = fields.Float(
        string='Weight (KG)',
        required=True,
        digits=(10, 2)
    )
    
    calculated_price = fields.Monetary(
        string='Calculated Price',
        compute='_compute_calculated_price',
        store=True,
        currency_field='currency_id'
    )
    
    status = fields.Selection([
        ('draft', 'Draft'),
        ('pending', 'Pending'),
        ('assigned', 'Assigned'),
        ('collected', 'Collected'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft', required=True, tracking=True)
    
    pickup_date = fields.Date(
        string='Pickup Date',
        required=True
    )
    
    photo_1 = fields.Binary(
        string='Photo 1',
        attachment=True
    )
    
    photo_2 = fields.Binary(
        string='Photo 2',
        attachment=True
    )
    
    qr_code = fields.Char(
        string='QR Code',
        copy=False,
        index=True
    )
    
    rating = fields.Selection([
        ('1', '1 - Poor'),
        ('2', '2 - Fair'),
        ('3', '3 - Good'),
        ('4', '4 - Very Good'),
        ('5', '5 - Excellent'),
    ], string='Rating')
    
    comments = fields.Text(
        string='Customer Comments'
    )
    
    # GPS Location (from customer at request time)
    gps_latitude = fields.Float(
        string='GPS Latitude',
        digits=(10, 7),
        help="Customer's latitude when creating the request"
    )
    
    gps_longitude = fields.Float(
        string='GPS Longitude',
        digits=(10, 7),
        help="Customer's longitude when creating the request"
    )
    
    # Dates
    create_date = fields.Datetime(
        string='Creation Date',
        readonly=True,
        index=True
    )
    
    completion_date = fields.Datetime(
        string='Completion Date',
        readonly=True,
        tracking=True
    )

    completion_deadline = fields.Datetime(
        string='Completion Deadline',
        readonly=True,
        tracking=True,
        help='Deadline for the collector to complete the order after acceptance',
    )
    
    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        default=lambda self: self.env.company.currency_id
    )
    
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env.company
    )
    
    @api.depends('weight', 'product_id', 'product_id.price_per_kg')
    def _compute_calculated_price(self):
        for request in self:
            if request.product_id and request.weight:
                request.calculated_price = request.weight * request.product_id.price_per_kg
            else:
                request.calculated_price = 0.0
    
    @api.model
    def create(self, vals):
        # Generate sequence number
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('cyclex.request') or _('New')
        
        # Generate unique QR code
        if not vals.get('qr_code'):
            vals['qr_code'] = self._generate_qr_code()
        
        # Get customer's GPS location if available
        if vals.get('customer_id') and not vals.get('gps_latitude'):
            customer = self.env['res.partner'].browse(vals['customer_id'])
            if customer.gps_latitude and customer.gps_longitude:
                vals['gps_latitude'] = customer.gps_latitude
                vals['gps_longitude'] = customer.gps_longitude
        
        return super(CyclexRequest, self).create(vals)
    
    def _generate_qr_code(self):
        """Generate a unique QR code for the request"""
        return str(uuid.uuid4())
    
    # ==========================================
    # Business Methods
    # ==========================================
    
    def action_submit(self):
        """Submit request (draft -> pending)"""
        self.ensure_one()
        if self.status != 'draft':
            raise ValidationError(_('Only draft requests can be submitted.'))
        self.write({'status': 'pending'})
        return True
    
    def action_assign_collector(self, collector_id):
        """Assign collector to request (pending -> assigned)"""
        self.ensure_one()
        if self.status != 'pending':
            raise ValidationError(_('Only pending requests can be assigned.'))
        deadline_days = int(self.env['ir.config_parameter'].sudo().get_param(
            'cyclex.completion_deadline_days', '3'
        ))
        self.write({
            'status': 'assigned',
            'collector_id': collector_id,
            'completion_deadline': fields.Datetime.now() + timedelta(days=deadline_days),
        })
        # TODO: Send notification to collector
        return True

    def action_reject_by_collector(self):
        """Revert an assigned order back to pending when collector rejects it."""
        self.ensure_one()
        if self.status != 'assigned':
            raise ValidationError(_('Only assigned requests can be rejected by collector.'))
        self.write({
            'status': 'pending',
            'collector_id': False,
            'completion_deadline': False,
        })
        return True
    
    def action_mark_collected(self):
        """Mark request as collected (assigned -> collected)"""
        self.ensure_one()
        if self.status != 'assigned':
            raise ValidationError(_('Only assigned requests can be marked as collected.'))
        
        # Update request status
        self.write({
            'status': 'collected',
            'completion_date': fields.Datetime.now()
        })
        
        # Create wallet transaction for customer
        self._create_wallet_transaction()
        
        # Create commission record for collector
        self._create_commission_record()
        
        # TODO: Send notification to customer
        # TODO: Send notification to collector
        return True
    
    def _create_wallet_transaction(self):
        """Create wallet transaction when request is collected"""
        self.ensure_one()
        Wallet = self.env['cyclex.wallet'].sudo()
        wallet = Wallet.search([('user_id', '=', self.customer_id.id)], limit=1)
        if not wallet:
            wallet = Wallet.create_wallet_for_customer(self.customer_id.id)

        description = _('Payment for request %s - %s kg of %s') % (
            self.name,
            self.weight,
            self.product_id.name
        )
        wallet.add_credit(
            amount=self.calculated_price,
            description=description,
            request_id=self.id
        )
        return wallet

    def _create_commission_record(self):
        """Create commission record when request is collected"""
        self.ensure_one()
        if not self.collector_id:
            return None
        return self.env['cyclex.commission'].sudo().create_commission_for_request(self)
    
    def action_cancel(self):
        """Cancel the request"""
        self.ensure_one()
        if self.status == 'collected':
            raise ValidationError(_('Collected requests cannot be cancelled.'))
        self.write({'status': 'cancelled'})
        return True
    
    @api.constrains('weight')
    def _check_weight(self):
        """Validate weight is positive"""
        for request in self:
            if request.weight <= 0:
                raise ValidationError(_('Weight must be greater than zero.'))
    
    @api.constrains('quantity')
    def _check_quantity(self):
        """Validate quantity is positive"""
        for request in self:
            if request.quantity <= 0:
                raise ValidationError(_('Quantity must be greater than zero.'))
    
    @api.constrains('pickup_date')
    def _check_pickup_date(self):
        """Validate pickup date is not in the past"""
        for request in self:
            if request.pickup_date and request.pickup_date < fields.Date.today():
                raise ValidationError(_('Pickup date cannot be in the past.'))

