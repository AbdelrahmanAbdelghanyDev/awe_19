# -*- coding: utf-8 -*-

from odoo import models, fields, api

# class awe_custmize_date(models.Model):
#     _inherit = 'sale.order'
#
#
#
#     xx_date= fields.Datetime(string="dddddddd")

    # commitment_date = fields.Datetime(compute='_compute_commitment_date', string='Commitment Date', store=True,
    #                                   help="Date by which the products are sure to be delivered. This is "
    #                                        "a date that you can promise to the customer, based on the "
    #                                        "Product Lead Times.")
    #
    # requested_date = fields.Datetime('Requested Date', readonly=True, states={'draft': [('readonly', False)],
    #                                                                           'sent': [('readonly', False)]},
    #                                  copy=False,
    #                                  help="Date by which the customer has requested the items to be "
    #                                       "delivered.\n"
    #                                       "When this Order gets confirmed, the Delivery Order's "
    #                                       "expected date will be computed based on this date and the "
    #                                       "Company's Security Delay.\n"
    #                                       "Leave this field empty if you want the Delivery Order to be "
    #                                       "processed as soon as possible. In that case the expected "
    #                                       "date will be computed using the default method: based on "
    #                                       "the Product Lead Times and the Company's Security Delay.")
    #
    # date_order = fields.Datetime(string='Order Date', required=True, readonly=True, index=True,
    #                              states={'draft': [('readonly', False)], 'sent': [('readonly', False)]}, copy=False,
    #                              default=fields.Datetime.now)

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100