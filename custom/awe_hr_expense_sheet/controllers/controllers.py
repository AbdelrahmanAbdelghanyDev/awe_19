# -*- coding: utf-8 -*-
# from odoo import http


# class AweHrExpenseSheet(http.Controller):
#     @http.route('/awe_hr_expense_sheet/awe_hr_expense_sheet', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/awe_hr_expense_sheet/awe_hr_expense_sheet/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('awe_hr_expense_sheet.listing', {
#             'root': '/awe_hr_expense_sheet/awe_hr_expense_sheet',
#             'objects': http.request.env['awe_hr_expense_sheet.awe_hr_expense_sheet'].search([]),
#         })

#     @http.route('/awe_hr_expense_sheet/awe_hr_expense_sheet/objects/<model("awe_hr_expense_sheet.awe_hr_expense_sheet"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('awe_hr_expense_sheet.object', {
#             'object': obj
#         })
