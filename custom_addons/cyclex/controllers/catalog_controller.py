# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request

from .api_base import CycleXApiBase


class CycleXCatalogController(CycleXApiBase):
    """Categories and products API endpoints."""

    @http.route('/api/cyclex/categories', type='http', auth='public', methods=['GET'], csrf=False)
    def categories(self, **kwargs):
        try:
            params = self._get_params()
            Category = request.env['cyclex.category'].sudo()
            domain = [('active', '=', True)]

            parent_id = params.get('parent_id')
            if parent_id:
                domain.append(('parent_id', '=', int(parent_id)))
            elif params.get('root_only'):
                domain.append(('parent_id', '=', False))

            categories = Category.search(domain, order='name')
            include_children = str(params.get('include_children', 'false')).lower() == 'true'

            return self._success({
                'categories': [
                    self._serialize_category(category, include_children=include_children)
                    for category in categories
                ],
            })
        except Exception as exc:
            return self._handle_exception(exc)

    @http.route('/api/cyclex/products', type='http', auth='public', methods=['GET'], csrf=False)
    def products(self, **kwargs):
        try:
            params = self._get_params()
            Product = request.env['cyclex.product'].sudo()
            domain = [('active', '=', True)]

            category_id = params.get('category_id')
            if category_id:
                domain.append(('category_id', '=', int(category_id)))

            search_term = params.get('search')
            if search_term:
                domain.append(('name', 'ilike', search_term))

            page = params.get('page', 1)
            limit = params.get('limit', 20)

            result = self._paginate(
                Product,
                domain,
                self._serialize_product,
                page=page,
                limit=limit,
                order='category_id, name',
            )
            return self._success(result)
        except Exception as exc:
            return self._handle_exception(exc)
