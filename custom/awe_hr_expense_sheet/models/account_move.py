from odoo import api, fields, models


class AccountMove(models.Model):
    _inherit = 'account.move'

    attachments_ids = fields.Many2many('ir.attachment')

