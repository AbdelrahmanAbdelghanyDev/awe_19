
from odoo import models, fields


class ResCompany(models.Model):
    _inherit = "res.company"

    revaluation_loss_account_id = fields.Many2one(
        comodel_name='account.account',
        string='Revaluation loss account',
        domain=[('internal_type', '=', 'other')],
        readonly=False,
    )
    revaluation_gain_account_id = fields.Many2one(
        comodel_name='account.account',
        string='Revaluation gain account',
        domain=[('internal_type', '=', 'other')],
        readonly=False,
    )
    revaluation_analytic_account_id = fields.Many2one(
        comodel_name='account.analytic.account',
        string='Revaluation Analytic account',
        readonly=False,
    )
    revaluation_exchange_diff_journal = fields.Many2one('account.journal',string='Exchange Different Journal')
    revaluation_entry_description = fields.Char(string='Entry Description')