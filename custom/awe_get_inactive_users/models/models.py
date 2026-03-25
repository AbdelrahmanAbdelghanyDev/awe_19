# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Partner(models.Model):
    _inherit = 'res.partner'

    user_id = fields.Many2one('res.users', string='Salesperson',
                              help='The internal user that is in charge of communicating with this contact if any.',
                              domain=['|', ('active', '=', False), ('active', '=', True)])


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    user_id = fields.Many2one('res.users', string='Salesperson', index=True, track_visibility='onchange',
                              default=lambda self: self.env.user,
                              domain=['|', ('active', '=', False), ('active', '=', True)])

