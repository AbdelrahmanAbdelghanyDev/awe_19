# -*- coding: utf-8 -*-
from odoo import http

# class AdditionDeductionSegmatek(http.Controller):
#     @http.route('/addition_deduction_segmatek/addition_deduction_segmatek/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/addition_deduction_segmatek/addition_deduction_segmatek/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('addition_deduction_segmatek.listing', {
#             'root': '/addition_deduction_segmatek/addition_deduction_segmatek',
#             'objects': http.request.env['addition_deduction_segmatek.addition_deduction_segmatek'].search([]),
#         })

#     @http.route('/addition_deduction_segmatek/addition_deduction_segmatek/objects/<model("addition_deduction_segmatek.addition_deduction_segmatek"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('addition_deduction_segmatek.object', {
#             'object': obj
#         })