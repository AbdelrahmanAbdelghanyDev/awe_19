from odoo import models,fields

# class ResPartner(models.Model):
#     _inherit = 'res.partner'

from odoo.exceptions import UserError

class CostEstimation(models.Model):
    _inherit = 'cost.estimation'

    def unlink(self):
        if not self.env.user.has_group('awe_group.delete_cost_estimation'):
            raise UserError("You are not allowed to delete Cost Estimation records.")
        return super().unlink()

