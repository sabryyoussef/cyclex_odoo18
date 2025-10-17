# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError


class CyclexCommission(models.Model):
    _name = 'cyclex.commission'
    _description = 'CycleX Collector Commission'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc'

    collector_id = fields.Many2one(
        'res.partner',
        string='Collector',
        required=True,
        domain=[('cyclex_user_type', '=', 'collector')],
        ondelete='cascade',
        tracking=True
    )
    
    request_id = fields.Many2one(
        'cyclex.request',
        string='Request/Order',
        required=True,
        ondelete='cascade'
    )
    
    order_value = fields.Monetary(
        string='Order Value',
        required=True,
        currency_field='currency_id'
    )
    
    commission_rate = fields.Float(
        string='Commission Rate (%)',
        required=True,
        digits=(5, 2)
    )
    
    commission_amount = fields.Monetary(
        string='Commission Amount',
        compute='_compute_commission_amount',
        store=True,
        currency_field='currency_id'
    )
    
    status = fields.Selection([
        ('pending', 'Pending'),
        ('paid', 'Paid'),
    ], string='Status', default='pending', tracking=True)
    
    payment_date = fields.Date(
        string='Payment Date',
        tracking=True,
        readonly=True
    )
    
    create_date = fields.Datetime(
        string='Creation Date',
        readonly=True,
        index=True
    )
    
    customer_id = fields.Many2one(
        'res.partner',
        string='Customer',
        related='request_id.customer_id',
        store=True,
        readonly=True
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
    
    notes = fields.Text(
        string='Notes'
    )
    
    @api.depends('order_value', 'commission_rate')
    def _compute_commission_amount(self):
        for commission in self:
            commission.commission_amount = (commission.order_value * commission.commission_rate) / 100
    
    # ==========================================
    # Business Methods
    # ==========================================
    
    @api.model
    def create_commission_for_request(self, request):
        """Create commission record when request is collected"""
        if not request.collector_id:
            raise ValidationError(_('Cannot create commission without assigned collector.'))
        
        # Check if commission already exists
        existing = self.search([('request_id', '=', request.id)], limit=1)
        if existing:
            raise ValidationError(_('Commission already exists for this request.'))
        
        # Create commission
        commission = self.create({
            'collector_id': request.collector_id.id,
            'request_id': request.id,
            'order_value': request.calculated_price,
            'commission_rate': request.collector_id.collector_commission_rate,
            'status': 'pending',
        })
        
        return commission
    
    def action_mark_paid(self):
        """Mark commission as paid"""
        self.ensure_one()
        
        if self.status != 'pending':
            raise UserError(_('Only pending commissions can be marked as paid.'))
        
        self.write({
            'status': 'paid',
            'payment_date': fields.Date.today()
        })
        
        # TODO: Send notification to collector
        return True
    
    def action_mark_pending(self):
        """Revert commission to pending (undo payment)"""
        self.ensure_one()
        
        if self.status != 'paid':
            raise UserError(_('Only paid commissions can be reverted to pending.'))
        
        self.write({
            'status': 'pending',
            'payment_date': False
        })
        
        return True
    
    # ==========================================
    # Validation
    # ==========================================
    
    @api.constrains('order_value')
    def _check_order_value(self):
        """Validate order value is positive"""
        for commission in self:
            if commission.order_value <= 0:
                raise ValidationError(_('Order value must be greater than zero.'))
    
    @api.constrains('commission_rate')
    def _check_commission_rate(self):
        """Validate commission rate is between 0 and 100"""
        for commission in self:
            if commission.commission_rate < 0 or commission.commission_rate > 100:
                raise ValidationError(_('Commission rate must be between 0 and 100.'))
    
    _sql_constraints = [
        ('request_unique', 'unique(request_id)',
         'Commission already exists for this request!')
    ]

