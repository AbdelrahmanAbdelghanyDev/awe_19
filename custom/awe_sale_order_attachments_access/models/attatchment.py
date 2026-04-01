from odoo import models, api
from odoo.exceptions import AccessError

class IrAttachment(models.Model):
    _inherit = "ir.attachment"

    def unlink(self):
        for attachment in self:
            if attachment.res_model == "sale.order" or attachment.res_model == "crm.lead":
                if not self.env.user.has_group("awe_sale_order_attachments_access.group_so_attachment_uploader"):
                    raise AccessError("You are not allowed to delete attachments on Sales Orders.")
        return super().unlink()
