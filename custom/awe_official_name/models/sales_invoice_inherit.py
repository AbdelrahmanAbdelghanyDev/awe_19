from odoo import models, fields, api, _
from odoo.exceptions import UserError


class sales_invoice_inherit(models.Model):
    _inherit = 'account.move'

    official_name = fields.Char(string='Official Name', related='partner_id.official_name')
    # number = fields.Char(related='move_id.name', store=True, readonly=False, copy=False)
    # number = fields.Char(related='seq_name', store=True, readonly=True, copy=False)
    seq_name = fields.Char(string='Invoice Number')
    po_num = fields.Char(string="PO Number")
    gr_num = fields.Char(string="GR Number")
    vendor_num = fields.Char(string="Vendor Number")
    is_revenue_button_clicked = fields.Boolean('Recognized')
    task_state = fields.Many2one('project.task.type', string='Task Stage')
    _sql_constraints = [
        ('code_seq_name_uniq', 'unique (seq_name)', 'Invoice Number must be unique !')
    ]


    def action_invoice_open(self):
        res = super(sales_invoice_inherit, self).action_invoice_open()
        if self.seq_name:
            self.move_id.name = self.seq_name
        else:
            pass
        return res


    def action_move_create(self):
        """ Creates invoice related analytics and financial move lines """
        account_move = self.env['account.move']

        for inv in self:
            if not inv.journal_id.sequence_id:
                raise UserError(_('Please define sequence on the journal related to this invoice.'))
            if not inv.invoice_line_ids:
                raise UserError(_('Please create some invoice lines.'))
            if inv.move_id:
                continue

            ctx = dict(self._context, lang=inv.partner_id.lang)

            if not inv.invoice_date:
                inv.with_context(ctx).write({'invoice_date': fields.Date.context_today(self)})
            if not inv.date_due:
                inv.with_context(ctx).write({'date_due': inv.invoice_date})
            company_currency = inv.company_id.currency_id

            # create move lines (one per invoice line + eventual taxes and analytic lines)
            iml = inv.invoice_line_move_line_get()
            iml += inv.tax_line_move_line_get()

            diff_currency = inv.currency_id != company_currency
            # create one move line for the total and possibly adjust the other lines amount
            total, total_currency, iml = inv.with_context(ctx).compute_invoice_totals(company_currency, iml)

            name = inv.name or '/'
            if inv.payment_term_id:
                totlines = \
                inv.with_context(ctx).payment_term_id.with_context(currency_id=company_currency.id).compute(total,
                                                                                                            inv.invoice_date)[
                    0]
                res_amount_currency = total_currency
                ctx['date'] = inv._get_currency_rate_date()
                for i, t in enumerate(totlines):
                    if inv.currency_id != company_currency:
                        amount_currency = company_currency.with_context(ctx).compute(t[1], inv.currency_id)
                    else:
                        amount_currency = False

                    # last line: add the diff
                    res_amount_currency -= amount_currency or 0
                    if i + 1 == len(totlines):
                        amount_currency += res_amount_currency

                    iml.append({
                        'type': 'dest',
                        'name': name,
                        'price': t[1],
                        'account_id': inv.account_id.id,
                        'date_maturity': t[0],
                        'amount_currency': diff_currency and amount_currency,
                        'currency_id': diff_currency and inv.currency_id.id,
                        'invoice_id': inv.id
                    })
            else:
                iml.append({
                    'type': 'dest',
                    'name': name,
                    'price': total,
                    'account_id': inv.account_id.id,
                    'date_maturity': inv.date_due,
                    'amount_currency': diff_currency and total_currency,
                    'currency_id': diff_currency and inv.currency_id.id,
                    'invoice_id': inv.id
                })
            part = self.env['res.partner']._find_accounting_partner(inv.partner_id)
            line = [(0, 0, self.line_get_convert(l, part.id)) for l in iml]
            line = inv.group_lines(iml, line)

            journal = inv.journal_id.with_context(ctx)
            line = inv.finalize_invoice_move_lines(line)

            date = inv.date or inv.invoice_date
            move_vals = {
                'ref': inv.reference,
                'line_ids': line,
                'journal_id': journal.id,
                'date': date,
                'narration': inv.comment,
            }
            ctx['company_id'] = inv.company_id.id
            ctx['invoice'] = inv
            ctx_nolang = ctx.copy()
            ctx_nolang.pop('lang', None)
            move = account_move.with_context(ctx_nolang).create(move_vals)
            # Pass invoice in context in method post: used if you want to get the same
            # account move reference when creating the same invoice after a cancelled one:
            move.post()
            # make the invoice point to that move
            vals = {
                'move_id': move.id,
                'date': date,
                'move_name': move.name,
            }
            inv.with_context(ctx).write(vals)
        return True

    #
    # def action_move_create(self):
    #     """ Creates invoice related analytics and financial move lines """
    #     account_move = self.env['account.move']
    #
    #     for inv in self:
    #         if not inv.journal_id.sequence_id:
    #             raise UserError(_('Please define sequence on the journal related to this invoice.'))
    #         if not inv.invoice_line_ids:
    #             raise UserError(_('Please create some invoice lines.'))
    #         if inv.move_id:
    #             continue
    #
    #         ctx = dict(self._context, lang=inv.partner_id.lang)
    #
    #         if not inv.date_invoice:
    #             inv.with_context(ctx).write({'date_invoice': fields.Date.context_today(self)})
    #         if not inv.date_due:
    #             inv.with_context(ctx).write({'date_due': inv.date_invoice})
    #         company_currency = inv.company_id.currency_id
    #
    #         # create move lines (one per invoice line + eventual taxes and analytic lines)
    #         iml = inv.invoice_line_move_line_get()
    #         iml += inv.tax_line_move_line_get()
    #
    #         diff_currency = inv.currency_id != company_currency
    #         # create one move line for the total and possibly adjust the other lines amount
    #         total, total_currency, iml = inv.with_context(ctx).compute_invoice_totals(company_currency, iml)
    #
    #         name = inv.name or '/'
    #         if inv.payment_term_id:
    #             totlines = \
    #             inv.with_context(ctx).payment_term_id.with_context(currency_id=company_currency.id).compute(total,
    #                                                                                                         inv.date_invoice)[
    #                 0]
    #             res_amount_currency = total_currency
    #             ctx['date'] = inv._get_currency_rate_date()
    #             for i, t in enumerate(totlines):
    #                 if inv.currency_id != company_currency:
    #                     amount_currency = company_currency.with_context(ctx).compute(t[1], inv.currency_id)
    #                 else:
    #                     amount_currency = False
    #
    #                 # last line: add the diff
    #                 res_amount_currency -= amount_currency or 0
    #                 if i + 1 == len(totlines):
    #                     amount_currency += res_amount_currency
    #
    #                 iml.append({
    #                     'type': 'dest',
    #                     'name': name,
    #                     'price': t[1],
    #                     'account_id': inv.account_id.id,
    #                     'date_maturity': t[0],
    #                     'amount_currency': diff_currency and amount_currency,
    #                     'currency_id': diff_currency and inv.currency_id.id,
    #                     'invoice_id': inv.id
    #                 })
    #         else:
    #             iml.append({
    #                 'type': 'dest',
    #                 'name': name,
    #                 'price': total,
    #                 'account_id': inv.account_id.id,
    #                 'date_maturity': inv.date_due,
    #                 'amount_currency': diff_currency and total_currency,
    #                 'currency_id': diff_currency and inv.currency_id.id,
    #                 'invoice_id': inv.id
    #             })
    #         part = self.env['res.partner']._find_accounting_partner(inv.partner_id)
    #         line = [(0, 0, self.line_get_convert(l, part.id)) for l in iml]
    #         line = inv.group_lines(iml, line)
    #
    #         journal = inv.journal_id.with_context(ctx)
    #         line = inv.finalize_invoice_move_lines(line)
    #
    #         date = inv.date or inv.date_invoice
    #         move_vals = {
    #             'ref': inv.reference,
    #             'line_ids': line,
    #             'journal_id': journal.id,
    #             'date': date,
    #             'narration': inv.comment,
    #         }
    #         ctx['company_id'] = inv.company_id.id
    #         ctx['invoice'] = inv
    #         ctx_nolang = ctx.copy()
    #         ctx_nolang.pop('lang', None)
    #         move = account_move.with_context(ctx_nolang).create(move_vals)
    #         # Pass invoice in context in method post: used if you want to get the same
    #         # account move reference when creating the same invoice after a cancelled one:
    #         move.post()
    #         # make the invoice point to that move
    #         vals = {
    #             'move_id': move.id,
    #             'date': date,
    #             'move_name': move.name,
    #         }
    #         inv.with_context(ctx).write(vals)
    #     return True

    # def button_process_edi_web_services(self):
    #     print('www')
