from odoo import models, fields, api
from odoo.exceptions import ValidationError

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    # can_archive = fields.Boolean(string="Can Archive", compute="_compute_can_archive", store=False)
    #
    # def _compute_can_archive(self):
    #     """Compute whether the current user is part of the 'Can Archive CRM Leads' group."""
    #     can_archive_crm_leads = 'auto_backup.group_archive_crm_lead'  # Replace with your group's XML ID
    #     for rec in self:
    #         rec.can_archive = self.env.user.has_group(can_archive_crm_leads)

    def write(self, vals):
        if 'active' in vals and not self.env.user.has_group('auto_backup.group_archive_crm_lead'):
            raise ValidationError("You Cannot Archive")
        return super(CrmLead, self).write(vals)