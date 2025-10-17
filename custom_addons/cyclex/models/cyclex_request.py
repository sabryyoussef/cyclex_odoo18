# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


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
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('cyclex.request') or _('New')
        return super(CyclexRequest, self).create(vals)

