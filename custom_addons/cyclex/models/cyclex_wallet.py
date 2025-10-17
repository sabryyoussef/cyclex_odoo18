# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class CyclexWallet(models.Model):
    _name = 'cyclex.wallet'
    _description = 'CycleX Customer Wallet'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    user_id = fields.Many2one(
        'res.partner',
        string='Customer',
        required=True,
        domain=[('cyclex_user_type', '=', 'customer')],
        ondelete='cascade'
    )
    
    balance = fields.Monetary(
        string='Current Balance',
        compute='_compute_balance',
        store=True,
        currency_field='currency_id',
        tracking=True
    )
    
    total_earned = fields.Monetary(
        string='Total Earned',
        compute='_compute_totals',
        store=True,
        currency_field='currency_id'
    )
    
    total_withdrawn = fields.Monetary(
        string='Total Withdrawn',
        compute='_compute_totals',
        store=True,
        currency_field='currency_id'
    )
    
    withdrawal_threshold = fields.Monetary(
        string='Withdrawal Threshold',
        default=1000.0,
        currency_field='currency_id',
        help="Minimum amount required for withdrawal"
    )
    
    status = fields.Selection([
        ('active', 'Active'),
        ('frozen', 'Frozen'),
    ], string='Status', default='active', tracking=True)
    
    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        default=lambda self: self.env.company.currency_id
    )
    
    transaction_ids = fields.One2many(
        'cyclex.wallet.transaction',
        'wallet_id',
        string='Transactions'
    )
    
    @api.depends('transaction_ids', 'transaction_ids.amount')
    def _compute_balance(self):
        for wallet in self:
            wallet.balance = sum(wallet.transaction_ids.mapped('amount'))
    
    @api.depends('transaction_ids', 'transaction_ids.amount', 'transaction_ids.transaction_type')
    def _compute_totals(self):
        for wallet in self:
            credits = wallet.transaction_ids.filtered(lambda t: t.transaction_type == 'credit')
            debits = wallet.transaction_ids.filtered(lambda t: t.transaction_type == 'debit')
            wallet.total_earned = sum(credits.mapped('amount'))
            wallet.total_withdrawn = abs(sum(debits.mapped('amount')))
    
    _sql_constraints = [
        ('user_unique', 'unique(user_id)',
         'Each customer can have only one wallet!')
    ]


class CyclexWalletTransaction(models.Model):
    _name = 'cyclex.wallet.transaction'
    _description = 'CycleX Wallet Transaction'
    _order = 'transaction_date desc'

    wallet_id = fields.Many2one(
        'cyclex.wallet',
        string='Wallet',
        required=True,
        ondelete='cascade'
    )
    
    request_id = fields.Many2one(
        'cyclex.request',
        string='Request/Order',
        ondelete='set null'
    )
    
    amount = fields.Monetary(
        string='Amount',
        required=True,
        currency_field='currency_id'
    )
    
    transaction_type = fields.Selection([
        ('credit', 'Credit'),
        ('debit', 'Debit'),
    ], string='Type', required=True)
    
    description = fields.Char(
        string='Description',
        required=True
    )
    
    transaction_date = fields.Datetime(
        string='Transaction Date',
        default=fields.Datetime.now,
        required=True
    )
    
    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        default=lambda self: self.env.company.currency_id
    )

