from odoo import models, api, _
from odoo.exceptions import ValidationError

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    # @api.model
    # def action_open_record(self, record_id):
    #     """
    #     Override to prevent opening the external link for partner_id.
    #     """
    #     record = self.env['res.partner'].browse(record_id)
    #     if record and self._context.get('model') == 'crm.lead':
    #         raise ValidationError(_("You are not allowed to open the external link for this partner."))
    #     return super(CrmLead, self).action_open_record(record_id)
