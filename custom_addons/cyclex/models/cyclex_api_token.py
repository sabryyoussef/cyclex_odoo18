# -*- coding: utf-8 -*-

import secrets
import uuid
from datetime import timedelta

from odoo import api, fields, models


class CyclexApiToken(models.Model):
    _name = 'cyclex.api.token'
    _description = 'CycleX API Authentication Token'
    _order = 'create_date desc'

    name = fields.Char(string='Label', default='Mobile App Token')
    user_id = fields.Many2one(
        'res.users',
        string='User',
        required=True,
        ondelete='cascade',
        index=True,
    )
    partner_id = fields.Many2one(
        'res.partner',
        string='Partner',
        related='user_id.partner_id',
        store=True,
        readonly=True,
    )
    token = fields.Char(
        string='Token',
        required=True,
        index=True,
        copy=False,
        default=lambda self: str(uuid.uuid4()),
    )
    expiry_date = fields.Datetime(string='Expiry Date')
    active = fields.Boolean(default=True)
    last_used = fields.Datetime(string='Last Used')

    _sql_constraints = [
        ('token_unique', 'unique(token)', 'API token must be unique!'),
    ]

    @api.model
    def _token_lifetime_days(self):
        return int(
            self.env['ir.config_parameter'].sudo().get_param(
                'cyclex.api_token_lifetime_days', '30'
            )
        )

    @api.model
    def create_token_for_user(self, user):
        """Create a new API token and deactivate previous tokens for the user."""
        self.search([('user_id', '=', user.id), ('active', '=', True)]).write(
            {'active': False}
        )
        return self.create({
            'user_id': user.id,
            'token': secrets.token_urlsafe(32),
            'expiry_date': fields.Datetime.now() + timedelta(
                days=self._token_lifetime_days()
            ),
            'active': True,
        })

    @api.model
    def get_user_from_token(self, token):
        """Validate token and return the associated user."""
        if not token:
            return self.env['res.users']
        record = self.sudo().search([
            ('token', '=', token),
            ('active', '=', True),
        ], limit=1)
        if not record:
            return self.env['res.users']
        if record.expiry_date and record.expiry_date < fields.Datetime.now():
            record.write({'active': False})
            return self.env['res.users']
        record.write({'last_used': fields.Datetime.now()})
        return record.user_id

    @api.model
    def revoke_user_tokens(self, user):
        self.search([('user_id', '=', user.id), ('active', '=', True)]).write(
            {'active': False}
        )
