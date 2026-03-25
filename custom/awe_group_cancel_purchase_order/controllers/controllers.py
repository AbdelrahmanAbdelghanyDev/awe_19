# -*- coding: utf-8 -*-
from odoo import http

# class AweGroupCancelPurchaseOrder(http.Controller):
#     @http.route('/awe_group_cancel_purchase_order/awe_group_cancel_purchase_order/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/awe_group_cancel_purchase_order/awe_group_cancel_purchase_order/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('awe_group_cancel_purchase_order.listing', {
#             'root': '/awe_group_cancel_purchase_order/awe_group_cancel_purchase_order',
#             'objects': http.request.env['awe_group_cancel_purchase_order.awe_group_cancel_purchase_order'].search([]),
#         })

#     @http.route('/awe_group_cancel_purchase_order/awe_group_cancel_purchase_order/objects/<model("awe_group_cancel_purchase_order.awe_group_cancel_purchase_order"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('awe_group_cancel_purchase_order.object', {
#             'object': obj
#         })