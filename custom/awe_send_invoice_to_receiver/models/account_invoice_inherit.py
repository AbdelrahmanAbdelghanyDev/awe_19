# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

from xmlrpc import client as xmlrpc_client
import ssl
from odoo.exceptions import  ValidationError


class account_invoice_inherit(models.Model):
    _inherit = 'account.move'

    def get_taxes_amounts(self,taxes):
        taxes_amount = []
        for rec in taxes:
            taxes_amount.append(rec.amount)

        return taxes_amount

    def get_invoice_info_to_send(self):
        if self.invoice_line_ids:
            lines_data = []
            for rec in self.invoice_line_ids:
                lines_data.append({
                    'name': rec.name,
                    'quantity': rec.quantity,
                    'price_unit': rec.price_unit,
                    'discount': rec.discount,
                    'invoice_line_tax_ids': self.get_taxes_amounts(rec.tax_ids) if rec.tax_ids else []
                })

            return {
                'sequence_number_next': self.name,
                'invoice_db_id':self.id,
                'currency_id': self.currency_id.name,
                'date_invoice': self.invoice_date,
                'partner_id': self.partner_id.id,
                'partner_name': self.partner_id.name,
                'po_num': self.po_num,
                'type': self.move_type,
                'gr_num': self.gr_num,
                'custom_payment_terms': self.custom_payment_terms,
                'invoice_line_ids': lines_data
            }

    def send_invoice_to_remote(self,info,remote_system):
        #
        url = remote_system.server_url
        db = remote_system.db_name
        username = remote_system.db_user
        password = remote_system.db_password

        common = xmlrpc_client.ServerProxy('{}/xmlrpc/2/common'.format(url)
                                           , verbose=False, use_datetime=True, context=ssl._create_unverified_context())
        uid = common.authenticate(db, username, password, {})
        models = xmlrpc_client.ServerProxy('{}/xmlrpc/2/object'.format(url), allow_none=True
                                           , verbose=False, use_datetime=True, context=ssl._create_unverified_context())

        models.execute_kw(db, uid, password, 'account.invoice', 'receive_invoices_from_remote', [info])

    def action_post(self):
        res = super(account_invoice_inherit, self).action_post()
        # in case of customer invoice / customer credit note and company is e-invoice
        # send data to another system
        if self.move_type in ('out_invoice', 'out_refund') and self.company_id.e_invoice:
            info = self.get_invoice_info_to_send()
            remote_system = self.env['receiver.system'].search([('syncronize','=',True)],limit=1)
            if remote_system:
                self.send_invoice_to_remote(info,remote_system)
        return res
