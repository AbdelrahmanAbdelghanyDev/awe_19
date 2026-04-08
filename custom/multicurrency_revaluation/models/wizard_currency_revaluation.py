
from datetime import timedelta

from odoo import models, fields, api, _
from odoo.exceptions import  UserError

# dr_cr = ['Receivable','Bank and Cash','Current asset','Non current asset','Prepayments','Fixed asset','Fixed asset','Depreciation','Cost of revenue','Off_balance sheet']
dr_cr = ['Non-current Assets','Current Assets','Expenses','Receivable','Bank and Cash','Cost of Revenue','Prepayments','Depreciation','Fixed Assets']

#cr_dr = ['Payable','Credit card','Current liability','Non current liability','Income','Other income','Equity','Current year earning']
cr_dr = ['Payable','Current Liabilities','Non-current Liabilities','Equity','Credit Card','Income','Other Income','Current Year Earnings']

class WizardCurrencyRevaluation(models.TransientModel):

    _name = 'wizard.currency.revaluation'
    _description = 'Currency Revaluation Wizard'

    @api.model
    def _get_default_revaluation_date(self):
        """
        Get today's date
        """
        return fields.date.today()

    @api.model
    def _get_default_label(self):
        """
        Get label
        """
        return "%(currency)s %(account)s %(rate)s currency revaluation"

    revaluation_date = fields.Date(string='Revaluation Date',required=True,default=lambda self: self._get_default_revaluation_date(),)
    label = fields.Char(string='Entry description',size=100,help="This label will be inserted in entries description. ",required=True,default=lambda self: self._get_default_label())
    currency = fields.Many2one('res.currency',string='Currency',required=True)

    #
    def revaluate_currency(self):
        """
        Compute unrealized currency gain and loss and add entries to
        adjust balances

        @return: dict to open an Entries view filtered on generated move lines
        """
        # return {'domain': "[('id', 'in', %s)]" % created_ids,
        print(self.currency.name)
        currency_rate = self.env['res.currency.rate'].search([('company_id','=',self.env.user.company_id.id),('currency_id','=',self.currency.id),('name','<=',self.revaluation_date)],order="name")[-1].rate
        account_account = self.env['account.account'].search([('company_id','=',self.env.user.company_id.id),('currency_revaluation','=',True)])
        print('1',account_account)
        created_ids = []
        for account in account_account:
            curr_list = []
            print('2',account)
            account_move_line = self.env['account.move.line'].search([('date','<=',self.revaluation_date),('account_id','=',account.id),('move_id.state','=','posted')])
            for mov_lin in account_move_line:
                curr_list.append(mov_lin.currency_id.id)
            print('account_move_line',account_move_line)
            if self.currency.id in curr_list:
                total_credit = []
                total_debit = []
                amount_currency = []
                for rec in account_move_line:
                    total_credit.append(rec.credit)
                    total_debit.append(rec.debit)
                    amount_currency.append(rec.amount_currency)

                foreign_currency_amount = sum (amount_currency)
                adjust_balance = abs(foreign_currency_amount)/currency_rate


                if account.user_type_id.name in dr_cr:
                    balance_dr_cr = sum(total_debit) - sum(total_credit)
                    entry_value_dr_cr = adjust_balance - balance_dr_cr
                    print('adjust_balance:',adjust_balance)
                    print('balance_dr_cr:',balance_dr_cr)
                    print('entry_value_dr_cr:',entry_value_dr_cr)
                    if entry_value_dr_cr > 0.01:
                        base_line = {
                            'name': account.company_id.revaluation_entry_description,
                            'account_id':account.id,
                            'debit': entry_value_dr_cr,
                            'credit': 0.0,
                        }
                        base_line2 = {
                            'name': account.company_id.revaluation_entry_description,
                            'account_id': account.company_id.revaluation_gain_account_id.id,
                            'debit': 0.00,
                            'credit': entry_value_dr_cr,
                        }
                        base_move = {
                            'journal_id': account.company_id.revaluation_exchange_diff_journal.id,
                            'date': self.revaluation_date,
                            'line_ids': [(0, 0, base_line), (0, 0, base_line2)],
                        }

                        create_entry = self.env['account.move'].search([]).create(base_move)
                        if create_entry.line_ids.ids not in created_ids:
                            print('created_ids1',created_ids)
                            created_ids.extend(create_entry.line_ids.ids)
                            print('created_ids2',created_ids)

                        create_entry.post()
                        # create_entry.write(base_line,base_line2)
                        print('journal entry:',base_move)
                        print('entry1-1:',base_line)
                        print('entry2-1:',base_line2)
                        print('===================')
                    if entry_value_dr_cr < 0.01:
                        base_line = {
                            'name': account.company_id.revaluation_entry_description,
                            'account_id':account.id,
                            'debit': 0.00,
                            'credit': abs(entry_value_dr_cr),
                        }
                        base_line2 = {
                            'name': account.company_id.revaluation_entry_description,
                            'account_id': account.company_id.revaluation_loss_account_id.id,
                            'debit': abs(entry_value_dr_cr),
                            'credit': 0.00,
                        }
                        base_move = {
                            'journal_id': account.company_id.revaluation_exchange_diff_journal.id,
                            'date': self.revaluation_date,
                            'line_ids': [(0, 0, base_line), (0, 0, base_line2)],
                        }
                        if not abs(entry_value_dr_cr) < 0.01:
                            create_entry = self.env['account.move'].search([]).create(base_move)
                            if create_entry.line_ids.ids not in created_ids:
                                print('created_ids3', created_ids)
                                created_ids.extend(create_entry.line_ids.ids)
                                print('created_ids4', created_ids)

                            create_entry.post()
                        # create_entry.write(base_line, base_line2)
                        # create_entry.write({
                        #     'line_ids': [base_line, base_line2]
                        # })
                        print('journal entry:', base_move)
                        print('entry1-2:', base_line)
                        print('entry2-2:', base_line2)
                        print('===================')
                    else:
                        pass

                if account.user_type_id.name in cr_dr:
                    balance_cr_dr = sum(total_credit) - sum(total_debit)
                    entry_value_cr_dr = adjust_balance - balance_cr_dr
                    print('adjust_balance:',adjust_balance)
                    print('balance_cr_dr:',balance_cr_dr)
                    print('entry_value_cr_dr:',entry_value_cr_dr)
                    if entry_value_cr_dr > 0.01:
                        base_line = {
                            'name': account.company_id.revaluation_entry_description,
                            'account_id':account.id,
                            'debit': 0.00,
                            'credit': entry_value_cr_dr,
                        }
                        base_line2 = {
                            'name': account.company_id.revaluation_entry_description,
                            'account_id':account.company_id.revaluation_gain_account_id.id,
                            'debit': entry_value_cr_dr,
                            'credit': 0.00,
                        }
                        base_move = {
                            'journal_id': account.company_id.revaluation_exchange_diff_journal.id,
                            'date': self.revaluation_date,
                            'line_ids': [(0, 0, base_line), (0, 0, base_line2)],
                        }
                        create_entry = self.env['account.move'].search([]).create(base_move)
                        if create_entry.line_ids.ids not in created_ids:
                            created_ids.extend(create_entry.line_ids.ids)
                        create_entry.post()
                        # create_entry.write(base_line, base_line2)
                        # create_entry.write({
                        #     'line_ids': [base_line, base_line2]
                        # })
                        print('journal entry:', base_move)
                        print('entry1:', base_line)
                        print('entry2:', base_line2)
                        print('===================')
                    if entry_value_cr_dr < 0.01:
                        base_line = {
                            'name': account.company_id.revaluation_entry_description,
                            'account_id':account.id,
                            'debit': abs(entry_value_cr_dr),
                            'credit': 0.00,
                        }
                        base_line2 = {
                            'name': account.company_id.revaluation_entry_description,
                            'account_id': account.company_id.revaluation_loss_account_id.id,
                            'debit': 0.00,
                            'credit': abs(entry_value_cr_dr),
                        }
                        base_move = {
                            'journal_id': account.company_id.revaluation_exchange_diff_journal.id,
                            'date': self.revaluation_date,
                            'line_ids': [(0, 0, base_line), (0, 0, base_line2)],
                        }
                        if not abs(entry_value_cr_dr) < 0.01:
                            create_entry = self.env['account.move'].search([]).create(base_move)
                            if create_entry.line_ids.ids not in created_ids:
                                created_ids.extend(create_entry.line_ids.ids)
                            create_entry.post()
                        # create_entry.write(base_line, base_line2)
                        # create_entry.write({
                        #     'line_ids': [base_line,base_line2]
                        # })
                        print('journal entry:', base_move)
                        print('entry1:', base_line)
                        print('entry2:', base_line2)
                        print('===================')
                    else:
                        pass
        print('created_ids:',created_ids)
        if created_ids:
            return {
                    'domain': "[('id', 'in', %s)]" % created_ids,
                    'name': _("Created revaluation lines"),
                    'view_type': 'form',
                    'view_mode': 'tree,form',
                    'auto_search': True,
                    'res_model': 'account.move.line',
                    'view_id': False,
                    'search_view_id': False,
                    'type': 'ir.actions.act_window'}
        else:
            raise UserError(
                _("No accounting entry has been posted.")
            )
