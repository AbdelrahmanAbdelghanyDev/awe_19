# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from odoo.addons import decimal_precision as dp

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


class Partner(models.Model):
    _inherit = 'res.partner'

    new_client = fields.Boolean(string="New Client")


class cost_estimation(models.Model):
    _name = 'cost.estimation'
    _rec_name = 'seq'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    seq = fields.Char(readonly=True, string="CE No.",copy=False)
    state = fields.Selection([('draft', 'Draft'),
                              ('first_approval', 'Waiting 1st Approval'),
                              ('second_approval', 'Waiting 2nd Approval'),
                              ('approved', 'Approved'),
                              ('rejected', 'Rejected'),
                              ('cancelled', 'Cancelled')], string="State", default='draft', tracking=True)
    customer = fields.Many2one('res.partner', string="Customer", readonly=True, store=True, domain="[('state','=','approved')]")
    opportunity = fields.Many2one('crm.lead', string="Source Document", readonly=True, store=True)
    sales_team = fields.Many2one("crm.team", string="Sales Team", related='opportunity.team_id',
                                 tracking=True, readonly=True)
    sales_person = fields.Many2one("res.users", string="Sales Person", related='opportunity.user_id',
                                   tracking=True, readonly=True)

    price_list = fields.Many2one('product.pricelist', string="PriceList", tracking=True)
    estimate_date = fields.Datetime(readonly=True, default=fields.Datetime.now(), string="Estimation Date", store=True,
                                    tracking=True)

    t_margin = fields.Float(string='Total Margin', store=True, compute='_compute_total', digits=(12, 4),
                            tracking=True)
    t_margin_percentage = fields.Float(string='Margin Percent', store=True,compute='_compute_total', digits=(12, 4),
                                       tracking=True)
    fx = fields.Float('Fx Rate', default=1.0, store=True, digits=(12, 4), tracking=True)

    cost_estimation_line = fields.One2many('cost.estimation.line', 'idx_cost', copy=1)
    products_line = fields.One2many('products.line', 'idx_cost')

    total_material_cost = fields.Float('Total Materials Cost', store=True, compute="_compute_total",
                                       tracking=True)
    total_labour_cost = fields.Float('Total labour Cost', store=True, compute="_compute_total",
                                     tracking=True)
    total_overhead_cost = fields.Float('Total Overhead Cost', store=True, compute="_compute_total",
                                       tracking=True)
    total_cost = fields.Float('Cost / Waves', store=True, compute="_compute_total", tracking=True)
    total_unit_price = fields.Float('Total Selling Price', store=True, compute="_compute_product_line_total",
                                    tracking=True)
    quotations_count = fields.Integer()
    notes = fields.Text('Notes', tracking=True)
    total_product_line_tax = fields.Float('Taxes', compute='_compute_product_line_total', tracking=True)
    currency_id = fields.Many2one('res.currency', related='price_list.currency_id', readonly=True)
    company_id = fields.Many2one('res.company', required=True, ondelete='cascade',
                                 default=lambda self: self.env.company.id)

    sale_order = fields.Many2one('sale.order', readonly=True, string='Sale Order')

    accounting_installed = fields.Boolean()

    research_type = fields.Many2one('product.category',string='Research Type', store=True, readonly=True)
    research_type_name = fields.Char(related='research_type.name')
    approach = fields.Selection([('capi', 'CAPI'), ('papi', 'PAPI')])

    waves = fields.Float(string='Waves', default=1)
    cost_of_waves = fields.Float(string='Cost of Waves', compute='_compute_cost_of_waves')

    cpi_x = fields.Float(string='CPI',compute='_compute_cpi')
    third_party_cost = fields.Float(string="Third Party Cost")
    travel_expenses = fields.Float('Travel Expense')
    hide_create_quotation = fields.Boolean(compute='_check_sale_order_state',default=False)
    cost_estimation_line_access= fields.Boolean(string='Cost Estimation Line Access' ,compute='_compute_cost_estimation_line_access')

    def _compute_cost_estimation_line_access(self):
        cost_estimation_line_access_group='cost_estimation.group_cost_est_line_access'
        for rec in self:
            if self.env.user.has_group(cost_estimation_line_access_group):
                rec.cost_estimation_line_access = True
            else:
                rec.cost_estimation_line_access = False

    @api.depends('sale_order.state')
    def _check_sale_order_state(self):
        for rec in self:
            print('teeest',rec.sale_order)
            if rec.sale_order and (rec.sale_order.state != 'draft'):
                rec.hide_create_quotation = True
            else:
                rec.hide_create_quotation = False
                pass

    @api.depends('cost_of_waves')
    def _compute_cpi(self):
        list_products_line = []
        quantity = 0
        for record in self:
            for rec in record.opportunity.product_line:
                if record.research_type_name == 'QL':
                    quantity = rec.quantity
                if record.research_type_name == 'QN':
                    quantity = rec.quantity_qn
                list_products_line.append(quantity)
            if list_products_line and (sum(list_products_line)>0):
                record.cpi_x = record.cost_of_waves / sum(list_products_line)
            else:
                record.cpi_x = 0
                pass

    @api.depends('waves')
    def _compute_cost_of_waves(self):
        self.cost_of_waves = self.waves * self.total_cost

    # methodology = fields.Char('Methodology')
    # number_of_legs = fields.Integer()
    # sample_size = fields.Float()
    # age = fields.Integer()
    # gender = fields.Selection([('male', 'Male'), ('female', 'Female'), ('both', 'Both')], string="Gender")
    # sec = fields.Char()
    # region = fields.Char()
    # usership = fields.Char()
    # moub = fields.Char()
################ QN ####################
    objective = fields.Char('Objective')
    methodology = fields.Char('Methodology')
    criteria_usage = fields.Text('Criteria / Usage')
    sample_size_text = fields.Char('Sample Size')
    sample_struct_per_reg = fields.Char('Sample Structure per Region')
    sample_struct_per_sec = fields.Char('Sample Structure per SEC')
    sample_struct_per_age = fields.Char('Sample Structure per Age')
    sample_struct_per_gen = fields.Char('Sample Structure per Gender')
    sample_struct_per_bra = fields.Char('Sample Structure per Brand')
    length_of_interview = fields.Selection(
        [('15', '15'), ('15-30', '15-30'), ('30-45', '40-45'), ('45-60', '45-60'), ('60', '60+')],
        string='Length of Interview in Minutes'
    )
    details = fields.Text("Other Details:")

############## QL ##########################

    translation = fields.Selection(
        [('yes', 'Yes'), ('no', 'No')],
        string="Simultaneous Translation"
    )
    other_translation = fields.Char(
        string="Other Translation"
    )
    no_of_client_attendees = fields.Char('Number of Clients to Attend')
    no_of_units_attendees = fields.Char('Number of Units Client will Attend')
    client_attendence_region_ids = fields.Many2many(
        'res.country.state',
        string='Client Attendance Region'
    )
    viewing_facility = fields.Selection([('yes', 'Yes'), ('no', 'No')])

    transcript = fields.Selection(
        [('yes', 'Yes'), ('no', 'No')],
        string='Transcript'
    )

    transcript_lang = fields.Char(
        string='Transcript Language'
    )
    ex_transcript = fields.Selection(
        [('yes', 'Yes'), ('no', 'No')],
        string='Extended Transcript'
    )
    printing_material = fields.Selection(
        [('yes', 'Yes'), ('no', 'No')],
        string='Printing Material'
    )
    details_ql = fields.Text("Other Details:")

    @api.onchange('price_list')
    def onch_pricelist(self):
        self.fx = self.price_list.currency_id.rate

    markup = fields.Float(string="Markup")

    @api.depends('products_line.subtotal', 'products_line.subtotal_taxed', 'products_line.taxes',
                 'total_cost', 'markup')
    def _compute_product_line_total(self):
        for rec in self:
            # prices_list = []
            product_line_tax_list = []
            for rec_product_line in rec.products_line:
                # prices_list.append(rec_product_line.subtotal)
                if rec_product_line.taxes:
                    product_line_tax_list.append(rec_product_line.subtotal_taxed)
            rec.total_product_line_tax = sum(product_line_tax_list)
            # rec.total_unit_price = sum(prices_list) + rec.total_product_line_tax
            rec.total_unit_price = rec.total_cost + (rec.total_cost * (rec.markup / 100))

    @api.depends('cost_estimation_line.total_cost_item_cost',
                 'total_unit_price', 'total_cost', 'third_party_cost',
                 'travel_expenses')
    def _compute_total(self):
        for rec in self:
            # rec = self
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

            rec.total_material_cost = sum(material_list)
            rec.total_labour_cost = sum(labour_list)
            rec.total_overhead_cost = sum(overhead_list)
            rec.total_cost = rec.total_material_cost + rec.total_labour_cost + rec.total_overhead_cost + rec.third_party_cost + rec.travel_expenses

        if rec.total_unit_price:
            rec.t_margin = rec.total_unit_price - rec.total_cost
            rec.t_margin_percentage = (rec.t_margin / rec.total_unit_price) * 100

    @api.model
    def create(self, vals):
        if vals.get('seq', 'New') == 'New':
            # vals['seq'] = self.env['ir.sequence'].next_by_code('cost.estimation') or 'New'
            vals['seq'] = self.env['ir.sequence'].sudo().next_by_code('cost.estimation') or 'New'

        result = super(cost_estimation, self).create(vals)

        return result

    def button_compute(self):
        line_list = []
        for rec in self.cost_estimation_line:
            if rec.salable_product.id not in line_list:
                line_list.append(rec.salable_product.id)
        products_list = []
        for li in line_list:
            unit_cost_list = []
            descp_list = []
            for line in self.cost_estimation_line:
                if line.salable_product.id == li:
                    unit_cost_list.append(line.cost_item_cost_sp)
                    if line.cost_item_description:
                        descp_list.append(line.cost_item_description)
            t = ""
            if descp_list:
                for desc in descp_list:
                    t = t + '- ' + desc + '\n'

            if self.env['cost.product.line'].search([('id','=',li)]).quantity > 0 :
                quantity_line = self.env['cost.product.line'].search([('id','=',li)]).quantity
            else:
                quantity_line = self.env['cost.product.line'].search([('id','=',li)]).quantity_qn
            products_list.append((0, 0, {'idx_cost': self.id, 'cost_item_description': t, 'salable_product': li,
                                         'unit_cost': sum(unit_cost_list)/quantity_line}))

        self.products_line = False
        self.products_line = products_list

    def create_quotation(self):
        quotation = self.env['sale.order']
        quotation_description_product = self.env['ir.config_parameter'].sudo().get_param('quotation_description_product') or False

        product_list = []
        for line in self.products_line:
            if quotation_description_product == 'sp':
                description = line.sp_desc
            else:
                description = line.cost_item_description
            print('line.taxes',line.taxes.ids)
            product_list.append((0, 0, {'product_id': line.salable_product.product_id.id,
                                        'name': description,
                                        'product_uom_qty': line.sp_quant,
                                        'price_unit': line.unit_price,
                                        'estim_line': line.id}))

        quotation.create({'partner_id': self.customer.id,
                          'cost_estimation_ref': self.id,
                          'total_margin': self.t_margin,
                          'margin_percent': self.t_margin_percentage,
                          'total_cost': self.total_material_cost,
                          'wave_cost': self.total_cost,
                          'user_id': self.sales_person.id,
                          'team_id': self.sales_team.id,
                          'pricelist_id': self.customer.property_product_pricelist.id,
                          'opportunity_id': self.opportunity.id,
                          'work_country_id': self.opportunity.work_country_id.id,
                          'project_objective':self.opportunity.project_objective.id,
                          'parent_opportunity':self.opportunity.id,
                          'revenue_team_id':self.opportunity.revenue_bu.id,
                          'third_party_cost':self.third_party_cost,
                          'travel_expenses':self.travel_expenses,
                          'order_line': product_list})
        self.quotations_count = len(self.env['sale.order'].search([('cost_estimation_ref', '=', self.id)]))
        return {
            'name': _('Quotation'),
            'type': 'ir.actions.act_window',
            'res_model': 'sale.order',
            'domain': [('id', '=',
                        self.env['sale.order'].search([('cost_estimation_ref', '=', self.id)], order='name desc',
                                                      limit=1).id)],
            'view_mode': 'tree,form',
        }

    def action_view_quotation(self):
        return {
            'name': _('Quotations'),
            'domain': [('cost_estimation_ref', '=', self.id)],
            'view_mode': 'tree,form',
            'res_model': 'sale.order',
            'view_id': False,
            'context': False,
            'type': 'ir.actions.act_window'
        }

    def submit(self):
        if self.customer.new_client:
            raise ValidationError(_("You can't submit cost estimation with new client"))
        self.state = 'first_approval'
        self.accounting_installed = self.env['cost.estimation'].search([('accounting_installed', '=', True)],
                                                                       limit=1).accounting_installed

    def approve_1(self):
        self.state = 'second_approval'

    def approve_2(self):
        one_approved_cost_est = self.env['ir.config_parameter'].sudo().get_param('one_approved_cost_est') or False
        multiple_ce = self.search([('opportunity', '=', self.opportunity.id), ('state', '=', 'approved')])
        if one_approved_cost_est and (len(multiple_ce) >= 1):
            raise ValidationError(_("You can't Approve Multiple cost estimation "))
        else:
            cost_estimations = self.env['cost.estimation'].search(
                [('opportunity.id', '=', self.opportunity.id), ('state', 'not in', ['approved', 'rejected'])])
            cancel_non_conf_ce = self.env['ir.config_parameter'].sudo().get_param('cancel_non_conf_ce') or False

            if cancel_non_conf_ce:
                for rec in cost_estimations:
                    rec.state = 'cancelled'
            self.state = 'approved'

    def reject_1(self):
        self.state = 'rejected'

    def reject_2(self):
        self.state = 'rejected'

    def cancel(self):
        self.state = 'cancelled'

    def set_draft(self):
        self.state = 'draft'


class ProductsLine(models.Model):
    _name = 'products.line'

    salable_product = fields.Many2one('cost.product.line', string='Methodology', store=True, readonly=True)
    sp_desc = fields.Text(string="Description", related='salable_product.description')
    cost_item_description = fields.Text('CI Description', store=True, readonly=False)
    sp_quant = fields.Float(compute='_compute_quant',string='SS',store=True)
    sp_quant_ql = fields.Float(related='sp_quant',string='No of Units')
    taxes = fields.Many2many('account.tax', string='Taxes', domain=[('type_tax_use', '=', 'sale')])
    # taxes = fields.Many2many('account.tax', string='Taxes', default=lambda self: self.salable_product.product_id.taxes_id.ids, domain=[('type_tax_use', '=', 'sale')])
    unit_of_measure = fields.Many2one('uom.uom', string='UoM', related='salable_product.unit_of_measure', readonly=True)
    unit_cost = fields.Float(string="Unit Cost", store=True, readonly=True)
    total_cost = fields.Float(string="Total Cost", compute='_product_line_calculations', store=True)
    margin = fields.Float(string="Markup")
    subtotal = fields.Float(string="Subtotal", compute='_product_line_calculations')
    subtotal_taxed = fields.Float(string="Subtotal Taxed",compute='_product_line_calculations')
    unit_price = fields.Float(string="Unit Price", compute='_product_line_calculations')
    idx_cost = fields.Many2one('cost.estimation')

    fw_city = fields.Many2one('res.country.state', 'FW City',related='salable_product.fw_city')
    sec = fields.Selection(SEC,related='salable_product.sec',string='SEC')
    gender = fields.Selection([('male', 'Male'),
                               ('female', 'Female'),
                               ('both', 'Both')],related='salable_product.gender')
    age = fields.Char('Age',related='salable_product.age')

    @api.constrains('salable_product')
    def onch_sal(self):
        self.taxes = self.salable_product.product_id.taxes_id.ids

    @api.depends('salable_product')
    def _compute_quant(self):
        for rec in self:
            if rec.salable_product.idx.research_type_name == 'QN':
                rec.sp_quant = rec.salable_product.quantity_qn
            if rec.salable_product.idx.research_type_name == 'QL':
                rec.sp_quant = rec.salable_product.quantity
            else:
                rec.sp_quant = 0
    @api.depends('unit_cost', 'sp_quant', 'margin','taxes')
    def _product_line_calculations(self):
        for rec in self:
            rec.total_cost = (rec.unit_cost * rec.sp_quant)
            rec.subtotal = rec.total_cost + (rec.total_cost * rec.margin / 100)
            rec.unit_price = rec.unit_cost + (rec.unit_cost * rec.margin / 100)
            tax_list = []
            if rec.taxes:
                for tax in rec.taxes:
                    tax_list.append(tax.amount)
                rec.subtotal_taxed = rec.subtotal * (sum(tax_list) / 100)
            else:
                rec.subtotal_taxed = 0


class CostEstimationLine(models.Model):
    _name = 'cost.estimation.line'
    _rec_name = 'budgetary_position'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    # def write(self, vals):
    #     if 'cost_item_cost_currency' in vals:
    #         old_value = self.cost_item_cost_currency
    #         super().write(vals)
    #         new_value = vals['cost_item_cost_currency']
    #         self._track_cost_item_cost_currency_changes(self.idx_cost, old_value, new_value)

    cost_estimation_line_access= fields.Boolean(string='Cost Estimation Line Access' ,compute='_compute_cost_estimation_line_access')

    def _compute_cost_estimation_line_access(self):
        cost_estimation_line_access_group='cost_estimation.group_cost_est_line_access'
        for rec in self:
            if self.env.user.has_group(cost_estimation_line_access_group):
                rec.cost_estimation_line_access = True
            else:
                rec.cost_estimation_line_access = False


    def _track_cost_item_cost_currency_changes(self, parent, old_value, new_value):
        parent.message_post(body=f'Line {self.display_name} Ci Unit Cost(Currency)'
                                 f' Changed from {old_value} -> {new_value}')

    budgetary_position = fields.Many2one('account.budget.post', string='Budgetary Position')

    cost_estimation_line_user_access = fields.Boolean(
        string='Line Access',
        compute='_compute_line_access',
        store=False
    )

    def _compute_line_access(self):
        """Allow editing only for users listed in related account.budget.post.user_ids."""
        current_user = self.env.user
        for line in self:
            line.cost_estimation_line_user_access = (
                    current_user in line.budgetary_position.user_ids
            )

    @api.onchange('cost_item')
    def onchange_cost_item_budget(self):
        if self.cost_item.budgetary_position:
            self.budgetary_position = self.cost_item.budgetary_position.id

    # self.crm_id.message_post(body=message, subject="Stage Changes", attachment_ids=self.attachment.ids)

    # def _track_cost_item_cost_currency_changes(self, field_to_track, new_value):
    #     if self.message_ids:
    #         message_id = field_to_track.message_post(
    #             body=f'{self._description}: {self.display_name}').id
    #         trackings = self.env['mail.tracking.value'].sudo().search(
    #             [('mail_message_id', '=', self.message_ids[0].id)])
    #         for tracking in trackings:
    #             print(tracking.read())
    #             tracking.update({
    #                 'old_value_float': tracking.new_value_float,
    #                 'new_value_float': new_value,
    #             })
    #             tracking.copy({'mail_message_id': message_id})

    salable_product = fields.Many2one('cost.product.line', string='Salable Product',
                                      domain=lambda self: self._domain_product_id())
    sp_desc = fields.Text(string="SP Description", related='salable_product.description')
    sp_quant = fields.Float(string="SP Qty", compute='_compute_quant')
    cost_item = fields.Many2one('product.template', string="Cost Item")
    cost_item_is_true = fields.Boolean(compute='_cost_item', store=True)


    @api.depends('cost_item')
    def _cost_item(self):
        for rec in self:
           if rec.cost_item.is_true:
               rec.cost_item_is_true=True
           else:
               rec.cost_item_is_true=False

    cost_item_description = fields.Text('CI Description')
    cost_item_type = fields.Selection([('material', 'Material'), ('labour', 'Labour'), ('overhead', 'Overhead')],
                                      string="CI Type", required=True, default='material')
    cost_item_quant_sp = fields.Float(string="CI Qty/SP",readonly=False)
    cost_item_cost_currency = fields.Float(string="CI Unit Cost(Currency)", default='1', tracking=True)
    fx = fields.Float('Fx Rate', related='idx_cost.fx', store=True, digits=(12, 4), readonly=True)
    taxes = fields.Many2many('account.tax', string='Taxes', default=False, domain=[('type_tax_use', '=', 'purchase')])
    cost_item_unit_cost = fields.Float(string="CI Unit Cost", compute='_calculations')
    cost_item_cost_sp = fields.Float(string="CI Cost/SP", compute='_calculations')
    total_cost_item_quantity = fields.Float(string='Total CI Qty', compute='_calculations')
    total_cost_item_cost = fields.Float(string='CI Total Cost', compute='_calculations')
    cost_item_uom_id = fields.Many2one('uom.uom', string='CI Unit of Measure', related='cost_item.uom_id',
                                       readonly=True)

    idx_cost = fields.Many2one('cost.estimation')

    @api.depends('salable_product')
    def _compute_quant(self):
        for rec in self:
            rec.sp_quant = 0
            if rec.salable_product.idx.research_type_name == 'QN':
                rec.sp_quant = rec.salable_product.quantity_qn
            elif rec.salable_product.idx.research_type_name == 'QL':
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
        domain = {'salable_product': [('id', 'in', self.idx_cost.opportunity.product_line.ids)]}
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


class CostEstimationTemplate(models.Model):
    _name = "cost.estimation.template"
    _inherit = 'sale.order.template'
    name = fields.Char('Estimation Template', required=True)
    number_of_days = fields.Integer(
        'Estimation Duration',
        help='Number of days for the \
        validity date computation of the Estimation'
    )

    # <quote> naming is not proper here since it is cost estimation,
    # but is keeped here for the sake of the views template.
    quote_line = fields.One2many(
        'cost.estimate.line',
        'quote_id',
        'Quotation Template Lines',
        copy=True
    )

    company_id = fields.Many2one('res.company', required=True, ondelete='cascade',
                                 default=lambda self: self.env.company.id)

    template_sales_ids = fields.One2many('sale.order.line','estimation_id')



class CostEstimationLine(models.Model):
    _name = "cost.estimate.line"
    _inherit = "sale.order.template.line"

    price_unit = fields.Float('Unit Price', required=True, digits=dp.get_precision('Product Price'), default =0)

    product_uom_qty = fields.Float('Quantity', required=True, digits=dp.get_precision('Product UoS'), default=0)

    product_id = fields.Many2one('product.product', 'Product', domain=([]),
                                 required=True)

    quote_id = fields.Many2one('cost.estimation.template')

    my_price_subtotal = fields.Float(string="Total cost", compute='_my_actual_total', store=True)

    @api.onchange('product_id')
    def _onchange_product_id(self):
        self.ensure_one()
        if self.product_id:
            name = self.product_id.name_get()[0][1]
            if self.product_id.description_sale:
                name += '\n' + self.product_id.description_sale
            self.name = name
            # self.price_unit = self.product_id.lst_price
            self.price_unit = 0
            self.product_uom_id = self.product_id.uom_id.id
            self.website_description = self.product_id.quote_description or self.product_id.website_description or ''
            domain = {'product_uom_id': [('category_id', '=', self.product_id.uom_id.category_id.id)]}
            return {'domain': domain}

    @api.onchange('product_uom_id')
    def _onchange_product_uom(self):
        if self.product_id and self.product_uom_id:
            # self.price_unit = self.product_id.uom_id._compute_price(self.product_id.lst_price, self.product_uom_id)
            self.price_unit = 0

    @api.depends('product_uom_qty', 'price_unit')
    def _my_actual_total(self):
        for i in self:
            i.my_price_subtotal = i.product_uom_qty * i.price_unit


    product_uom_category_id = fields.Many2one('uom.category', related='product_id.uom_id.category_id')
