# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
from odoo.exceptions import UserError, ValidationError

# from odoo.addons.account.models.account_bank_statement import AccountBankStatementLine as StatementLine
# bloms15

class BankStatmentINh(models.Model):
    _inherit = 'account.bank.statement'


    def button_post(self):
        ''' Move the bank statements from 'draft' to 'posted'. '''
        # if any(statement.state != 'open' for statement in self):
        #     raise UserError(_("Only new statements can be posted."))

        self._check_balance_end_real_same_as_computed()

        for statement in self:
            if not statement.name:
                statement._set_next_sequence()

        self.write({'state': 'posted'})
        lines_of_moves_to_post = self.line_ids.filtered(lambda line: line.move_id.state != 'posted')
        if lines_of_moves_to_post:
            lines_of_moves_to_post.move_id._post(soft=False)


class AccountBankStatementLineinh(models.Model):
    _inherit = 'account.bank.statement.line'



    date = fields.Date(required=True, index=True, copy=False, default=fields.Date.context_today)

    @api.model_create_multi
    def create(self, vals_list):
        # OVERRIDE
        # res = super(StatementLine, self).create(vals_list)
        counterpart_account_ids = []

        for vals in vals_list:
            statement = self.env['account.bank.statement'].browse(vals['statement_id'])
            if statement.state != 'open' and self._context.get('check_move_validity', True):
                # raise UserError(_("You can only create statement line in open bank statements."))
                print('ddd33')
                pass
            # Force the move_type to avoid inconsistency with residual 'default_move_type' inside the context.
            vals['move_type'] = 'entry'

            journal = statement.journal_id
            # Ensure the journal is the same as the statement one.
            vals['journal_id'] = journal.id
            vals['currency_id'] = (journal.currency_id or journal.company_id.currency_id).id
            if 'date' not in vals:
                vals['date'] = statement.date

            # Hack to force different account instead of the suspense account.
            counterpart_account_ids.append(vals.pop('counterpart_account_id', None))

        # # st_lines = super(StatementLine).create(vals_list)
        st_lines = super(AccountBankStatementLineinh, self).create(vals_list)

        for i, st_line in enumerate(st_lines):
            print("curreency :> ",st_line.currency_id)
            counterpart_account_id = counterpart_account_ids[i]

            to_write = {'statement_line_id': st_line.id, 'narration': st_line.narration}
            if 'line_ids' not in vals_list[i]:
                to_write['line_ids'] = [(0, 0, line_vals) for line_vals in st_line._prepare_move_line_default_vals(counterpart_account_id=counterpart_account_id)]

            st_line.move_id.write(to_write)
            st_line.move_id.date = st_line.date

            # Otherwise field narration will be recomputed silently (at next flush) when writing on partner_id
            self.env.remove_to_compute(st_line.move_id._fields['narration'], st_line.move_id)
        return st_lines

    #
    # @api.constrains('amount', 'amount_currency', 'currency_id', 'foreign_currency_id', 'journal_id')
    # def _check_amounts_currencies(self):
    #     ''' Ensure the consistency the specified amounts and the currencies. '''
    #
    #     for st_line in self:
    #         # if st_line.journal_id != st_line.statement_id.journal_id:
    #         #     raise ValidationError(_('The journal of a statement line must always be the same as the bank statement one.'))
    #         # if st_line.foreign_currency_id == st_line.currency_id:
    #         #     raise ValidationError(_("The foreign currency must be different than the journal one: %s", st_line.currency_id.name))
    #         if not st_line.foreign_currency_id and st_line.amount_currency:
    #             raise ValidationError(_("You can't provide an amount in foreign currency without specifying a foreign currency."))
    #
    #
    # @api.depends('journal_id', 'currency_id', 'amount', 'foreign_currency_id', 'amount_currency',
    #              'move_id.to_check',
    #              'move_id.line_ids.account_id', 'move_id.line_ids.amount_currency',
    #              'move_id.line_ids.amount_residual_currency', 'move_id.line_ids.currency_id',
    #              'move_id.line_ids.matched_debit_ids', 'move_id.line_ids.matched_credit_ids')
    # def _compute_is_reconciled(self):
    #     ''' Compute the field indicating if the statement lines are already reconciled with something.
    #     This field is used for display purpose (e.g. display the 'cancel' button on the statement lines).
    #     Also computes the residual amount of the statement line.
    #     '''
    #
    #     for st_line in self:
    #         print("st_line.currency_id :> ",st_line.currency_id)
    #         # st_line.currency_id = st_line.journal_id.currency_id.id
    #         liquidity_lines, suspense_lines, other_lines = st_line._seek_for_lines()
    #
    #         # Compute residual amount
    #         if st_line.to_check:
    #             st_line.amount_residual = -st_line.amount_currency if st_line.foreign_currency_id else -st_line.amount
    #         elif suspense_lines.account_id.reconcile:
    #             st_line.amount_residual = sum(suspense_lines.mapped('amount_residual_currency'))
    #         else:
    #             st_line.amount_residual = sum(suspense_lines.mapped('amount_currency'))
    #
    #         # Compute is_reconciled
    #         if not st_line.id:
    #             # New record: The journal items are not yet there.
    #             st_line.is_reconciled = False
    #         elif suspense_lines:
    #             # In case of the statement line comes from an older version, it could have a residual amount of zero.
    #             st_line.is_reconciled = suspense_lines.currency_id.is_zero(st_line.amount_residual)
    #         elif st_line.currency_id:
    #             if st_line.currency_id.is_zero(st_line.amount):
    #                 st_line.is_reconciled = True
    #         else:
    #             # The journal entry seems reconciled.
    #             st_line.is_reconciled = True
