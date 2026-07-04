# -*- coding: utf-8 -*-

from odoo import http
from odoo.exceptions import ValidationError, UserError
from odoo.http import request

from .api_base import CycleXApiBase


class CycleXWalletController(CycleXApiBase):
    """Wallet API endpoints."""

    def _get_customer_wallet(self, env, partner):
        wallet = env['cyclex.wallet'].search([('user_id', '=', partner.id)], limit=1)
        if not wallet:
            wallet = env['cyclex.wallet'].sudo().create_wallet_for_customer(partner.id)
        return wallet

    @http.route('/api/cyclex/wallet/balance', type='http', auth='public', methods=['GET'], csrf=False)
    def wallet_balance(self, **kwargs):
        try:
            user, error = self._authenticate(required_user_type='customer')
            if error:
                return error

            env = self._env_as_user(user)
            wallet = self._get_customer_wallet(env, user.partner_id)

            return self._success({
                'balance': wallet.balance,
                'total_earned': wallet.total_earned,
                'total_withdrawn': wallet.total_withdrawn,
                'withdrawable_amount': wallet.balance,
                'withdrawal_threshold': wallet.withdrawal_threshold,
                'currency': wallet.currency_id.name,
                'status': wallet.status,
            })
        except Exception as exc:
            return self._handle_exception(exc)

    @http.route('/api/cyclex/wallet/transactions', type='http', auth='public', methods=['GET'], csrf=False)
    def wallet_transactions(self, **kwargs):
        try:
            user, error = self._authenticate(required_user_type='customer')
            if error:
                return error

            params = self._get_params()
            env = self._env_as_user(user)
            wallet = self._get_customer_wallet(env, user.partner_id)

            result = self._paginate(
                env['cyclex.wallet.transaction'],
                [('wallet_id', '=', wallet.id)],
                self._serialize_transaction,
                page=params.get('page', 1),
                limit=params.get('limit', 20),
                order='transaction_date desc',
            )
            return self._success(result)
        except Exception as exc:
            return self._handle_exception(exc)

    @http.route('/api/cyclex/wallet/withdraw', type='http', auth='public', methods=['POST'], csrf=False)
    def wallet_withdraw(self, **kwargs):
        try:
            user, error = self._authenticate(required_user_type='customer')
            if error:
                return error

            params = self._get_params()
            amount = params.get('amount')
            if not amount:
                return self._error('Withdrawal amount is required', code='missing_fields')

            amount = float(amount)
            env = self._env_as_user(user)
            wallet = self._get_customer_wallet(env, user.partner_id)

            if amount < wallet.withdrawal_threshold:
                return self._error(
                    'Minimum withdrawal amount is %s' % wallet.withdrawal_threshold,
                    code='below_threshold',
                )
            if amount > wallet.balance:
                return self._error('Insufficient balance', code='insufficient_balance')

            transaction = wallet.sudo().add_debit(
                amount,
                'Withdrawal request via mobile app',
            )
            return self._success({
                'transaction': self._serialize_transaction(transaction),
                'balance': wallet.balance,
            }, message='Withdrawal processed successfully')
        except (ValidationError, UserError) as exc:
            return self._error(str(exc), code='validation_error')
        except Exception as exc:
            return self._handle_exception(exc)
