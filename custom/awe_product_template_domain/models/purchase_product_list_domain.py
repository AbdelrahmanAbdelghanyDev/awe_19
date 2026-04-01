from odoo import models, fields, api


# class purchase_product_list_domain(models.Model):
#     _inherit = "product.template"


    # @api.model
    # def search(self, args, offset=0, limit=None,order=None, count=False):
    #
    #         args = [('company_id', '=',self.env.user.company_id.id)] + args
    #         return super(purchase_product_list_domain, self).search(args, offset=offset, limit=limit,
    #                     order=order,count=count)

    # @api.model
    # def search(self, args, offset=0, limit=None, order=None, count=False):
    #     context = self._context or {}
    #     if not context.get('show_parent_account', False):
    #         args += [('user_type_id.type', '!=', 'view')]
    #     return super(AccountAccount, self).search(args, offset, limit, order, count=count)




