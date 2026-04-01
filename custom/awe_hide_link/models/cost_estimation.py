from odoo import models, api, _
from odoo.exceptions import ValidationError

class CrmLead(models.Model):
    _inherit = 'cost.estimation'