# -*- coding: utf-8 -*-

from odoo import models, fields, api

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



class OpportunityCostEstimation(models.Model):
    _inherit = 'opportunity.cost.estimation'

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
    # client_attendence_region_ids = fields.Many2many(comodel_name="res.country.state", relation="client_attendence_region_rel", column1="sale_order_1", column2="opportunity_1", string="quotation" )

    cpi = fields.Float(compute='_compute_cpi')

    # quotations_ids = fields.One2many(
    #     'sale.order', 'opportunity_cost_estimation')

    # quotation_id = fields.Many2many('sale.order')
    quotation_id = fields.Many2many(comodel_name="sale.order", relation="sale_order_opportunity_rel", column1="sale_order_1", column2="opportunity_1", string="quotation" )

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


