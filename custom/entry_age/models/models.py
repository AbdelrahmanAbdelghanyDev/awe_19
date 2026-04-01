# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime


class AccountMoveAge(models.Model):
    _inherit = 'account.move'

    complete_checker = fields.Boolean('Completed',default=True)

    account_move_age = fields.Char('Age')

    def _entry_age(self):
        print(self)
        for rec in self.env['account.move'].search([('complete_checker','=',False)]):
            print('rec',rec)
            print('yesss', datetime.today())
            print('xx',rec.date)
            age = datetime.today() - datetime.strptime(rec.date, "%Y-%m-%d")
            rec.account_move_age = age.days
            print(age.days)
