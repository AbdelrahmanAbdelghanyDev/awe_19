# -*- coding: utf-8 -*-
from odoo import http

# class CostEstimationAccounting(http.Controller):
#     @http.route('/cost_estimation_accounting/cost_estimation_accounting/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/cost_estimation_accounting/cost_estimation_accounting/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('cost_estimation_accounting.listing', {
#             'root': '/cost_estimation_accounting/cost_estimation_accounting',
#             'objects': http.request.env['cost_estimation_accounting.cost_estimation_accounting'].search([]),
#         })

#     @http.route('/cost_estimation_accounting/cost_estimation_accounting/objects/<model("cost_estimation_accounting.cost_estimation_accounting"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('cost_estimation_accounting.object', {
#             'object': obj
#         })