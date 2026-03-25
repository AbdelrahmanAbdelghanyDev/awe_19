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


class CustomSaleOrder(models.Model):
    _inherit = 'sale.order'
    executive_team_id = fields.Many2one('executive.team',tracking=True)
    revenue_team_id = fields.Many2one('revenue.team',tracking=True)

    margin = fields.Float(compute='_compute_margin')
    margin_percentage = fields.Char(compute='_compute_margin')
    contribution_profit = fields.Float(related='margin', store=True)
    contribution_margin = fields.Char(related='margin_percentage', store=True)

    travel_expenses = fields.Float()
    margin_after_travel = fields.Float(compute='_compute_margin')
    margin_percentage_after = fields.Char(compute='_compute_margin')
    third_party_cost = fields.Float(string="Third Party Cost")
    currency_id = fields.Many2one('res.currency', string="Currency", readonly=False)
    budget_total = fields.Float(compute='_compute_budget_total')
    budget_currency = fields.Many2one('res.currency', string="Budget Currency", readonly=False,
                                      related='opportunity_cost_estimation.currency_id')

    margin_percentage_x = fields.Char(
        string='Margin_percentage_x',
        required=False)
    margin_after_travel_x = fields.Float(
        string='Margin_after_travel_x',
        required=False)
    margin_percentage_after_x = fields.Char(
        string='Margin_percentage_after_x',
        required=False)
    budget_total_x = fields.Float(
        string='Budget_total_x',
        required=False)
    @api.depends('opportunity_total_cost', 'budget_currency', )
    def _compute_budget_total(self):
        for rec in self:
            budget_rates = self.env['res.currency.rate'].search(
                [('company_id', '=', rec.company_id.id), ('currency_id', '=', rec.budget_currency.id)], limit=1)
            print("the budget rate", budget_rates)
            company_rates = self.env['res.currency.rate'].search(
                [('company_id', '=', rec.company_id.id), ('currency_id', '=', rec.pricelist_id.currency_id.id)], limit=1)
            print("the company rate", company_rates)

            if rec.pricelist_id.currency_id.rate:
                if not budget_rates:
                    the_budget_rate = 1

                else:
                    the_budget_rate = budget_rates.rate

                if not company_rates:
                    the_company_rate = 1

                else:
                    the_company_rate = company_rates.rate

                first_ex = rec.opportunity_total_cost / the_budget_rate
                print("first_ex", first_ex)
                print("66666666666666666666666", rec.opportunity_total_cost)
                my_budget_total = first_ex * the_company_rate

                rec.update({'budget_total': my_budget_total})

            else:
                rec.update({'budget_total': 0})
            # self.write({'cp_after_travel_custom': self.budget_total})


    @api.depends('budget_total', 'amount_untaxed', 'travel_expenses')
    def _compute_margin(self):
        for rec in self:
            if rec.amount_untaxed > 0:
                if rec.budget_total >= 0:
                    rec.margin = rec.amount_untaxed - rec.budget_total - rec.third_party_cost
                    if rec.amount_untaxed == 0:
                        rec.margin_percentage = '-Inf %'
                    else:
                        rec.margin_percentage = str(
                            round(rec.margin / rec.amount_untaxed * 100.0, 2)) + ' %'
                        rec.margin_percentage_x = '-Inf %'
                    rec.margin_after_travel = rec.amount_untaxed - \
                                               rec.budget_total - rec.travel_expenses - rec.third_party_cost
                    rec.margin_after_travel_x = 0

                    if rec.amount_untaxed == 0:
                        rec.margin_percentage_after = '-Inf %'
                    else:
                        rec.margin_percentage_after = str(
                            round(rec.margin_after_travel / rec.amount_untaxed * 100.0, 2)) + ' %'
                        rec.margin_percentage_after_x = '-Inf %'
                        #################################################################################################

                if rec.budget_total_x > 0 and rec.budget_total == 0:
                    rec.margin_x = rec.amount_untaxed - rec.budget_total_x - rec.third_party_cost

                    if rec.amount_untaxed == 0:
                        rec.margin_percentage_x = '-Inf %'
                    else:
                        rec.margin_percentage_x = str(
                            round(rec.margin_x / rec.amount_untaxed * 100.0, 2)) + ' %'
                        rec.margin_percentage = '-Inf %'

                    rec.margin_after_travel_x = rec.amount_untaxed - \
                                                 rec.budget_total_x - rec.travel_expenses - rec.third_party_cost
                    rec.margin_after_travel = 0
                    if rec.amount_untaxed == 0:
                        rec.margin_percentage_after_x = '-Inf %'
                    else:
                        rec.margin_percentage_after_x = str(
                            round(rec.margin_after_travel_x / rec.amount_untaxed * 100.0, 2)) + ' %'
                        rec.margin_percentage_after = '-Inf %'
            else:
                if rec.budget_total >= 0:
                    rec.margin = rec.amount_untaxed + rec.budget_total - rec.third_party_cost
                    if rec.amount_untaxed == 0:
                        rec.margin_percentage = '-Inf %'
                    else:
                        rec.margin_percentage = str(
                            round(rec.margin / rec.amount_untaxed * 100.0, 2)) + ' %'
                        rec.margin_percentage_x = '-Inf %'
                    rec.margin_after_travel = rec.amount_untaxed + \
                                              rec.budget_total - rec.travel_expenses - rec.third_party_cost
                    rec.margin_after_travel_x = 0

                    if rec.amount_untaxed == 0:
                        rec.margin_percentage_after = '-Inf %'
                    else:
                        rec.margin_percentage_after = str(
                            round(rec.margin_after_travel / rec.amount_untaxed * 100.0, 2)) + ' %'
                        rec.margin_percentage_after_x = '-Inf %'
                        #################################################################################################

                if rec.budget_total_x > 0 and rec.budget_total == 0:
                    rec.margin_x = rec.amount_untaxed + rec.budget_total_x - rec.third_party_cost

                    if rec.amount_untaxed == 0:
                        rec.margin_percentage_x = '-Inf %'
                    else:
                        rec.margin_percentage_x = str(
                            round(rec.margin_x / rec.amount_untaxed * 100.0, 2)) + ' %'
                        rec.margin_percentage = '-Inf %'

                    rec.margin_after_travel_x = rec.amount_untaxed + \
                                                rec.budget_total_x - rec.travel_expenses - rec.third_party_cost
                    rec.margin_after_travel = 0
                    if rec.amount_untaxed == 0:
                        rec.margin_percentage_after_x = '-Inf %'
                    else:
                        rec.margin_percentage_after_x = str(
                            round(rec.margin_after_travel_x / rec.amount_untaxed * 100.0, 2)) + ' %'
                        rec.margin_percentage_after = '-Inf %'
            # self.write({'total_budget_custom': self.margin_after_travel})
            # print('xxxxxxxxxxxxxxxxxx', self.total_budget_custom, self.cp_after_travel_custom)

        # @api.onchange('opportunity_cost_estimation')
        # def _onchange_opportunity(self):
        #     print (self.opportunity_cost_estimation)
        #     self.budget_total = self.opportunity_total_cost_2 * self.pricelist_id.currency_id.rate

        # @api.depends('opportunity_total_cost_2','pricelist_id')
        # def budget_cost(self):
        #
        #     self.budget_total=self.opportunity_total_cost_2*self.pricelist_id.currency_id.rate


    commitment_date = fields.Datetime(compute='_compute_commitment_date', string='Order Dates', store=True,
                                      help="Date by which the products are sure to be delivered. This is "
                                           "a date that you can promise to the customer, based on the "
                                           "Product Lead Times.")

    date_order = fields.Datetime(string='Confirming Date', required=True, readonly=True, index=True,
                                 states={'draft': [('readonly', False)], 'sent': [('readonly', False)]}, copy=False,
                                 default=fields.Datetime.now)
