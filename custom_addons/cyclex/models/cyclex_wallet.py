# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError


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
    
    # ==========================================
    # Business Methods
    # ==========================================
    
    @api.model
    def create_wallet_for_customer(self, customer_id):
        """Create a wallet for a customer if it doesn't exist"""
        existing = self.search([('user_id', '=', customer_id)], limit=1)
        if existing:
            return existing
        
        customer = self.env['res.partner'].browse(customer_id)
        if customer.cyclex_user_type != 'customer':
            raise ValidationError(_('Wallets can only be created for customers.'))
        
        return self.create({
            'user_id': customer_id,
            'status': 'active'
        })
    
    def add_credit(self, amount, description, request_id=None):
        """Add credit to wallet (earnings from recycling)"""
        self.ensure_one()
        
        if self.status != 'active':
            raise UserError(_('Cannot add credit to frozen wallet.'))
        
        if amount <= 0:
            raise ValidationError(_('Credit amount must be positive.'))
        
        # Create transaction
        transaction = self.env['cyclex.wallet.transaction'].create({
            'wallet_id': self.id,
            'request_id': request_id,
            'amount': amount,
            'transaction_type': 'credit',
            'description': description,
        })
        
        return transaction
    
    def add_debit(self, amount, description):
        """Debit from wallet (withdrawal)"""
        self.ensure_one()
        
        if self.status != 'active':
            raise UserError(_('Cannot debit from frozen wallet.'))
        
        if amount <= 0:
            raise ValidationError(_('Debit amount must be positive.'))
        
        if amount > self.balance:
            raise UserError(_('Insufficient balance. Available: %s') % self.balance)
        
        # Create transaction (amount is negative for debit)
        transaction = self.env['cyclex.wallet.transaction'].create({
            'wallet_id': self.id,
            'amount': -amount,
            'transaction_type': 'debit',
            'description': description,
        })
        
        return transaction
    
    def action_request_withdrawal(self):
        """Request withdrawal of wallet balance"""
        self.ensure_one()
        
        if self.status != 'active':
            raise UserError(_('Cannot withdraw from frozen wallet.'))
        
        if self.balance < self.withdrawal_threshold:
            raise UserError(
                _('Minimum withdrawal amount is %s. Current balance: %s') 
                % (self.withdrawal_threshold, self.balance)
            )
        
        # Return wizard to confirm withdrawal
        return {
            'name': _('Request Withdrawal'),
            'type': 'ir.actions.act_window',
            'res_model': 'cyclex.wallet.withdrawal.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_wallet_id': self.id,
                'default_amount': self.balance
            }
        }
    
    def action_freeze_wallet(self):
        """Freeze wallet (admin action)"""
        self.ensure_one()
        self.write({'status': 'frozen'})
        # TODO: Send notification to customer
        return True
    
    def action_activate_wallet(self):
        """Activate frozen wallet (admin action)"""
        self.ensure_one()
        self.write({'status': 'active'})
        # TODO: Send notification to customer
        return True
    
    def action_view_transactions(self):
        """View wallet transactions"""
        self.ensure_one()
        return {
            'name': _('Wallet Transactions'),
            'type': 'ir.actions.act_window',
            'res_model': 'cyclex.wallet.transaction',
            'view_mode': 'tree,form',
            'domain': [('wallet_id', '=', self.id)],
            'context': {'default_wallet_id': self.id}
        }


class CyclexWalletTransaction(models.Model):
    _name = 'cyclex.wallet.transaction'
    _description = 'CycleX Wallet Transaction'
    _order = 'transaction_date desc'

    wallet_id = fields.Many2one(
        'cyclex.wallet',
        string='Wallet',
        required=True,
        ondelete='cascade',
        index=True
    )
    
    customer_id = fields.Many2one(
        'res.partner',
        string='Customer',
        related='wallet_id.user_id',
        store=True,
        readonly=True
    )
    
    request_id = fields.Many2one(
        'cyclex.request',
        string='Request/Order',
        ondelete='set null',
        index=True
    )
    
    amount = fields.Monetary(
        string='Amount',
        required=True,
        currency_field='currency_id',
        help="Positive for credit, negative for debit"
    )
    
    transaction_type = fields.Selection([
        ('credit', 'Credit'),
        ('debit', 'Debit'),
    ], string='Type', required=True, index=True)
    
    description = fields.Char(
        string='Description',
        required=True
    )
    
    transaction_date = fields.Datetime(
        string='Transaction Date',
        default=fields.Datetime.now,
        required=True,
        index=True
    )
    
    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        default=lambda self: self.env.company.currency_id
    )
    
    # ==========================================
    # Validation
    # ==========================================
    
    @api.constrains('amount', 'transaction_type')
    def _check_amount_sign(self):
        """Validate amount sign matches transaction type"""
        for transaction in self:
            if transaction.transaction_type == 'credit' and transaction.amount < 0:
                raise ValidationError(_('Credit transactions must have positive amounts.'))
            if transaction.transaction_type == 'debit' and transaction.amount > 0:
                raise ValidationError(_('Debit transactions must have negative amounts.'))

