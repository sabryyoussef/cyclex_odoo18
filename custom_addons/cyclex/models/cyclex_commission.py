# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


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
        tracking=True
    )
    
    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        default=lambda self: self.env.company.currency_id
    )
    
    @api.depends('order_value', 'commission_rate')
    def _compute_commission_amount(self):
        for commission in self:
            commission.commission_amount = (commission.order_value * commission.commission_rate) / 100

