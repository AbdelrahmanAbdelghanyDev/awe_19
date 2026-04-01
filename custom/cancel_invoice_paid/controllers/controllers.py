# -*- coding: utf-8 -*-
from odoo import http

# class CancelInvoicePaid(http.Controller):
#     @http.route('/cancel_invoice_paid/cancel_invoice_paid/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/cancel_invoice_paid/cancel_invoice_paid/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('cancel_invoice_paid.listing', {
#             'root': '/cancel_invoice_paid/cancel_invoice_paid',
#             'objects': http.request.env['cancel_invoice_paid.cancel_invoice_paid'].search([]),
#         })

#     @http.route('/cancel_invoice_paid/cancel_invoice_paid/objects/<model("cancel_invoice_paid.cancel_invoice_paid"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('cancel_invoice_paid.object', {
#             'object': obj
#         })