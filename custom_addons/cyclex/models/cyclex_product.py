# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class CyclexProduct(models.Model):
    _name = 'cyclex.product'
    _description = 'CycleX Recyclable Product'
    _order = 'category_id, name'

    name = fields.Char(
        string='Product Name',
        required=True,
        translate=True
    )
    
    category_id = fields.Many2one(
        'cyclex.category',
        string='Category',
        required=True,
        ondelete='restrict'
    )
    
    description = fields.Text(
        string='Description',
        translate=True
    )
    
    price_per_kg = fields.Float(
        string='Price per KG',
        required=True,
        digits=(12, 2),
        help="Price paid per kilogram in local currency"
    )
    
    image = fields.Image(
        string='Product Image',
        max_width=1024,
        max_height=1024
    )
    
    active = fields.Boolean(
        string='Active',
        default=True
    )
    
    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        default=lambda self: self.env.company.currency_id
    )
    
    request_count = fields.Integer(
        string='Request Count',
        compute='_compute_request_count',
        store=True
    )
    
    @api.depends('name')
    def _compute_request_count(self):
        # Placeholder - will be implemented in Phase 1.4
        for product in self:
            product.request_count = 0
    
    _sql_constraints = [
        ('name_category_unique', 'unique(name, category_id)',
         'Product name must be unique within the same category!')
    ]

