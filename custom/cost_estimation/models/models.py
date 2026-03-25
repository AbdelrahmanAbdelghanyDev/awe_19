# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

SEC = [
    ('A', 'A'),
    ('AB', 'AB'),
    ('BC1', 'BC1'),
    ('C1', 'C1'),
    ('C2', 'C2'),
    ('C1C2', 'C1C2'),
    ('C2D', 'C2D'),
    ('D', 'D'),
    ('E', 'E'),
    ('DE', 'DE'),
]


class cost_estimation_crm(models.Model):
    _inherit = 'crm.lead'

    product_line = fields.One2many('cost.product.line', 'idx')
    # product_line_qn = fields.One2many('cost.product.line.qn','idx')
    estimation_count = fields.Integer(compute='_compute_estimation_data', string="Number of Estimation")
    quotation_restriction = fields.Boolean(
        default=lambda self: self.env['ir.config_parameter'].sudo().get_param('quotation_restriction'))
    sample_size_text = fields.Float('Sample Size', compute='_compute_sample_size', readonly=True)
    sample_size_qn = fields.Float('Sample Size (x)')
    old = fields.Boolean(compute='check_old', default=False, store=True)

    @api.depends('pdt_line', 'pdt_line_ql')
    def check_old(self):
        if self.pdt_line or self.pdt_line_ql:
            self.old = True
        else:
            self.old = False

    def _compute_estimation_data(self):
        for rec in self:
            est_cnt = rec.env['cost.estimation'].search([('opportunity.id', '=', rec.id)])
            rec.estimation_count = len(est_cnt)
            

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
                result = []
                for rec in self.product_line:
                    if (not rec.product_id.cost_ok) and rec.product_id.cost_estimation:
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
                                      'cost_item_cost_currency': 1.0,
                                      'cost_item_quant_sp': product.qty,
                                      'cost_item_uom_id': product.uom.id,
                                      'cost_item_type': cost_item_type,
                                      'cost_item_cost_sp': 1.0,
                                      'taxes': False,
                                      'fx': 1.0,
                                      'total_cost_item_quantity': 1.0,
                                      'budgetary_position': product.budgetary_position.id,
                                      'total_cost_item_cost': 1.0}
                            result.append((0, 0, values))
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
                                  'budgetary_position': rec.product_id.budgetary_position.id,
                                  'cost_item_quant_sp': 1.0,
                                  'cost_item_cost_sp': 1.0,
                                  'taxes': False,
                                  'fx': 1.0,
                                  'total_cost_item_quantity': 1.0,
                                  'total_cost_item_cost': 1.0}
                        result.append((0, 0, values))
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
                    'default_cost_estimation_line': result,
                    'default_seq': 'New',
                }

                return action

    def action_smart_estimation(self):
        action = self.env.ref('cost_estimation.action_cost_estimation').read()[0]

        action['domain'] = [('opportunity', '=', self.id)]

        return action


################################################ QL ######################################
class crm_product_line(models.Model):
    _name = 'cost.product.line'
    _rec_name = 'product_id'

    description = fields.Text(string="Description", compute='_compute_description')
    product_id = fields.Many2one('product.product', string='Methodology', domain='[("methodology_id", "=", True)]')
    custom_company_id = new_field = fields.Integer(compute='_run', default=lambda self:self.env['res.company']._company_default_get('sale.order').id)

    def _run(self):
        for rec in self:
            rec.custom_company_id = rec.env['res.company']._company_default_get('sale.order').id

    fw_country = fields.Many2one('res.country')
    fw_city = fields.Many2one('res.country.state')
    sec = fields.Selection(SEC, string='SEC')
    quantity = fields.Float(string='No of Units')

    quantity_qn = fields.Float(string='ss', default=1)
    mp_of_respondants = fields.Float(string='No of Respondants')
    gender = fields.Selection([('male', 'Male'),
                               ('female', 'Female'),
                               ('both', 'Both')])
    age = fields.Char('Age')
    idx = fields.Many2one('crm.lead')
    unit_of_measure = fields.Many2one('uom.uom', string='UoM', readonly=True)
    # quantity = fields.Float(string='ss')
    # data_capture = fields.Selection([('capi', 'CAPI'),
    #                                  ('papi', 'PAPI'), ('cati', 'CATI'), ('online', 'Online')])

    data_capture = fields.Selection([('capi', 'CAPI'),
                                     ('papi', 'PAPI'),
                                     ('cati', 'CATI'),
                                     ('online', 'Online')])
    research_type_id_crm = fields.Many2one(related='idx.research_type_id')
    research_type_id_crm_name = fields.Char(related='research_type_id_crm.name')

    @api.onchange('product_id')
    def _compute_description(self):
        for rec in self:


            rec.description = ''
            if not rec.sec:
                sec = ''
            if rec.sec:
                sec = rec.sec
            if not rec.fw_city.name:
                fw_city = ''
            if rec.fw_city.name:
                fw_city = rec.fw_city.name
            if not rec.product_id.name:
                product = ''
            if rec.product_id.name:
                product = rec.product_id.name
            if rec.idx.research_type_name == 'QN':
                rec.description = '%s,%s' % (product, fw_city)
            if rec.idx.research_type_name == 'QL':
                rec.description = '%s,%s,%s' % (rec.product_id.name, fw_city, sec)
            rec.unit_of_measure = rec.product_id.uom_id.id