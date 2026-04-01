from odoo import models, fields, api



class res_currency_rate_inherit(models.Model):
    _inherit = 'res.currency.rate'

    second_rate = fields.Float(string="My Rate")

    @api.onchange('second_rate')
    def _compute_rate(self):
        for record in self:
            if record.second_rate!=0:
               record.rate = 1/record.second_rate




