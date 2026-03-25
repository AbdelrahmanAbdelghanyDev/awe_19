# -*- coding: utf-8 -*-

from odoo import models, fields, api


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    cancel_visibility = fields.Boolean(compute='get_cancel_visibility')

    def get_cancel_visibility(self):
        for rec in self:
            if rec.state == 'purchase' and not self.env.user.has_group('awe_group_cancel_purchase_order.purchase_order_cancel'):
                rec.cancel_visibility = True
                print(rec.cancel_visibility)
            else:
                rec.cancel_visibility = False
                print(rec.cancel_visibility)

    # @api.model
    # def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
    #     res = super(PurchaseOrder, self).fields_view_get(view_id=view_id,
    #                                                      view_type=view_type,
    #                                                      toolbar=toolbar,
    #                                                      submenu=submenu)
    #     if view_type == 'form':
    #         print(self.env.context)
    #         params = self.env.context.get('params', False)
    #         print(params)
    #         active_id = params.get('id', False) if params else False
    #         print(active_id)
    #         state = self.env['purchase.order'].browse(active_id).state if active_id else False
    #         print(state)
    #         eview = etree.fromstring(res['arch'])
    #         xml_button = eview.xpath("//button[@name='button_cancel']")
    #         print(xml_button)
    #         if xml_button and state == 'purchase':
    #             node = xml_button[0]
    #             invisible_attrs = ['0', False] if self.env.user.\
    #                 has_group('awe_group_cancel_purchase_order.purchase_order_cancel') else ['1', True]
    #             print(invisible_attrs)
    #             node.set('invisible', invisible_attrs[0])
    #             modifiers = json.loads(node.get("modifiers"))
    #             modifiers['invisible'] = invisible_attrs[1]
    #             node.set("modifiers", json.dumps(modifiers))
    #         res['arch'] = etree.tostring(eview)
    #     return res


