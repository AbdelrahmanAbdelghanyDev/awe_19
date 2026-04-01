# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class EstimationMethodology(models.Model):
    _name = 'estimation.methodology'
    _rec_name = 'name'
    _description = 'Estimation Methodology'

    name = fields.Char(string='Name', required=1)
    type = fields.Char(string='Type')


class CostEstimation(models.Model):
    _inherit = 'cost.estimation'

    time_estimation_ids = fields.One2many(comodel_name="time.estimation.line", copy=True,
                                          inverse_name="idx_time")

    same_methodology_count = fields.Integer(compute='get_same_methodology_count')

    def get_same_methodology_estimation(self):
        self.ensure_one()
        if self.id:
            return {
                "type": "ir.actions.act_window",
                "name": "Same Methodology Estimation",
                "view_mode": "tree",
                "res_model": "cost.estimation",
                "domain": [('methodology_id', '=', self.methodology_id.id), ('id', '!=', self.id)],
                "context": "{'create': False,'tree_view_ref':'time_cost_estimation.similar_estimation_tree'}",
                # 'view_id': self.env.ref(
                #     'time_cost_estimation.similar_estimation_tree').id,
                # 'views': [(self.env.ref(
                #     'time_cost_estimation.similar_estimation_tree').id,
                #            'tree')],
            }
        else:
            return {
                "type": "ir.actions.act_window",
                "name": "Same Methodology Estimation",
                "view_mode": "tree",
                "res_model": "cost.estimation",
                "domain": [('methodology_id', '=', self.methodology_id.id)],
                "context": "{'create': False,'tree_view_ref':'time_cost_estimation.similar_estimation_tree'}",
                # 'view_id': self.env.ref(
                #     'time_cost_estimation.similar_estimation_tree').id,
                # 'views': [(self.env.ref(
                #     'time_cost_estimation.similar_estimation_tree').id,
                #            'tree')],
            }

    @api.depends('methodology_id')
    def get_same_methodology_count(self):
        for rec in self:
            if rec.id:
                rec.same_methodology_count = self.env['cost.estimation'].search_count([('methodology_id',
                                                                                        '=', rec.methodology_id.id),
                                                                                       ('id', '!=', rec.id)])
            else:
                rec.same_methodology_count = self.env['cost.estimation'].search_count([('methodology_id',
                                                                                        '=', rec.methodology_id.id)])
    markup = fields.Float(string="Markup")

    gross_margin_value = fields.Float(string="Gross Margin Value", compute='get_estimation_margins')
    gross_margin_percentage = fields.Float(string="Gross Margin Percentage %", compute='get_estimation_margins')
    operating_profit = fields.Float(string="Operating Profit", compute='get_estimation_margins')
    operating_profit_percentage = fields.Float(string="Operating Profit Percentage %", compute='get_estimation_margins')
    cpi = fields.Float(string="CPI", compute='get_estimation_margins')

    methodology_id = fields.Many2one(comodel_name="estimation.methodology", string="Methodology Type")

    @api.depends('total_unit_price', 'total_material_cost', 'total_cost', 'opportunity.sample_size')
    def get_estimation_margins(self):
        for rec in self:
            rec.gross_margin_value = rec.total_unit_price - rec.total_material_cost
            rec.gross_margin_percentage = (rec.gross_margin_value / rec.total_unit_price) \
                if rec.total_unit_price != 0 else 0
            rec.operating_profit = rec.total_unit_price - rec.total_cost
            rec.operating_profit_percentage = (rec.operating_profit / rec.total_unit_price) \
                if rec.total_unit_price != 0 else 0
            rec.cpi = rec.total_unit_price / rec.opportunity.sample_size if rec.opportunity.sample_size != 0 else 0

    @api.depends('cost_estimation_line.total_cost_item_cost',
                 'time_estimation_ids.total_cost_item_cost',
                 'total_unit_price', 'total_cost', 'third_party_cost',
                 'travel_expenses')
    def _compute_total(self):
        for rec in self:
            material_list = []
            labour_list = []
            overhead_list = []

            for line in rec.cost_estimation_line:
                if line.cost_item_type == 'material':
                    material_list.append(line.total_cost_item_cost)
                if line.cost_item_type == 'labour':
                    labour_list.append(line.total_cost_item_cost)
                if line.cost_item_type == 'overhead':
                    overhead_list.append(line.total_cost_item_cost)

            for line in rec.time_estimation_ids:
                if line.cost_item_type == 'material':
                    material_list.append(line.total_cost_item_cost)
                if line.cost_item_type == 'labour':
                    labour_list.append(line.total_cost_item_cost)
                if line.cost_item_type == 'overhead':
                    overhead_list.append(line.total_cost_item_cost)

            rec.total_material_cost = sum(material_list)
            rec.total_labour_cost = sum(labour_list)
            rec.total_overhead_cost = sum(overhead_list)
            rec.total_cost = rec.total_material_cost + rec.total_labour_cost + rec.total_overhead_cost + rec.third_party_cost + rec.travel_expenses

        if rec.total_unit_price:
            rec.t_margin = rec.total_unit_price - rec.total_cost
            rec.t_margin_percentage = (rec.t_margin / rec.total_unit_price) * 100


class TimeEstimationLine(models.Model):
    _name = 'time.estimation.line'

    salable_product = fields.Many2one('cost.product.line', string='Salable Product',
                                      domain=lambda self: self._domain_product_id())
    sp_desc = fields.Text(string="SP Description", related='salable_product.description', readonly=True)
    sp_quant = fields.Float(string="SP Qty", compute='_compute_quant')
    cost_item = fields.Many2one('product.template', string="Cost Item")
    cost_item_description = fields.Text('CI Description')
    cost_item_type = fields.Selection([('material', 'Material'), ('labour', 'Labour'), ('overhead', 'Overhead')],
                                      string="CI Type", required=True, default='material')
    cost_item_quant_sp = fields.Float(string="CI Qty/SP", default='1')
    cost_item_cost_currency = fields.Float(string="CI Unit Cost(Currency)", default='0')
    fx = fields.Float('Fx Rate', related='idx_time.fx', store=True, digits=(12, 4), readonly=True)
    taxes = fields.Many2many('account.tax', string='Taxes', default=False, domain=[('type_tax_use', '=', 'purchase')])
    cost_item_unit_cost = fields.Float(string="CI Unit Cost", compute='_calculations')
    cost_item_cost_sp = fields.Float(string="CI Cost/SP", compute='_calculations')
    total_cost_item_quantity = fields.Float(string='Total CI Qty', compute='_calculations')
    total_cost_item_cost = fields.Float(string='CI Total Cost', compute='_calculations')
    cost_item_uom_id = fields.Many2one('uom.uom', string='CI Unit of Measure', related='cost_item.uom_id',
                                       readonly=True)

    idx_time = fields.Many2one('cost.estimation')

    # budgetary_position = fields.Many2one('account.budget.post', string='Budgetary Position')

    # @api.onchange('cost_item')
    # def onchange_cost_item_budget(self):
    #     if self.cost_item.budgetary_position:
    #         self.budgetary_position = self.cost_item.budgetary_position.id

    @api.depends('salable_product')
    def _compute_quant(self):
        for rec in self:
            rec.sp_quant = 0
            if rec.salable_product.idx.research_type_name == 'QN':
                rec.sp_quant = rec.salable_product.quantity_qn
            if rec.salable_product.idx.research_type_name == 'QL':
                rec.sp_quant = rec.salable_product.quantity
            else:
                rec.sp_quant = 0

    @api.depends('cost_item_cost_currency', 'taxes', 'fx', 'cost_item_quant_sp', 'sp_quant')
    def _calculations(self):
        for rec in self:
            taxes_list = []
            for tax in rec.taxes:
                taxes_list.append(tax.amount)
            if rec.fx > 0:
                rec.cost_item_unit_cost = (rec.cost_item_cost_currency / rec.fx) + (
                        (rec.cost_item_cost_currency / rec.fx) * (sum(taxes_list) / 100))
            else:
                rec.cost_item_unit_cost = rec.cost_item_cost_currency + (
                        rec.cost_item_cost_currency * (sum(taxes_list) / 100))

            rec.cost_item_cost_sp = rec.cost_item_unit_cost * rec.cost_item_quant_sp
            rec.total_cost_item_quantity = rec.cost_item_quant_sp * rec.sp_quant
            # rec.total_cost_item_cost = rec.cost_item_cost_sp * rec.sp_quant
            rec.total_cost_item_cost = rec.cost_item_unit_cost * rec.cost_item_quant_sp

    @api.onchange('salable_product')
    def onchange_salable_product(self):
        domain = {'salable_product': [('id', 'in', self.idx_time.opportunity.product_line.ids)]}
        return {'domain': domain}

    @api.onchange('cost_item')
    def onchange_cost_item(self):
        self.cost_item_description = self.cost_item.description_picking
        self.cost_item_uom_id = self.cost_item.uom_id.id
        self.cost_item_type = self.cost_item.cost_item_type

    def _domain_product_id(self):
        if self.env.context.get('active_id'):
            opportunity = self.env['crm.lead'].search(
                [('id', '=', self.env.context.get('active_id'))])

            return "[('id', 'in', %s)]" % opportunity.product_line.ids


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    def action_estimation(self):
        if self.sample_size == 0:
            raise ValidationError("Sample Size Can't be zero")
        approved_cost_estimation = self.env['cost.estimation'].search(
            [('opportunity.id', '=', self.id), ('state', '=', 'approved')])
        multiple_cost_estimate = self.env['ir.config_parameter'].sudo().get_param('multiple_cost_estimate') or False
        quantity = 0
        if approved_cost_estimation and not multiple_cost_estimate:
            raise ValidationError(
                _("You can't create multiple cost estimation for this opportunity due to your setting restrictions"))
        else:
            if (not self.product_line) and (not self.pdt_line) and (not self.pdt_line_ql):
                raise ValidationError(_(
                    "You can't create cost estimation without product lines"))
            else:
                if self.pdt_line:
                    self.product_line = False
                    result_qn = []
                    for line_qn in self.pdt_line:
                        values_qn = {'product_id': line_qn.product_id.id,
                                     'fw_country': line_qn.fw_city_country,
                                     'data_capture': line_qn.data_capture,
                                     'fw_city': line_qn.fw_country,
                                     'quantity_qn': line_qn.product_uom_qty}
                        result_qn.append((0, 0, values_qn))
                    self.product_line = result_qn
                if self.pdt_line_ql:
                    self.product_line = False
                    result_ql = []
                    for line_ql in self.pdt_line_ql:
                        values_ql = {'product_id': line_ql.product_id.id,
                                     'fw_country': line_ql.fw_city_country,
                                     'data_capture': line_ql.data_capture,
                                     'fw_city': line_ql.fw_country,
                                     'sec': line_ql.sec,
                                     'mp_of_respondants': line_ql.no_of_respondants,
                                     'gender': line_ql.gender,
                                     'age': line_ql.age,
                                     'quantity': line_ql.no_of_units_attendees}
                        result_ql.append((0, 0, values_ql))
                    self.product_line = result_ql
                cost_estimation_line = []
                time_estimation_line = []
                for rec in self.product_line:
                    if (not rec.product_id.cost_ok) and (rec.product_id.cost_estimation or
                                                         rec.product_id.time_estimation_ids):
                        if self.research_type_name == 'QN':
                            quantity = rec.quantity_qn
                        if self.research_type_name == 'QL':
                            quantity = rec.quantity
                        for product in rec.product_id.cost_estimation:
                            if not product.cost_item_type:
                                cost_item_type = 'material'
                            else:

                                cost_item_type = product.cost_item_type
                            values = {'salable_product': rec.id,
                                      'sp_desc': rec.description,
                                      'sp_quant': quantity,
                                      'cost_item': product.product_id.id,
                                      'cost_item_description': product.description,
                                      'cost_item_unit_cost': 1.0,
                                      'cost_item_cost_currency': 0.0,
                                      'cost_item_quant_sp': product.qty,
                                      'cost_item_uom_id': product.uom.id,
                                      'cost_item_type': cost_item_type,
                                      'cost_item_cost_sp': 1.0,
                                      'taxes': False,
                                      'fx': 1.0,
                                      'total_cost_item_quantity': 1.0,
                                      # 'budgetary_position': product.budgetary_position.id,
                                      'total_cost_item_cost': 1.0}
                            cost_estimation_line.append((0, 0, values))

                        for product in rec.product_id.time_estimation_ids:
                            if not product.cost_item_type:
                                cost_item_type = 'overhead'
                            else:
                                cost_item_type = product.cost_item_type
                            values = {'salable_product': rec.id,
                                      'sp_desc': rec.description,
                                      'sp_quant': quantity,
                                      'cost_item': product.product_id.id,
                                      'cost_item_description': product.description,
                                      'cost_item_unit_cost': 1.0,
                                      'cost_item_cost_currency': 0.0,
                                      'cost_item_quant_sp': product.product_id.standard_price,
                                      'cost_item_uom_id': product.uom.id,
                                      'cost_item_type': cost_item_type,
                                      'cost_item_cost_sp': 1.0,
                                      'taxes': False,
                                      'fx': 1.0,
                                      'total_cost_item_quantity': 1.0,
                                      # 'budgetary_position': product.budgetary_position.id,
                                      'total_cost_item_cost': 1.0}
                            time_estimation_line.append((0, 0, values))
                    else:
                        if self.research_type_name == 'QN':
                            quantity = rec.quantity_qn
                        if self.research_type_name == 'QL':
                            quantity = rec.quantity
                        values = {'salable_product': rec.id,
                                  'sp_desc': rec.description,
                                  'sp_quant': quantity,
                                  'cost_item': False,
                                  'cost_item_description': False,
                                  'cost_item_unit_cost': 1.0,
                                  'cost_item_cost_currency': 1.0,
                                  'cost_item_type': 'material',
                                  # 'budgetary_position': rec.product_id.budgetary_position.id,
                                  'cost_item_quant_sp': 1.0,
                                  'cost_item_cost_sp': 1.0,
                                  'taxes': False,
                                  'fx': 1.0,
                                  'total_cost_item_quantity': 1.0,
                                  'total_cost_item_cost': 1.0}
                        cost_estimation_line.append((0, 0, values))
                        time_estimation_line.append((0, 0, values))
                action = self.env.ref("cost_estimation.cost_estimation_form_action").read()[0]

                action['context'] = {
                    'default_customer': self.partner_id.id,
                    'default_research_type': self.research_type_id.id,
                    'default_opportunity': self.id,
                    'default_price_list': self.partner_id.property_product_pricelist.id,
                    'default_objective': self.objective,
                    'default_methodology': self.methodology,
                    'default_criteria_usage': self.criteria_usage,
                    'default_sample_size_text': self.sample_size_text,
                    'default_sample_struct_per_reg': self.sample_struct_per_reg,
                    'default_sample_struct_per_sec': self.sample_struct_per_sec,
                    'default_sample_struct_per_age': self.sample_struct_per_age,
                    'default_sample_struct_per_gen': self.sample_struct_per_gen,
                    'default_sample_struct_per_bra': self.sample_struct_per_bra,
                    'default_length_of_interview': self.length_of_interview_sel,
                    'default_details': self.details,
                    'default_sp_desc': self.description,
                    'default_translation': self.translation,
                    'default_other_translation': self.other_translation,
                    'default_no_of_client_attendees': self.no_of_client_attendees,
                    'default_no_of_units_attendees': self.no_of_units_attendees,
                    'default_client_attendence_region_ids': self.client_attendence_region_ids.ids,
                    'default_viewing_facility': self.viewing_facility,
                    'default_transcript': self.transcript,
                    'default_transcript_lang': self.transcript_lang,
                    'default_ex_transcript': self.ex_transcript,
                    'default_printing_material': self.printing_material,
                    'default_details_ql': self.details_ql,
                    'default_cost_estimation_line': cost_estimation_line,
                    'default_time_estimation_ids': time_estimation_line,
                    'default_seq': 'New',
                }

                return action


class ProductTemplate(models.Model):
    _inherit = "product.template"

    time_estimation_ids = fields.One2many('product.time.cost.line', 'idt')


class ProductTimeCostLine(models.Model):
    _name = 'product.time.cost.line'
    _description = 'Product Time Cost Line'

    product_id = fields.Many2one('product.template', string='Product')
    description = fields.Text('Description', related='product_id.description_picking')
    qty = fields.Float('Quantity')
    uom = fields.Many2one('uom.uom', string='Unit of Measure')
    cost_item_type = fields.Selection(related='product_id.cost_item_type', string="CI Type")
    idt = fields.Many2one('product.template')
    # budgetary_position = fields.Many2one('account.budget.post', related='product_id.budgetary_position',
    #                                      string='Budgetary Position')

    @api.onchange('product_id')
    def _onch_proj(self):
        self.uom = self.product_id.uom_id.id

