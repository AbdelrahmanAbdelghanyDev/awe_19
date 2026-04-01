# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
from odoo.exceptions import UserError
# from odoo.exceptions import AccessError, UserError, RedirectWarning, ValidationError, Warning
class AccountInvoice(models.Model):
    _inherit = "account.move"

    def action_invoice_cancel(self):
        if self.filtered(lambda inv: inv.state not in ['draft', 'open', 'paid']):
            raise UserError(_("Invoice must be in draft or open or paid state in order to be cancelled."))
        if self.state == 'paid':
            # print(self.move_id.state)
            # self.move_id.state = 'draft'
            # print(self.move_id.state)
            lines = self.env['account.move.line'].search([('move_id','=', self.move_id.id), ('reconciled','=', True)])
            for line in lines:
                line.remove_move_reconcile()

        return self.action_cancel()
