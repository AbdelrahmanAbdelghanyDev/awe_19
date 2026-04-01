# -*- coding: utf-8 -*-
# from odoo import http


# class AweStopConsDateInvoice(http.Controller):
#     @http.route('/awe_stop_cons_date_invoice/awe_stop_cons_date_invoice', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/awe_stop_cons_date_invoice/awe_stop_cons_date_invoice/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('awe_stop_cons_date_invoice.listing', {
#             'root': '/awe_stop_cons_date_invoice/awe_stop_cons_date_invoice',
#             'objects': http.request.env['awe_stop_cons_date_invoice.awe_stop_cons_date_invoice'].search([]),
#         })

#     @http.route('/awe_stop_cons_date_invoice/awe_stop_cons_date_invoice/objects/<model("awe_stop_cons_date_invoice.awe_stop_cons_date_invoice"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('awe_stop_cons_date_invoice.object', {
#             'object': obj
#         })
