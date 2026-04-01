# -*- coding: utf-8 -*-
# from odoo import http


# class AwePurchaseFix(http.Controller):
#     @http.route('/awe_purchase_fix/awe_purchase_fix', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/awe_purchase_fix/awe_purchase_fix/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('awe_purchase_fix.listing', {
#             'root': '/awe_purchase_fix/awe_purchase_fix',
#             'objects': http.request.env['awe_purchase_fix.awe_purchase_fix'].search([]),
#         })

#     @http.route('/awe_purchase_fix/awe_purchase_fix/objects/<model("awe_purchase_fix.awe_purchase_fix"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('awe_purchase_fix.object', {
#             'object': obj
#         })
