# -*- coding: utf-8 -*-

import json
import logging
from odoo import http, _
from odoo.http import request
from odoo.exceptions import ValidationError, UserError

_logger = logging.getLogger(__name__)


class CyclexWalletController(http.Controller):
    """
    Wallet API Controller for CycleX Mobile App
    """
    
    @http.route('/api/cyclex/wallet/balance', type='http', auth='user', methods=['POST'], csrf=False)
    def get_balance(self, **kwargs):
        """
        Get current wallet balance
        
        Returns:
        - success: True/False
        - data: Balance, total earned, withdrawable amount
        """
        try:
            partner = request.env.user.partner_id
            
            # Validate user type
            if partner.cyclex_user_type != 'customer':
                return request.make_response(
                    json.dumps({
                        'success': False,
                        'message': _('Only customers have wallets'),
                        'error_code': 'INVALID_USER_TYPE'
                    }),
                    headers={'Content-Type': 'application/json'},
                    status=403
                )
            
            # Get or create wallet
            wallet = request.env['cyclex.wallet'].sudo().search([
                ('user_id', '=', partner.id)
            ], limit=1)
            
            if not wallet:
                wallet = request.env['cyclex.wallet'].sudo().create_wallet_for_customer(partner.id)
            
            return request.make_response(
                json.dumps({
                    'success': True,
                    'data': {
                        'balance': wallet.balance,
                        'total_earned': wallet.total_earned,
                        'total_withdrawn': wallet.total_withdrawn,
                        'withdrawal_threshold': wallet.withdrawal_threshold,
                        'can_withdraw': wallet.balance >= wallet.withdrawal_threshold,
                        'currency': wallet.currency_id.name,
                        'currency_symbol': wallet.currency_id.symbol,
                        'status': wallet.status,
                    }
                }),
                headers={'Content-Type': 'application/json'},
                status=200
            )
            
        except Exception as e:
            _logger.error(f"Get balance error: {str(e)}")
            return request.make_response(
                json.dumps({
                    'success': False,
                    'message': _('An error occurred while fetching balance'),
                    'error_code': 'SERVER_ERROR'
                }),
                headers={'Content-Type': 'application/json'},
                status=500
            )
    
    @http.route('/api/cyclex/wallet/transactions', type='http', auth='user', methods=['POST'], csrf=False)
    def get_transactions(self, **kwargs):
        """
        Get wallet transaction history
        
        Optional params:
        - transaction_type: 'credit' or 'debit'
        - limit: Number of results (default: 20)
        - offset: Pagination offset
        
        Returns:
        - success: True/False
        - data: List of transactions
        """
        try:
            # Handle both form data and JSON data
            if request.httprequest.content_type == 'application/json':
                data = json.loads(request.httprequest.data.decode('utf-8'))
            else:
                data = request.params
            
            partner = request.env.user.partner_id
            
            if partner.cyclex_user_type != 'customer':
                return request.make_response(
                    json.dumps({
                        'success': False,
                        'message': _('Only customers have wallets'),
                        'error_code': 'INVALID_USER_TYPE'
                    }),
                    headers={'Content-Type': 'application/json'},
                    status=403
                )
            
            # Get wallet
            wallet = request.env['cyclex.wallet'].sudo().search([
                ('user_id', '=', partner.id)
            ], limit=1)
            
            if not wallet:
                return request.make_response(
                    json.dumps({
                        'success': True,
                        'data': {
                            'transactions': [],
                            'total': 0
                        }
                    }),
                    headers={'Content-Type': 'application/json'},
                    status=200
                )
            
            # Get parameters
            transaction_type = data.get('transaction_type')
            limit = int(data.get('limit', 20))
            offset = int(data.get('offset', 0))
            
            # Build domain
            domain = [('wallet_id', '=', wallet.id)]
            if transaction_type:
                domain.append(('transaction_type', '=', transaction_type))
            
            # Search transactions
            transactions = request.env['cyclex.wallet.transaction'].sudo().search(
                domain,
                order='transaction_date desc',
                limit=limit,
                offset=offset
            )
            
            total_count = request.env['cyclex.wallet.transaction'].sudo().search_count(domain)
            
            # Format response
            transaction_list = []
            for trans in transactions:
                transaction_list.append({
                    'id': trans.id,
                    'amount': trans.amount,
                    'type': trans.transaction_type,
                    'description': trans.description,
                    'date': str(trans.transaction_date),
                    'request_number': trans.request_id.name if trans.request_id else None,
                })
            
            return request.make_response(
                json.dumps({
                    'success': True,
                    'data': {
                        'transactions': transaction_list,
                        'total': total_count,
                        'limit': limit,
                        'offset': offset
                    }
                }),
                headers={'Content-Type': 'application/json'},
                status=200
            )
            
        except Exception as e:
            _logger.error(f"Get transactions error: {str(e)}")
            return request.make_response(
                json.dumps({
                    'success': False,
                    'message': _('An error occurred while fetching transactions'),
                    'error_code': 'SERVER_ERROR'
                }),
                headers={'Content-Type': 'application/json'},
                status=500
            )
    
    @http.route('/api/cyclex/wallet/withdraw', type='http', auth='user', methods=['POST'], csrf=False)
    def request_withdrawal(self, **kwargs):
        """
        Request withdrawal from wallet
        
        Expected params:
        - amount: Amount to withdraw
        
        Returns:
        - success: True/False
        - message: Status message
        """
        try:
            # Handle both form data and JSON data
            if request.httprequest.content_type == 'application/json':
                data = json.loads(request.httprequest.data.decode('utf-8'))
            else:
                data = request.params
            
            partner = request.env.user.partner_id
            
            if partner.cyclex_user_type != 'customer':
                return request.make_response(
                    json.dumps({
                        'success': False,
                        'message': _('Only customers can withdraw'),
                        'error_code': 'INVALID_USER_TYPE'
                    }),
                    headers={'Content-Type': 'application/json'},
                    status=403
                )
            
            amount = float(data.get('amount', 0))
            
            if amount <= 0:
                return request.make_response(
                    json.dumps({
                        'success': False,
                        'message': _('Invalid amount'),
                        'error_code': 'INVALID_AMOUNT'
                    }),
                    headers={'Content-Type': 'application/json'},
                    status=400
                )
            
            # Get wallet
            wallet = request.env['cyclex.wallet'].sudo().search([
                ('user_id', '=', partner.id)
            ], limit=1)
            
            if not wallet:
                return request.make_response(
                    json.dumps({
                        'success': False,
                        'message': _('Wallet not found'),
                        'error_code': 'NOT_FOUND'
                    }),
                    headers={'Content-Type': 'application/json'},
                    status=404
                )
            
            # Validate withdrawal
            if wallet.balance < wallet.withdrawal_threshold:
                return request.make_response(
                    json.dumps({
                        'success': False,
                        'message': _('Minimum withdrawal amount is %s') % wallet.withdrawal_threshold,
                        'error_code': 'BELOW_THRESHOLD'
                    }),
                    headers={'Content-Type': 'application/json'},
                    status=400
                )
            
            if amount > wallet.balance:
                return request.make_response(
                    json.dumps({
                        'success': False,
                        'message': _('Insufficient balance'),
                        'error_code': 'INSUFFICIENT_BALANCE'
                    }),
                    headers={'Content-Type': 'application/json'},
                    status=400
                )
            
            # Create withdrawal transaction
            transaction = wallet.sudo().add_debit(
                amount,
                _('Withdrawal request - Pending approval')
            )
            
            # TODO: Create withdrawal request record for admin approval
            # TODO: Send notification to admin
            
            return request.make_response(
                json.dumps({
                    'success': True,
                    'message': _('Withdrawal request submitted successfully. Pending approval.'),
                    'data': {
                        'transaction_id': transaction.id,
                        'amount': amount,
                        'remaining_balance': wallet.balance,
                    }
                }),
                headers={'Content-Type': 'application/json'},
                status=200
            )
            
        except (ValidationError, UserError) as e:
            return request.make_response(
                json.dumps({
                    'success': False,
                    'message': str(e),
                    'error_code': 'VALIDATION_ERROR'
                }),
                headers={'Content-Type': 'application/json'},
                status=400
            )
        except Exception as e:
            _logger.error(f"Withdrawal error: {str(e)}")
            return request.make_response(
                json.dumps({
                    'success': False,
                    'message': _('An error occurred while processing withdrawal'),
                    'error_code': 'SERVER_ERROR'
                }),
                headers={'Content-Type': 'application/json'},
                status=500
            )

