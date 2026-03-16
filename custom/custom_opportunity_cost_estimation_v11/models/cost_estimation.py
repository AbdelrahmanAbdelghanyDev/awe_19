from odoo import models, fields, api, _
from odoo.exceptions import UserError


class OpportunityCostEstimation(models.Model):
    _name = 'opportunity.cost.estimation'

    partner_id = fields.Many2one('res.partner', string='partner_id')
    date_order = fields.Datetime(
        string='Order Date',
        required=True,
        readonly=True,
        index=True,
        copy=False,
        default=fields.Datetime.now
    )
    validity_date = fields.Date(string='Expiration Date', copy=False)
    payment_term_id = fields.Many2one(
        'account.payment.term', string='Payment Terms')

    name = fields.Char(readonly=True, default="New")
    parent_opportunity = fields.Many2one(
        'crm.lead',
        string='parent_opportunity'
    )
    order_line = fields.One2many(
        'custom.sale.order.line',
        'parent_cost',
        string='Order Lines'
    )
    template_id = fields.Many2one(
        'cost.estimation.template', string="template_id")
    pricelist_id = fields.Many2one('product.pricelist', string='Pricelist')

    amount_untaxed = fields.Monetary(
        string='Untaxed Amount',
        store=True,
        readonly=True,
        compute='_amount_all',
         
    )
    amount_tax = fields.Monetary(
        string='Taxes',
        store=True,
        readonly=True,
        compute='_amount_all',
         
    )
    amount_total = fields.Monetary(
        string='Total',
        store=True,
        readonly=True,
        compute='_amount_all',
         
    )

    currency_id = fields.Many2one(
        "res.currency",
        string="Currency",
    )
    company_id = fields.Many2one(
        'res.company',
        'Company',
        default=lambda self: self.env['res.company']._company_default_get(
            'sale.order')
    )

    state = fields.Selection([
        ('draft', 'Draft'),
        ('done', 'Approved'),
        ('cancel', 'Cancelled'),
    ], string='Status', readonly=True, copy=False, index=True, default='draft')

    estimation_type = fields.Many2one('product.category')

    pdt_line = fields.One2many(
        'crm.product_line',
        'pdt_cost_estimation',
        string="Product"
    )
    pdt_line_view = fields.One2many('crm.product_line', 'pdt_cost_estimation')

    research_type = fields.Selection([('ql', 'QL'), ('qn', 'QN')])
    approach = fields.Selection([('capi', 'CAPI'), ('papi', 'PAPI')])
    methodology = fields.Char()
    number_of_legs = fields.Integer()
    sample_size = fields.Float()
    age = fields.Integer()
    gender = fields.Selection(
        [('male', 'Male'), ('female', 'Female'), ('both', 'Both')],
        string="Gender"
    )
    sec = fields.Char()
    region = fields.Char()
    usership = fields.Char()
    moub = fields.Char()

    #

    @api.onchange('estimation_type')
    def onchange_estimation_type(self):
        self.pdt_line_view = self.pdt_line
        for i in self.estimation_type:
            self.pdt_line_view = self.pdt_line_view.filtered(
                lambda r: r.category.id == i.id)

    #
    def action_approve(self):
        if self.estimation_type.id:
            self.write({'state': 'done'})
        else:
            raise UserError(
                _('Must select Estimation type, can\'t left to be blank.')
            )

    #
    def action_cancel(self):
        self.write({'state': 'cancel'})

    #
    def action_draft(self):
        self.write({'state': 'draft'})

    @api.depends('order_line.price_total','template_id')
    def _amount_all(self):
        """
        Compute the total amounts of the SO.
        """
        for order in self:
            amount_untaxed = amount_tax = 0.0
            for line in order.order_line:
                amount_untaxed += line.price_subtotal
                # FORWARDPORT UP TO 10.0
                if order.company_id.tax_calculation_rounding_method == 'round_globally':
                    price = line.price_unit * \
                        (1 - (line.discount or 0.0) / 100.0)
                    taxes = line.tax_id.compute_all(
                        price,
                        line.order_id.currency_id,
                        line.product_uom_qty,
                        product=line.product_id,
                        partner=order.partner_shipping_id
                    )
                    amount_tax += sum(t.get('amount', 0.0)
                                      for t in taxes.get('taxes', []))
                else:
                    amount_tax += line.price_tax
            order.update({
                'amount_untaxed': order.pricelist_id.currency_id.round(amount_untaxed),
                'amount_tax': order.pricelist_id.currency_id.round(amount_tax),
                'amount_total': amount_untaxed + amount_tax,
            })

    #
    # @api.onchange('template_id')
    # def template_id_onchange(self):
    #     if self.template_id:
    #         template=self.env['cost.estimation.template'].search([])
    #         for record in template:
    #             # data = {
    #             #         'order_line': [(6, 0 ,record.quote_line.ids)]
    #             #        }
    #             self.write({'order_line':[(4,record.quote_line.ids)]})





    @api.onchange('template_id')
    def onchange_template_id(self):
        print ("zazzzzzzzzzzzzazzzzzzzzz")
        if not self.template_id:
            return
        template = self.template_id.with_context(lang=self.partner_id.lang)
        order_lines = [(5, 0, 0)]
        for line in template.quote_line:
            if self.pricelist_id:
                price = \
                    self.pricelist_id\
                    .with_context(uom=line.product_uom_id.id)\
                    .get_product_price(line.product_id, 1, False)
            else:
                price = line.price_unit


            if line.price_unit==1:
                myval=0
            else:
                myval=line.price_unit


            if line.product_uom_qty==1:
                qtyval=0
            else:
                qtyval=line.product_uom_qty

            # 'price_unit':line.price_unit,
            data = {
                'name': line.name,
                'price_unit':myval ,
                'discount': line.discount,
                'product_uom_qty': qtyval,
                'product_id': line.product_id.id,
                'layout_category_id': line.layout_category_id,
                'product_uom': line.product_uom_id.id,
                'website_description': line.website_description,
                'price_subtotal_new':line.my_price_subtotal,
                'no_of_waves':1,
            }

            if self.pricelist_id:
                data.update(
                    self.env['custom.sale.order.line']._get_purchase_price(
                        self.pricelist_id,
                        line.product_id,
                        line.product_uom_id,
                        fields.Date.context_today(self)
                    )
                )
            order_lines.append((0, 0, data))

        self.order_line = order_lines
    # @api.model
    # def create(self, vals):
    #     if not vals:
    #         vals = {}
    #     if self._context is None:
    #         self._context = {}
    #
    #     vals['name'] = self.env['ir.sequence'].get('seq.cost.estimation')
    #     return super(OpportunityCostEstimation, self).create(vals)

    @api.model
    def create(self, vals):
        sequence = 'seq.cost.estimation.'
        companies = ('egy', 'ksa', 'res', 'uae')
        current_company_id = self.env.user.company_id.id
        if current_company_id == 3:
            sequence += companies[0]
        elif current_company_id == 4:
            sequence += companies[1]
        elif current_company_id == 1:
            sequence += companies[2]
        elif current_company_id == 5:
            sequence += companies[3]
        vals['name'] = self.env['ir.sequence'].next_by_code(sequence)
        return super(OpportunityCostEstimation, self).create(vals)


    @api.onchange('partner_id')
    def onchange_partner_id(self):
        """
        Update the following fields when the partner is changed:
        - Payment term
        """
        if not self.partner_id:
            self.update({
                'payment_term_id': False,
                'pricelist_id': False,
            })
            return

        values = {
            'pricelist_id': self.partner_id.property_product_pricelist and self.partner_id.property_product_pricelist.id or False,
        }
        self.update(values)

    cpi = fields.Float(
        string='Cpi', 
        required=False)
    translation = fields.Selection(
        [('yes', 'Yes'), ('no', 'No')],
        string="Simultaneous Translation"
    )
    other_translation = fields.Char(
        string="Other Translation"
    )
    research_type_name = fields.Char(
        'Reaseach Type Name',
        related="estimation_type.name",
        readonly=True,
    )
    currency_id = fields.Many2one(
        "res.currency",
        string="Currency",
        readonly=False,
    )

    transcript = fields.Selection(
        [('yes', 'Yes'), ('no', 'No')],
        string='Transcript'
    )

    ex_transcript = fields.Selection(
        [('yes', 'Yes'), ('no', 'No')],
        string='Extended Transcript'
    )
    printing_material = fields.Selection(
        [('yes', 'Yes'), ('no', 'No')],
        string='Printing Material'
    )
    transcript_lang = fields.Char(
        string='Transcript Language'
    )

    client_attendance = fields.Selection([('yes', 'Yes'),
                                          ('no', 'No')])

    no_of_client_attendees = fields.Char('Number of Clients to Attend')
    no_of_units_attendees = fields.Char('Number of Units Client will Attend')

    client_attendence_region_ids = fields.Many2many(
        'res.country.state',
        string='Client Attendance Region'
    )
    client_attendence_region_ids = fields.Many2many(comodel_name="res.country.state", relation="client_attendence_region_rel", column1="sale_order", column2="opportunity", string="quotation" )


    presentation = fields.Selection([('yes', 'Yes'), ('no', 'No')])
    viewing_facility = fields.Selection([('yes', 'Yes'), ('no', 'No')])

    length_of_interview = fields.Char()
    dp = fields.Selection([('yes', 'Yes'), ('no', 'No')])
    reporting = fields.Selection([('yes', 'Yes'), ('no', 'No')])
    presentation = fields.Selection([('yes', 'Yes'), ('no', 'No')])
    viewing_facility = fields.Selection([('yes', 'Yes'), ('no', 'No')])
    client_attendance = fields.Selection([('yes', 'Yes'),
                                          ('no', 'No')])

    details = fields.Text()
    transcript = fields.Selection(
        [('yes', 'Yes'), ('no', 'No')],
        string='Transcript'
    )

    objective = fields.Char('Objective')
    methodology = fields.Char('Methodology')
    criteria_usage = fields.Text('Criteria / Usage')
    sample_size_text = fields.Char('Sample Size')
    sample_struct_per_reg = fields.Char('Sample Structure per Region')
    sample_struct_per_sec = fields.Char('Sample Structure per SEC')
    sample_struct_per_age = fields.Char('Sample Structure per Age')
    sample_struct_per_gen = fields.Char('Sample Structure per Gender')
    sample_struct_per_bra = fields.Char('Sample Structure per Brand')
    no_of_client_attendees = fields.Char('Number of Clients to Attend')
    no_of_units_attendees = fields.Char('Number of Units Client will Attend')
    client_attendence_region_ids = fields.Many2many(
        'res.country.state',
        string='Client Attendance Region'
    )


    cpi = fields.Float(compute='_compute_cpi')

    # quotations_ids = fields.One2many(
    #     'sale.order', 'opportunity_cost_estimation')

    # quotation_id = fields.Many2many('sale.order')
    quotation_id = fields.Many2many(comodel_name="sale.order", relation="sale_order_opportunity_rel",
                                    column1="sale_order_1", column2="opportunity_1", string="quotation")

    ex_transcript = fields.Selection(
        [('yes', 'Yes'), ('no', 'No')],
        string='Extended Transcript'
    )
    printing_material = fields.Selection(
        [('yes', 'Yes'), ('no', 'No')],
        string='Printing Material'
    )
    transcript_lang = fields.Char(
        string='Transcript Language'
    )
    length_of_interview = fields.Char('Length of Interview')
    translation = fields.Selection(
        [('yes', 'Yes'), ('no', 'No')],
        string="Simultaneous Translation"
    )
    other_translation = fields.Char(
        string="Other Translation"
    )
    research_type_name = fields.Char(
        'Reaseach Type Name',
        related="estimation_type.name",
        readonly=True,
    )
    currency_id = fields.Many2one(
        "res.currency",
        string="Currency",
        readonly=False,
    )

    @api.depends('order_line')
    def _compute_cpi(self):
        for record in self:
            sum_qty = 0
            sum_total_cost = 0
            sum_SS = 0
            for line in record.order_line:
                sum_qty += line.product_uom_qty
                sum_total_cost += line.price_subtotal
            for line2 in record.pdt_line_view:
                sum_SS += line2.product_uom_qty

            if sum_SS:
                record.cpi = sum_total_cost / sum_SS
            else:
                record.cpi = 0

    @api.model
    def change_prefix(self):
        seq_id = self.env.ref(
            'custom_opportunity_cost_estimation_v11.seq_cost_estimation').id
        self.env['ir.sequence'].browse(seq_id).prefix = 'BUD/'

class CostEstimationTemplate(models.Model):
    _name = "cost.estimation.template"
    _inherit = "sale.order.template"

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


class CostEstimationLine(models.Model):
    _name = "cost.estimate.line"
    _inherit = "sale.order.template.line"

    price_unit = fields.Float(
        'Unit Price', required=True,
        digits=(16, 2),
        default=0
    )
    product_uom_qty = fields.Float('Quantity', required=True, digits=(16, 2), default=0)

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


