# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class CyclexCategory(models.Model):
    _name = 'cyclex.category'
    _description = 'CycleX Product Category'
    _parent_name = 'parent_id'
    _parent_store = True
    _order = 'parent_path, name'

    name = fields.Char(
        string='Category Name',
        required=True,
        translate=True
    )
    
    parent_id = fields.Many2one(
        'cyclex.category',
        string='Parent Category',
        index=True,
        ondelete='cascade'
    )
    
    parent_path = fields.Char(index=True, unaccent=False)
    
    child_ids = fields.One2many(
        'cyclex.category',
        'parent_id',
        string='Child Categories'
    )
    
    description = fields.Text(
        string='Description',
        translate=True
    )
    
    image = fields.Image(
        string='Image',
        max_width=256,
        max_height=256
    )
    
    active = fields.Boolean(
        string='Active',
        default=True
    )
    
    product_count = fields.Integer(
        string='Number of Products',
        compute='_compute_product_count',
        store=True
    )
    
    @api.depends('child_ids')
    def _compute_product_count(self):
        # Placeholder - will be implemented in Phase 1.3
        for category in self:
            category.product_count = 0
    
    def name_get(self):
        result = []
        for category in self:
            if category.parent_id:
                name = f"{category.parent_id.name} / {category.name}"
            else:
                name = category.name
            result.append((category.id, name))
        return result
    
    _sql_constraints = [
        ('name_unique', 'unique(name, parent_id)',
         'Category name must be unique within the same parent!')
    ]

