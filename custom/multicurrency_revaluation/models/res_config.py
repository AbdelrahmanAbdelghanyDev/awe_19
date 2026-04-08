
from odoo import models, fields


class AccountConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    revaluation_loss_account_id = fields.Many2one(
        related='company_id.revaluation_loss_account_id',
        comodel_name='account.account',
        string='Revaluation loss account',
        domain=[('internal_type', '=', 'other')],
        readonly=False,
    )
    revaluation_gain_account_id = fields.Many2one(
        related='company_id.revaluation_gain_account_id',
        comodel_name='account.account',
        string='Revaluation gain account',
        domain=[('internal_type', '=', 'other')],
        readonly=False,
    )
    revaluation_analytic_account_id = fields.Many2one(
        related='company_id.revaluation_analytic_account_id',
        comodel_name='account.analytic.account',
        string='Revaluation Analytic account',
        readonly=False,
    )
    revaluation_exchange_diff_journal = fields.Many2one(related='company_id.revaluation_exchange_diff_journal',comodel_name='account.journal',string='Exchange Different Journal',readonly=False,)
    revaluation_entry_description = fields.Char(related='company_id.revaluation_entry_description',string='Entry Description',readonly=False)