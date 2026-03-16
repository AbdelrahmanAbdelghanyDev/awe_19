from odoo.exceptions import UserError
from odoo import api, fields, models


class AccountMoveInherit(models.Model):
    _inherit = "account.move"

    def unlink(self):
        for move in self:
            if move.move_type == 'entry':
                if self.env.user.has_group('awe_delete_access.group_delete_permission'):
                  raise UserError("You do not have permission to delete this Journal Entries.")

        return super(AccountMoveInherit, self).unlink()

