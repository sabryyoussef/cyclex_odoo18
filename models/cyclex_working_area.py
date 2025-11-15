# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class CyclexWorkingArea(models.Model):
    _name = 'cyclex.working.area'
    _description = 'CycleX Working Area'
    _order = 'governorate, name'

    name = fields.Char(
        string='Area Name',
        required=True,
        translate=True,
        help="Name of the city or district"
    )
    
    governorate = fields.Char(
        string='Governorate',
        required=True,
        translate=True,
        help="Governorate or province"
    )
    
    description = fields.Text(
        string='Description',
        translate=True
    )
    
    active = fields.Boolean(
        string='Active',
        default=True
    )
    
    collector_ids = fields.Many2many(
        'res.partner',
        'partner_working_area_rel',
        'area_id',
        'partner_id',
        string='Collectors',
        domain=[('cyclex_user_type', '=', 'collector')]
    )
    
    collector_count = fields.Integer(
        string='Number of Collectors',
        compute='_compute_collector_count',
        store=True
    )
    
    # GPS boundaries (optional for future geo-fencing)
    center_latitude = fields.Float(
        string='Center Latitude',
        digits=(10, 7)
    )
    
    center_longitude = fields.Float(
        string='Center Longitude',
        digits=(10, 7)
    )
    
    radius_km = fields.Float(
        string='Radius (km)',
        help="Approximate radius of coverage area"
    )
    
    @api.depends('collector_ids')
    def _compute_collector_count(self):
        for area in self:
            area.collector_count = len(area.collector_ids)
    
    def name_get(self):
        result = []
        for area in self:
            name = f"{area.name}, {area.governorate}"
            result.append((area.id, name))
        return result
    
    _sql_constraints = [
        ('name_governorate_unique', 'unique(name, governorate)',
         'This area already exists in the governorate!')
    ]

