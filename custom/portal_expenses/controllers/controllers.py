# -*- coding: utf-8 -*-
import math

from werkzeug import urls

from odoo import fields as odoo_fields, tools, _
from odoo.exceptions import ValidationError
from odoo.http import Controller, request, route, Response
from datetime import datetime, timedelta
from odoo.exceptions import UserError, AccessError, ValidationError


class ExpensePortal(Controller):
    @route(['/my/expenses'], type='http', auth="user", website=True)
    def my_expenses(self, **kw):
        def convert_datetime_to_date(date):
            if date:
                return date.split(' ')[0]
            else:
                return False

        get_class_state_dict = {'refused': 'label label-danger', 'reported': 'label label-info',
                                'done': 'label label-success', 'draft': 'label label-warning'}
                                # 'cancel': 'label label-default', 'validate': 'label label-success'}
        get_description_state_dict = {'draft': 'To Submit', 'reported': 'Reported',
                                      'refused': 'Refused', 'done': 'Approved'}
        vals = {}
        vals['convert_datetime_to_date'] = convert_datetime_to_date
        vals['get_description_state_dict'] = get_description_state_dict
        vals['get_class_state_dict'] = get_class_state_dict
        employee_id = request.env['hr.employee'].sudo().search([('user_id', '=', request.uid)])
        expenses = {}
        if employee_id:
            expenses = request.env['hr.expense'].sudo().search(
                [('employee_id', '=', employee_id.id)])#, ('type', '=', 'remove')])
        vals['expenses'] = expenses
        return request.render("portal_expenses.my_expenses", vals)

    @route(['/my/expense/create'], type='http', auth="user", website=True)
    def my_expenses_create(self,vals={}, **kw):
        if 'error' not in vals:
            vals['error'] = {}


        if 'analytic_account_ids' not in vals:
            vals['analytic_account_ids'] = request.env['account.analytic.account'].sudo().search([])
        if 'product_ids' not in vals:
            vals['product_ids'] = request.env['product.product'].sudo().search([('can_be_expensed','=', True)])
        print('expense create vals', vals)
        return request.render("portal_expenses.my_expense", vals)

    @route(['/my/expense/<int:expense_id>'], type='http', auth="user", website=True)
    def my_expense(self, expense_id=0, **kw):
        def convert_datetime_to_date(date):
            if date:
                date = datetime.strptime(date.split(' ')[0], '%Y-%m-%d')
                return date.strftime("%m/%d/%Y")
            else:
                return False

        vals = {}
        vals['error'] = {}
        vals['convert_datetime_to_date'] = convert_datetime_to_date
        vals['analytic_account_ids'] = request.env['account.analytic.account'].sudo().search([])
        vals['product_ids'] = request.env['product.product'].sudo().search([('can_be_expensed','=', True)])
        if expense_id > 0:
            vals['expense'] = request.env['hr.expense'].sudo().browse(expense_id)
            print(vals['expense']['total_amount'])
            print(vals,vals['expense'], vals['expense']['unit_amount'])
            vals['expense']['total_amount'] = vals['expense']['unit_amount'] * vals['expense']['quantity']
        print(vals['expense']['total_amount'], vals)
        return request.render("portal_expenses.my_expense", vals)

    @route(['/my/expense/update'], type='http', auth="user", website=True)
    def my_expense_update(self, expense_id, **post):
        if expense_id != '':
            expense_id = int(expense_id)
            if expense_id > 0:
                expense_id = request.env['hr.expense'].sudo().browse(expense_id)
                if expense_id and post.get('to_delete') == "on":
                    expense_id.unlink()
                elif expense_id:
                    post['state'] = 'draft'#'draft'
                    post['date'] = datetime.strptime(post['date'], "%m/%d/%Y").strftime("%Y-%m-%d %H:%M:%S")
                    # post['date_to'] = datetime.strptime(post['date_to'], "%m/%d/%Y").strftime("%Y-%m-%d %H:%M:%S")
                    if 'date_from_half_day' in post:
                        del post['date_from_half_day']
                    if 'date_to_half_day' in post:
                        del post['date_to_half_day']
                    expense_id.update(post)
        else:
            post['employee_id'] = request.env['hr.employee'].sudo().search([('user_id', '=', request.env.uid)]).id
            # if post['employee_id'] is None:
                # post['employee_id'] = request.env['hr.employee'].sudo().search([('user_id', '=', request.env.uid)]).id
            # post['project_id'] = request['project_id']
            print(post)
            try:
                sheet ={}
                sheet['employee_id'] =  post['employee_id']
                sheet['name'] = post['name']
                sheet['payment_mode'] = post['payment_mode']
                sheet['state'] = 'submit'
                sheet_id = request.env['hr.expense.sheet'].sudo().create(sheet)

                post['sheet_id'] = sheet_id.id
                post['state'] = 'reported'#'draft'
                expense_id = request.env['hr.expense'].sudo().create(post)

                # mult_an = request.env['multible.analytic'].sudo().create({'analytic_account_id.id': post['analytic_account_ids'],
                #                                                       'expense_id':expense_id})
                # expense_id.analytic_account_ids = mult_an
                expense_id.analytic_account_id = post['analytic_account_ids']
                print(expense_id.analytic_account_id)

                expense_id.state = 'draft'
                expense_id.submit_expenses()
                expense_id.state = 'reported'

            except Exception as exc:
                request._cr.rollback()
                print(exc)
                post['error_message'] = "Error " +str(exc) +' '
                return self.my_expenses_create(post)
                # pass
                # return request.redirect('/my/expenses')
        return request.redirect('/my/expenses')

    @route(['/my/expense/delete'], type='http', auth="user", website=True)
    def my_expense_delete(self, **post):
        for key, value in post.items():
            if key.isdigit():
                expense_id = int(key)
                expense_id = request.env['hr.expense'].sudo().browse(expense_id)
                if expense_id:
                    expense_id.unlink()
        return request.redirect('/my/expenses')
