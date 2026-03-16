from odoo import models, fields, api,_
from odoo.exceptions import UserError




class Product(models.Model):
    _inherit = 'product.template'

    methodology_id = fields.Boolean(string="Methodology",  default=False)




class ProductProduct(models.Model):
    _inherit = 'product.product'

    methodology_id = fields.Boolean(string="Methodology",  default=False)


class custom_opportunity(models.Model):
    _name = 'crm.lead'
    _inherit = 'crm.lead'

    cost_estimation = fields.One2many(
        'opportunity.cost.estimation',
        'parent_opportunity',
        string="cost_estimation"
    )

    cost_estimation_number = fields.Integer(
        compute='_compute_cost_estimation_amount_total',
        string="cost_estimation_number"
    )

    research_type = fields.Selection([('ql', 'QL'), ('qn', 'QN')])
    approach = fields.Selection([('capi', 'ONLINE'), ('papi', 'OFFLINE')])
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


    type_of_study_qn = fields.Selection([
        ('sti', 'STI'),
        ('clt/ct', 'CLT/CT'),
        ('clt/pt', 'CLT/PT'),
        ('dtd/pp', 'DTD/PP'),
        ('exit', 'EXIT'),
        ('online', 'ONLINE'),
        ('mv', 'MV'),
        ('mc', 'MC'),
        ('cati', 'CATI'),
        ('other/multi', 'OTHER/MULTI'),
    ], string="Type of Study (QN)")

    type_of_study_ql = fields.Selection([
        ('fgd', 'FGD'),
        ('idi/ct', 'IDI/CT'),
        ('mfgd', 'MFGD'),
        ('paired', 'PAIRED'),
        ('triads', 'TRIADS'),
        ('fgd-pt', 'FGD-PT'),
        ('idi-pt', 'IDI-PT'),
        ('mfgd-pt', 'MFGD-PT'),
        ('paired-pt', 'PAIRED-PT'),
        ('triads-pt', 'TRIADS-PT'),
        ('emmersion', 'EMMERSION'),
        ('ethnografic', 'ETHNOGRAFIC'),
        ('ihv', 'IHV'),
        ('shop along', 'SHOP ALONG'),
        ('other/multi', 'OTHER/MULTI'),
    ], string="Type of Study (QL)")

    number_of_products = fields.Integer("Number of Products")
    type_of_products = fields.Char("Type of Products")
    type_of_test = fields.Char("Type of Test")
    product_transportation = fields.Char("Product Transportation")
    products_purchase = fields.Char("Products Purchase")
    products_storage = fields.Char("Products Storage")
    extra_labels = fields.Char("Extra Labels")
    extra_tools_needed = fields.Char("Extra Tools Needed")

    other_multi_note = fields.Text(string="")

    @api.depends('cost_estimation')
    def _compute_cost_estimation_amount_total(self):
        for i in self:
            nbr = 0
            for j in i.cost_estimation:
                nbr += 1
            i.cost_estimation_number = nbr

    #
    def new_cost_estimation(self):
        vals = {
            'partner_id': self.partner_id.id,
            'user_id': self.user_id.id,
            'parent_opportunity': self.id,
            'pricelist_id': self.partner_id.property_product_pricelist and self.partner_id.property_product_pricelist.id or False,
            'research_type': self.research_type,
            'approach': self.approach,
            'methodology': self.methodology,
            'number_of_legs': self.number_of_legs,
            'sample_size': self.sample_size,
            'age': self.age,
            'gender': self.gender,
            'sec': self.sec,
            'region': self.region,
            'usership': self.usership,
            'moub': self.moub,
        }
        estimation = self.env['opportunity.cost.estimation'].create(vals)
        product = self.env['crm.product_line']
        for i in self.pdt_line:

            product_value = {
                'pdt_cost_estimation': estimation.id,
                'product_id': i.product_id.id,
                'name': i.name,
                'product_uom_qty': i.product_uom_qty,
                'uom_id': i.uom_id.id,
                'category': i.category.id,
            }

            product.create(product_value)

        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'opportunity.cost.estimation',
            'target': 'current',
            'res_id': estimation.id,
            'views': [(self.env.ref(
                'custom_opportunity_cost_estimation_v11.opportunity_cost_estimation_form').id,
                'form')],
        }

    company_id = fields.Many2one('res.company', required=True, ondelete='cascade',
                                 default=lambda self: self.env.company.id)

class LeadProductLine(models.Model):
    _name = 'crm.product_line'

    product_id = fields.Many2one(
        'product.product',
        string="Product",
        change_default=True,
        ondelete='restrict',
        required=False, domain='[("methodology_id", "=", True)]'
    )
    name = fields.Text(string='Description')
    pdt_crm = fields.Many2one('crm.lead')
    pdt_crm_2 = fields.Many2one('crm.lead')

    product_uom_qty = fields.Float(string='Quantity', default=1.0)
    price_unit = fields.Float(string='Cost Price')
    market_price = fields.Float(string='Sale Price')
    qty_hand = fields.Integer(string='Quantity On Hand')
    # uom_id = fields.Many2one('product.uom', 'Unit of Measure')
    uom_id = fields.Many2one(
        comodel_name='uom.uom',
        string='Unit of Measure',
        required=False)
    pdt_cost_estimation = fields.Many2one('opportunity.cost.estimation')
    category = fields.Many2one('product.category')

    @api.onchange('product_id')
    def product_data(self):
        data = self.env['product.template'].search(
            [('name', '=', self.product_id.name)])
        self.name = data.name
        self.price_unit = data.list_price
        self.uom_id = data.uom_id
        self.market_price = data.standard_price

        try:
            self.qty_hand = data.qty_available
        except Exception:
            self.qty_hand = 0

        self.category = data.categ_id.id


class LeadProduct(models.Model):
    _inherit = 'crm.lead'

    pdt_line = fields.One2many('crm.product_line', 'pdt_crm', string="Product")

    @api.constrains('pdt_line')
    def constrains_method_pdt_line(self):
        for rec in self:
            if len(rec.pdt_line) > 1:
                raise UserError(_('You Can Create One Line Only'))

    def sale_action_quotations_new(self):
        print ("\n\n\n\n\n")
        vals = {
            'partner_id': self.partner_id.id,
            'user_id': self.user_id.id,
            'parent_opportunity': self.id,
            'opportunity_id': self.id,
            'work_country_id':self.work_country_id.id,
            'revenue_team_id':self.revenue_bu.id,
            'tag_ids': [(6,0, self.tag_ids.ids)],
            'team_id':self.team_id.id
        }
        sale_order = self.env['sale.order'].create(vals)
        order_line = self.env['sale.order.line']
        if self.research_type_id.name == 'QN':
            for data in self.pdt_line:
                pdt_value = {
                    'order_id': sale_order.id,
                    'product_id': data.product_id.id,
                    'name': data.name,
                    'product_uom_qty': data.product_uom_qty,
                    'uom_id': data.uom_id.id,
                }
                order_line.create(pdt_value)
        elif self.research_type_id.name == 'QL':
            for data in self.pdt_line_ql:
                pdt_value = {
                    'order_id': sale_order.id,
                    'product_id': data.product_id.id,
                    'name': data.name,
                    'product_uom_qty': float(data.no_of_units_attendees),
                    'uom_id': data.uom_id.id,
                }
                order_line.create(pdt_value)

        view_id = self.env.ref('sale.view_order_form')
        print ("\n\n\n\n\n")
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'sale.order',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'current',
            'res_id': sale_order.id,
            'view_id': view_id.id,
        }
