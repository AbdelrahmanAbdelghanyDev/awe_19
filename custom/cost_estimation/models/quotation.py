# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from lxml import etree


class QuotationOrderLine(models.Model):
    _inherit = 'sale.order.line'

    estim_line = fields.Many2one('products.line')

    @api.constrains('estim_line')
    def _const_estim_line(self):
        self.tax_ids = self.estim_line.taxes.ids

    estimation_id = fields.Many2one('cost.estimation.template')


class Quotation(models.Model):
    _inherit = 'sale.order'

    cost_estimation_ref = fields.Many2one('cost.estimation', string='Cost Estimation Ref')
    total_cost = fields.Float('Total Material Cost')
    wave_cost = fields.Float('Cost / Wave', default=lambda self: self.total_cost)
    total_margin = fields.Float('Total Margin', digits=(12, 4), )
    margin_percent = fields.Float('Margin Percent', digits=(12, 4), )
    budget_currency_x = fields.Many2one('res.currency', string="Budget Currency", readonly=True, store=True)
    budget_total_x = fields.Float(compute='_compute_budget_total_x', string="Cost (budget currency)")
    margin_x = fields.Float(compute='_compute_margin_x', store=True)
    margin_percentage_x = fields.Char(compute='_compute_margin_x', store=True)
    margin_after_travel_x = fields.Float(compute='_compute_margin_x', store=True)
    margin_percentage_after_x = fields.Char(compute='_compute_margin_x', store=True)
    contribution_profit_x = fields.Float(related='margin_x', store=True)
    contribution_margin_x = fields.Char(related='margin_percentage_x', store=True)
    op_percentage = fields.Float(compute='_compute_op_percent')

    @api.depends('pricelist_id.currency_id.rate', 'amount_untaxed')
    def get_untaxed_company_currency(self):
        new_currency_rate = 0
        for rec in self:
            for currency in rec.pricelist_id.currency_id:
                for currency_line in currency.rate_ids:
                    if currency_line.company_id == rec.company_id:
                        new_currency_rate = currency.rate
                    # elif currency == rec.company_id.currency_id:
                    #     new_currency_rate = 1
            rec.untaxed_company_currency = (rec.amount_untaxed *
                                            (1 / new_currency_rate)) if \
                rec.pricelist_id.currency_id.rate != 0 else 0

    untaxed_company_currency = fields.Float(string="Untaxed Company Currency",
                                            compute='get_untaxed_company_currency', store=False)

    @api.depends('amount_untaxed', 'wave_cost')
    def _compute_op_percent(self):
        self = self.sudo()
        for rec in self:
            if rec.amount_untaxed > 0:
                untaxed_company_rate = (rec.amount_untaxed * (1 / rec.currency_id.rate)) if rec.currency_id.rate != 0 else 0
                planned_revenue = untaxed_company_rate - rec.wave_cost
                rec.op_percentage = (planned_revenue / untaxed_company_rate) * 100 if rec.amount_untaxed != 0 else 0
            else:
                untaxed_company_rate = (
                            rec.amount_untaxed * (1 / rec.currency_id.rate)) if rec.currency_id.rate != 0 else 0
                planned_revenue = untaxed_company_rate + rec.wave_cost
                rec.op_percentage = (planned_revenue / untaxed_company_rate) * 100 if rec.amount_untaxed != 0 else 0

    @api.constrains('cost_estimation_ref')
    def const_est(self):
        for rec in self:
            print('rec', rec)
            if rec.cost_estimation_ref:
                rec.budget_currency_x = rec.cost_estimation_ref.price_list.currency_id

    # @api.one
    # @api.constrains('budget_total_x', 'amount_untaxed', 'travel_expenses', 'third_party_cost')
    @api.depends('budget_total_x', 'amount_untaxed', 'travel_expenses', 'third_party_cost')
    def _compute_margin_x(self):
        for rec in self:
            if rec.amount_untaxed > 0:
                rec.margin_x = rec.amount_untaxed - (
                    rec.budget_total_x if rec.budget_total_x else rec.budget_total) - rec.third_party_cost
                if rec.amount_untaxed == 0:
                    rec.margin_percentage_x = '-Inf %'
                else:
                    rec.margin_percentage_x = str(
                        round(rec.margin_x / rec.amount_untaxed * 100.0, 2)) + ' %'

                rec.margin_after_travel_x = rec.amount_untaxed - \
                                            (
                                                rec.budget_total_x if rec.budget_total_x else rec.budget_total) - rec.travel_expenses - rec.third_party_cost
                if rec.amount_untaxed == 0:
                    rec.margin_percentage_after_x = '-Inf %'
                else:
                    rec.margin_percentage_after_x = str(
                        round(rec.margin_after_travel_x / rec.amount_untaxed * 100.0, 2)) + ' %'
            else:
                rec.margin_x = rec.amount_untaxed + (
                    rec.budget_total_x if rec.budget_total_x else rec.budget_total) - rec.third_party_cost
                if rec.amount_untaxed == 0:
                    rec.margin_percentage_x = '-Inf %'
                else:
                    rec.margin_percentage_x = str(
                        round(rec.margin_x / rec.amount_untaxed * 100.0, 2)) + ' %'

                rec.margin_after_travel_x = rec.amount_untaxed + \
                                            (
                                                rec.budget_total_x if rec.budget_total_x else rec.budget_total) - rec.travel_expenses - rec.third_party_cost
                if rec.amount_untaxed == 0:
                    rec.margin_percentage_after_x = '-Inf %'
                else:
                    rec.margin_percentage_after_x = str(
                        round(rec.margin_after_travel_x / rec.amount_untaxed * 100.0, 2)) + ' %'

            print("YYYY",rec.margin_after_travel_x,rec.margin_x,rec.margin_percentage_x, rec.amount_untaxed, rec.budget_total, rec.travel_expenses, rec.third_party_cost)

    @api.depends('total_cost', 'budget_currency_x', )
    def _compute_budget_total_x(self):
        for rec in self:
            budget_rates = self.env['res.currency.rate'].search(
                [('company_id', '=', rec.company_id.id), ('currency_id', '=', rec.pricelist_id.currency_id.id)],
                limit=1)

            rec.budget_total_x = budget_rates.rate * rec.total_cost

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):

        res = super(Quotation, self).fields_view_get(view_id, view_type, toolbar=toolbar, submenu=submenu)
        eview = etree.fromstring(res['arch'])
        quotation = self.env['ir.config_parameter'].sudo().get_param('quotation_restriction') or False
        if quotation and view_type:
            for node in eview.xpath("//tree"):
                node.set('create', "false")
            for node in eview.xpath("//form"):
                node.set('create', "false")
        else:
            for node in eview.xpath("//form"):
                node.set('create', "true")
            for node in eview.xpath("//tree"):
                node.set('create', "true")
        res['arch'] = etree.tostring(eview)
        return res

    def action_confirm(self):
        res = super(Quotation, self).action_confirm()
        if self.cost_estimation_ref:
            sale_order = self.env['sale.order'].search(
                [('cost_estimation_ref', '=', self.cost_estimation_ref.id), ('state', '=', 'sale')])
            if len(sale_order) > 1:
                raise ValidationError(_("There is a sale order for this cost estimation"))
            else:
                self.cost_estimation_ref.sale_order = self.id
        return res
