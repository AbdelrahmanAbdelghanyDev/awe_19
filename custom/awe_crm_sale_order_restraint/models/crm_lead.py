# -*- coding: utf-8 -*-
from lxml import etree

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
import logging
from datetime import date

_logger = logging.getLogger(__name__)


class CRMStage(models.Model):
    _inherit = 'crm.stage'

    is_sale = fields.Boolean('Is sale')
    stage_seq = fields.Selection([('start','Start'),('end','End')],string='Stage Start And End')



class CRMLead(models.Model):
    _inherit = 'crm.lead'

    is_sale_group = fields.Boolean('Is sale group',compute='compute_is_sale_group')
    stage_seq = fields.Selection(related='stage_id.stage_seq')

    def compute_is_sale_group(self):
        for rec in self:
            if rec.stage_id.is_sale:
                if not self.env.user.has_group('awe_crm_sale_order_restraint.crm_sale_order_drag_group'):
                    rec.is_sale_group = True
                else:
                    rec.is_sale_group = False
            else:
                rec.is_sale_group = False

    def previous_stage(self):
        sequences = self.env['crm.stage'].sudo().search([])
        seq_list = list(sequences)
        for stage in seq_list:
            if self.stage_id == stage:
                new_seq = seq_list.index(stage) - 1
                self.stage_id = seq_list[new_seq]
                break

    def next_stage(self):
        sequences = self.env['crm.stage'].sudo().search([])
        seq_list = list(sequences)
        for stage in seq_list:
            if self.stage_id == stage:
                new_seq = seq_list.index(stage) + 1
                self.stage_id = seq_list[new_seq]
                break


