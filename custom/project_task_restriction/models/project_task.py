from odoo import api, fields, models, _
from odoo.exceptions import UserError

class ProjectTask(models.Model):
    _inherit='project.task'


    def write(self, vals):
        if vals.get('stage_id'):
            if self.stage_id.allowed_user_ids:
                u_id = []
                for i in self.stage_id.allowed_user_ids:
                    u_id.append(i.id)
                if not self.env.user.id in u_id:
                    raise UserError(_("You dont have the permissions to change the stage"))
            else:
                raise UserError(_("You dont have the permissions to change the stage"))
        return super(ProjectTask, self).write(vals)