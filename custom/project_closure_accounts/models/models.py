# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
from datetime import datetime , timedelta
import logging
_logger = logging.getLogger(__name__)


# class CrmLeadTAGINH(models.Model):
#     _name = 'crm.tag'
#
#     name = fields.Char(required=True)

class CostAccounts(models.Model):
    _name = 'cost_accounts'

    description = fields.Text('Description')
    original_acc_id = fields.Many2one('account.account', 'Original Account', required=True)
    corresponding_acc_id = fields.Many2one('account.account', 'Corresponding Account', required=True)


class RevenueAccounts(models.Model):
    _name = 'revenue_accounts'

    description = fields.Text('Description')
    revenue_acc_id = fields.Many2one('account.account', 'Revenue Account', required=True)
    accrued_acc_id = fields.Many2one('account.account', 'Accrued Account', required=True)
    company_id = fields.Many2one('res.company', 'Company')
    tag = fields.Many2one('crm.tag', 'Tag', required=True)


class HiddenField(models.Model):
    _inherit = 'account.move'

    cor = fields.Char(hidden_field=True)  # cost or revenue


# class CustomCurrency(models.Model):
#     _inherit = 'res.currency.rate'
#
#
#     def write(self, vals):
#         record = super(CustomCurrency, self).write(vals)
#         print('rec', record, 'self', self, self.rate,self.id, self.currency_id.id, self.currency_id.name)#, record.rate, record.id, self.id)
#         proj_tasks = self.env['project.task'].search([('original_currency_id', '=', self.currency_id.id)])
#
#         print('len of tasks', len(proj_tasks),  proj_tasks)
#         # if self.rate != self.rate:
#         for task in proj_tasks:
#             # print('rev: ', task.revenue, 'old converted ', task.converted_revenue, task.currency_rate)
#             if self.currency_id.rate != 0:
#                 # print('in iff')
#                 # task.write({'converted_revenue': task.revenue / task.currency_rate})  # self.original_currency_id.rate
#                 task.converted_revenue = task.revenue / self.currency_id.rate
#         return record
#
#     @api.model
#     def create(self, vals):
#         record = super(CustomCurrency, self).create(vals)
#         print('create','rec', record, 'self', self, record.rate, record.id, record.currency_id.id,
#               record.currency_id.name)  # , record.rate, record.id, record.id)
#         proj_tasks = self.env['project.task'].search([('original_currency_id', '=', record.currency_id.id)])
#
#         print('len of tasks', len(proj_tasks), proj_tasks)
#         # if self.rate != self.rate:
#         for task in proj_tasks:
#             # print('rev: ', task.revenue, 'old converted ', task.converted_revenue, task.currency_rate)
#             if record.currency_id.rate != 0:
#                 # print('in iff')
#                 # task.write({'converted_revenue': task.revenue / task.currency_rate})  # self.original_currency_id.rate
#                 task.converted_revenue = task.revenue / record.currency_id.rate
#         return record



class CustomProjectTask(models.Model):
    _inherit = 'project.task'

    # def default_counter_value(self):
    #     flag = self.env['res.users'].has_group('project_closure_accounts.group_project_task_revenue')
    #     if not flag:
    #         return 1.0
    #     else:
    #         return self.revenue

    is_cost_button_clicked = fields.Boolean(hidden_field=True, default=False)
    is_revenue_button_clicked = fields.Boolean(hidden_field=True, default=False)
    revenue = fields.Float(string='Sales Value', readonly=True)
    original_currency_id = fields.Many2one('res.currency', readonly=True)
    converted_revenue = fields.Float(string='Sales(Base Currency)', readonly=False, store=True)
    tag_id = fields.Many2one('crm.tag', 'Tag')
    order_date = fields.Datetime(string="Order Date", readonly=False)
    cost_date = fields.Date(string="Cost Date")
    date_start = fields.Date(
        string='FW Starting Date',
        required=False)
    # @api.onchange("cost_date")
    # def getCompanyName(self):
    #     name = self.env['ir.sequence'].search([('name', '=', 'Project Closure'), ('company_id', '=',  self.company_id.id)]).next_by_id()
    #     # id = name.next_by_id()
    #     # next_seq = id.next_by_id(cr, uid, seq_id, context)
    #     # print(id)

    def post_journals(self):
        analytic_tag_ids = self.Revenue_bu.analytic_tag_ids
        partner_id = self.partner_id
        label = self.name
        if self.is_cost_button_clicked:
            return

        if not self.cost_date:
            message = 'Can\'t Create Journal Entry!\n' + 'Please insert Cost Date.'
            raise exceptions.ValidationError(message)
            return

        project_cost_accounts = self.env['cost_accounts']
        journal_entry_item = self.env['account.move.line']
        journal_entry = self.env['account.move']

        # journal_entry_item_found indicates if an item with an original account
        # and project analytic_account_id is found or not
        # journal_entry_item_project is the variable holding reference to the list of found journal_entry_items
        # with one of the original accounts and project_analytic_account_id
        # journal_entry_id holds reference to the newly created journal_entry to hold the items

        # in order for this function to work there should be a journal entry with lines that include
        # 1)the analytic account of the project
        # and 2)the account the same as one of the original accounts in the Cost/Wip Accounts

        # 1st it searches for journal with the name Project Closure and the same company as the currently selected company
        # then it searches for entry items with one of the original accounts and project analytic account
        # if any of the items was already created from the button

        journal_entry_item_found = False
        original_accounts = project_cost_accounts.search([])

        journal_entry_id = self.env['account.move']
        journal_entry_item1 = self.env['account.move.line']
        journal_entry_item2 = self.env['account.move.line']

        if not original_accounts:
            message = 'Can\'t Create Journal Entry!\n' + 'Please Create Cost / WIP accounts.'
            raise exceptions.ValidationError(message)
            return
        current_company_id =  self.company_id.id
        journal = self.env['account.journal'].search(
            [('code', '=', 'PR.C.'), ('company_id', '=', current_company_id)])
        for o_account in original_accounts:
            journal_entry_item_project = journal_entry_item.search(
                [('account_id', '=', o_account.original_acc_id.id),  # original_accounts[i].original_acc_id.id),
                 ('analytic_account_id', '=', self.project_id.analytic_account_id.id),
                 ('move_id.date', '>=', self.date_start), ('move_id.date', '<=', self.cost_date),
                 ('move_id.state', '=', 'posted')])
            # print("journal_entry_item_project : ",journal_entry_item_project)
            # ('date_maturity','>=', self.date_start), ('date_maturity','<=', self.cost_date)
            for item_project in journal_entry_item_project:
                if item_project.move_id.cor == '(cost)' or item_project.move_id.cor == '(revenue)':
                    continue
                if journal_entry_item_found is False:
                    journal_entry_item_found = True
                    journal_entry_id = journal_entry.create({
                        'date': self.cost_date,  # fields.Date.today(),
                        'journal_id': journal.id,  # journal_entry_item_project[j].journal_id.id,#3
                        'ref': self.project_id.name,
                        'name': self.env['ir.sequence'].search([('name', '=', 'Project Closure'),('company_id', '=', current_company_id)]).next_by_id(),
                        # 'name': 'Project Completion ' + self.project_id.analytic_account_id.display_name,
                        'cor': '(cost)',
                    })
                # if the account was credit make it debit and vice versa
                if item_project.debit != 0:
                    item1 = 'credit'
                    item2 = 'debit'
                    amount = item_project.debit
                    amount_currency = item_project.amount_currency
                    currency_id = item_project.currency_id.id
                elif item_project.credit != 0:
                    item1 = 'debit'
                    item2 = 'credit'
                    amount = item_project.credit
                    amount_currency = item_project.amount_currency
                    currency_id = item_project.currency_id.id

                journal_entry_item1 = journal_entry_item.with_context(check_move_validity=False).create({
                    'account_id': o_account.original_acc_id.id,
                    'analytic_account_id': self.project_id.analytic_account_id.id,
                    'move_id': journal_entry_id.id,
                    item1: amount,
                    'amount_currency': amount_currency if item1 == 'debit' else -amount_currency,
                    'currency_id': currency_id,
                    'analytic_tag_ids': analytic_tag_ids.ids,
                    'partner_id': partner_id.id,
                    'name': label,
                    'partner_id': item_project.partner_id.id,
                    'name': item_project.name,
                })
                journal_entry_item2 = journal_entry_item.with_context(check_move_validity=False).create({
                    'account_id': o_account.corresponding_acc_id.id,
                    'analytic_account_id': self.project_id.analytic_account_id.id,
                    'move_id': journal_entry_id.id,
                    item2: amount,
                    'amount_currency': amount_currency if item2 == 'debit' else -amount_currency,
                    'currency_id': currency_id,
                    'analytic_tag_ids': analytic_tag_ids.ids,
                    'partner_id': partner_id.id,
                    'name': label,
                    'partner_id': item_project.partner_id.id,
                    'name': item_project.name,
                })
        if journal_entry_item_found is False:
            message = 'Can\'t Create Journal Entry!\n' + \
                      'No Journal Entry line found with the Analytical Account of the Project' + \
                      ' and One of the Cost / WIP Original Accounts.'
            raise exceptions.ValidationError(message)
            return
        if journal_entry_id and journal_entry_item1 and journal_entry_item2:
            self.is_cost_button_clicked = True


    def close_revenue(self):


        if self.is_revenue_button_clicked:
            return
        print(self.date_deadline)
        # print(self.revenue, self.tag_id, self.sale_line_id)
        # if self.revenue == 0.0 or self.revenue == 1.0:
        #     self.revenue = self.sale_line_id.price_subtotal
        #     for tag in self.sale_line_id.order_id.tag_ids:
        #         self.tag_id = tag.id
        # print(self.revenue, self.tag_id)

        project_revenue_accounts = self.env['revenue_accounts']
        journal_entry_item = self.env['account.move.line']
        journal_entry = self.env['account.move']
        p_r_accounts = project_revenue_accounts.search(
            [('tag', '=', self.tag_id.id), ('company_id', '=', self.company_id.id)])

        current_company_id =  self.company_id.id
        journal = self.env['account.journal'].search(
            [('code', '=', 'PR.C.'), ('company_id', '=', current_company_id)])

        if not p_r_accounts:
            if self.tag_id.name:
                message = (
                            'Can\'t Create Journal Entry!\n' + 'Please Create Revenue account with the tag: ' + self.tag_id.name)
            else:
                message = ('Can\'t Create Journal Entry!\n' + 'No tag found ')
            raise exceptions.ValidationError(message)
            return

        current_company_id = self.company_id.id
        print(" self.company_id.id :> ",self.company_id.name)
        journal = self.env['account.journal'].search(
            [('code', '=', 'PR.C.'), ('company_id', '=', current_company_id)])
        print("journal :> ",journal)
        if p_r_accounts:
            journal_entry_id = journal_entry.create({
                'date': self.date_deadline,  # fields.Date.today(),
                'journal_id': journal.id,
                'ref': self.project_id.name,
                # 'name': 'Project Completion ' + self.project_id.analytic_account_id.display_name,
                'name': self.env['ir.sequence'].search(
                    [('name', '=', 'Project Closure'), ('company_id', '=',  self.company_id.id)]).next_by_id(),
                'cor': '(revenue)'
            })
            journal_entry_item.with_context(check_move_validity=False).create({
                'account_id': p_r_accounts.accrued_acc_id.id,
                'analytic_account_id': self.project_id.analytic_account_id.id,
                'move_id': journal_entry_id.id,
                'debit': self.converted_revenue,
                'amount_currency': self.revenue,
                'currency_id': self.original_currency_id.id,
            })
            journal_entry_item.with_context(check_move_validity=False).create({
                'account_id': p_r_accounts.revenue_acc_id.id,
                'analytic_account_id': self.project_id.analytic_account_id.id,
                'move_id': journal_entry_id.id,
                'credit': self.converted_revenue,
                'amount_currency': -self.revenue,
                'currency_id': self.original_currency_id.id,
            })
            self.is_revenue_button_clicked = True

            self.env['account.move'].search([('invoice_origin', '=', self.sale_line_id.order_id.name)]).write({
                'is_revenue_button_clicked': self.is_revenue_button_clicked,
                'task_state': self.stage_id.id})
            
    def get_converted_revenue   (self, amount_convert):
        self.original_currency_id = self.sale_line_id.currency_id.id
        # print(self.original_currency_id)
        order_rate = self.env['res.currency.rate'].search(
            [('company_id', '=', self.company_id.id), ('currency_id', '=', self.original_currency_id.id),
             ('name', '<=', self.sale_line_id.order_id.confirmation_date)], limit=1)
        # print("Order rate", order_rate,order_rate.rate, 'date:', order_rate.name)
        # print('confirm date:', self.sale_line_id.order_id.confirmation_date)
        # print('company:', self.company_id.name)
        _logger.info("Currency converted with rate is : ", order_rate)
        if not order_rate:
            order_rate = self.env['res.currency.rate'].search(
                [('company_id', '=', self.company_id.id), ('currency_id', '=', self.original_currency_id.id)], limit=1)
        if not order_rate:
            _logger.info("No Currency rates found.")
            the_order_rate = 1
        else:
            _logger.info("Amount will be converted on following rates : ", order_rate.rate)
            the_order_rate = order_rate.rate
        # print('the order rate', the_order_rate)
        # print('revenue', self.revenue)
        my_revenue_total = amount_convert / the_order_rate
        # print('\n\n\n\n\nmy rev total ', my_revenue_total)
        return my_revenue_total

    @api.model
    def get_old_converted_revenue(self):
        proj_tasks = self.env['project.task'].search([])

        for task in proj_tasks:
            task.update({'converted_revenue': task.get_converted_revenue(task.revenue)})

            # if task.is_revenue_button_clicked:

            print('hghhghg', task.converted_revenue)
            # task.original_currency_id = task.sale_line_id.currency_id.id
            # if(task.original_currency_id.rate != 0):
            #     task.converted_revenue = task.revenue/task.company_id.currency_id.rate#task.original_currency_id.rate
