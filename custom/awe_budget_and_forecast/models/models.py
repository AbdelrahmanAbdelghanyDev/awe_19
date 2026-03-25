# -*- coding: utf-8 -*-
from odoo import models, fields, api
from collections import defaultdict
import json


class BudgetAndForecast(models.Model):
    _name = 'budget.forecast'
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _rec_name = 'name'

    name = fields.Char(string='Reference', required=True, tracking=True)
    comparison_ids = fields.Many2many(comodel_name='budget.forecast', relation='budget_forecast_comparison_rel',
                                      column1='budget_forecast_id',
                                      column2='compare_id',
                                      string='Compare Records',
                                      domain="[('id', '!=', id)]",
                                      limit=5, tracking=True)
    type = fields.Selection([('consumer', 'Consumer'), ('health_care', 'Health Care')], tracking=True)
    year = fields.Char(tracking=True)
    comparison_count = fields.Integer(string='Comparison Count', compute='_compute_comparison_count')
    budget_forecast_line_ids = fields.One2many(comodel_name='budget.forecast.line', inverse_name='budget_forecast_id',
                                               string='Lines')
    comparison_line_ids = fields.One2many(comodel_name='comparison.line', inverse_name='budget_forecast_id',
                                          string='Comparison')
    sales_bu_total_ids = fields.One2many(comodel_name='sales.bu.total', inverse_name='budget_forecast_id',
                                         string='Sales BU Totals')
    rev_bu_total_ids = fields.One2many(comodel_name='rev.bu.total', inverse_name='budget_forecast_id',
                                       string='Revenue BU Totals')
    state = fields.Selection([('draft', 'Draft'),
                              ('approved', 'Approved')], string='Status', default='draft', tracking=True)

    # partner_id_domain = fields.Char(compute="_compute_partner_id_domain")
    #
    # def _compute_partner_id_domain(self):
    #     for rec in self:
    #         clients = []
    #         partners = self.env['res.partner'].search([('ref', '!=', False)])
    #         for partner in partners:
    #             if partner.ref[0] == 'C':
    #                 clients.append(partner.id)
    #         rec.partner_id_domain = json.dumps([('id', 'in', clients)])

    @api.depends('comparison_ids')
    def _compute_comparison_count(self):
        for record in self:
            record.comparison_count = len(record.comparison_ids) + 1

    def action_approve(self):
        self.state = 'approved'

    def action_reset_to_draft(self):
        self.state = 'draft'

    def get_totals(self):

        self.sales_bu_total_ids.unlink()  # Clear previous data
        self.rev_bu_total_ids.unlink()  # Clear previous data

        # Grouped totals for Sales BU
        sales_bu_totals_dict = defaultdict(lambda: {'sales': 0, 'rev': 0, 'gm': 0})
        # Grouped totals for Revenue BU
        rev_bu_totals_dict = defaultdict(lambda: {'sales': 0, 'rev': 0, 'gm': 0})
        # for budget_forecast in all_budget_forecasts:
        #     for line in budget_forecast.budget_forecast_line_ids:
        for line in self.budget_forecast_line_ids:
            if line.sales_bu_id:
                sales_bu_totals_dict[line.sales_bu_id.id]['sales'] += line.sales
                sales_bu_totals_dict[line.sales_bu_id.id]['rev'] += line.rev
                sales_bu_totals_dict[line.sales_bu_id.id]['gm'] += line.gm
            if line.rev_bu_id:
                rev_bu_totals_dict[line.rev_bu_id.id]['sales'] += line.sales
                rev_bu_totals_dict[line.rev_bu_id.id]['rev'] += line.rev
                rev_bu_totals_dict[line.rev_bu_id.id]['gm'] += line.gm

        sales_bu_totals = [
            {
                'sales_bu_id': sales_bu_id,
                'sales': totals['sales'],
                'rev': totals['rev'],
                'gm': totals['gm'],
                'budget_forecast_id': self.id,
            }
            for sales_bu_id, totals in sales_bu_totals_dict.items()
        ]

        rev_bu_totals = [
            {
                'rev_bu_id': rev_bu_id,
                'sales': totals['sales'],
                'rev': totals['rev'],
                'gm': totals['gm'],
                'budget_forecast_id': self.id,
            }
            for rev_bu_id, totals in rev_bu_totals_dict.items()
        ]

        self.env['sales.bu.total'].create(sales_bu_totals)
        self.env['rev.bu.total'].create(rev_bu_totals)

    def generate_comparison(self):
        """
        Generate comparison data for the current record and related comparison records.
        
        This method first clears any existing comparison lines to ensure data accuracy.
        It then creates a grouping key function to group comparison lines by specific fields.
        Using this key, it iterates over all comparison records, including the current record,
        to group and aggregate data from their child records.
        Finally, it processes these grouped data into a format suitable for creating new comparison lines
        and creates them in the database.
        """
        self.ensure_one()  # Ensure the operation is performed on a single record
        self.comparison_line_ids.unlink()  # Clear previous data

        all_budget_forecasts = self + self.comparison_ids

        # Grouping by `partner_id` only to merge the same client
        def _group_key(line):
            return (
                # line.partner_id.id,
                line.label,
                line.type,
                # line.project_type,
                line.sales_bu_id.id,
                line.rev_bu_id.id
            )

        # Dictionary to store grouped comparison lines by partner_id with quarterly values
        line_groups = defaultdict(lambda: defaultdict(float))

        for idx, comp_budget_forecast in enumerate(all_budget_forecasts, 1):
            for line in comp_budget_forecast.budget_forecast_line_ids:
                key = _group_key(line)
                quarter_key = f'q{idx}_'  # q1_, q2_, etc.

                # Summing values per quarter for the same client
                line_groups[key][quarter_key + 'sales'] += line.sales
                line_groups[key][quarter_key + 'rev'] += line.rev
                line_groups[key][quarter_key + 'gm'] += line.gm

        # Prepare data for creating comparison lines
        comparison_lines = [
            {
                # 'partner_id': key[0],
                'label': key[0],
                'type': key[1],
                # 'project_type': key[2],
                'sales_bu_id': key[2],
                'rev_bu_id': key[3],
                'budget_forecast_id': self.id,  # Link to the current record
                **values  # Unpacking quarterly data dynamically
            }
            for key, values in line_groups.items()
        ]

        # Create records in the database
        self.env['comparison.line'].create(comparison_lines)

    budget_forecast_line_count = fields.Integer(
        string="Lines Count",
        compute="_compute_budget_forecast_line_count"
    )

    @api.depends('budget_forecast_line_ids')
    def _compute_budget_forecast_line_count(self):
        for record in self:
            record.budget_forecast_line_count = len(record.budget_forecast_line_ids)

    def action_view_forecast_lines(self):
        self.ensure_one()
        return {
            'name': 'Forecast Lines',
            'type': 'ir.actions.act_window',
            'res_model': 'budget.forecast.line',
            'view_mode': 'tree',
            'domain': [('budget_forecast_id', '=', self.id)],
            'context': {'default_budget_forecast_id': self.id},
            'target': 'current',
        }

    # def generate_comparison(self):
    #     """
    #     Generate comparison data for the current record and related comparison records.
    #
    #     This method first clears any existing comparison lines to ensure data accuracy.
    #     It then creates a grouping key function to group comparison lines by specific fields.
    #     Using this key, it iterates over all comparison records, including the current record,
    #     to group and aggregate data from their child records.
    #     Finally, it processes these grouped data into a format suitable for creating new comparison lines
    #     and creates them in the database.
    #     """
    #     self.ensure_one()  # Ensure the operation is performed on a single record
    #     self.comparison_line_ids.unlink()  # Clear previous data
    #     self.sales_bu_total_ids.unlink()  # Clear previous data
    #     self.rev_bu_total_ids.unlink()  # Clear previous data
    #
    #     all_budget_forecasts = self + self.comparison_ids  # Include current record
    #
    #     # Create grouping key function
    #     def _group_key(line):
    #         """
    #         Generate a unique key for each comparison line.
    #
    #         This key is used to group lines with the same client, label, creator, sector, and business unit.
    #         """
    #         return (
    #             line.partner_id.id,
    #             line.label,
    #             line.create_uid.id,
    #             line.sector_id.id,
    #             line.project_type,
    #             line.sales_bu_id.id,
    #             line.rev_bu_id.id
    #         )
    #
    #     # Initialize a dictionary to store grouped comparison lines
    #     line_groups = defaultdict(dict)
    #     # Iterate over all comparison records to group and aggregate data
    #     for idx, comp_budget_forecast in enumerate(all_budget_forecasts, 1):
    #         for line in comp_budget_forecast.budget_forecast_line_ids:
    #             key = _group_key(line)
    #             budget_forecast_key = f'q{idx}_'
    #             line_groups[key][budget_forecast_key + 'sales'] = line.sales
    #             line_groups[key][budget_forecast_key + 'rev'] = line.rev
    #             line_groups[key][budget_forecast_key + 'gm'] = line.gm
    #             line_groups[key][budget_forecast_key + 'rev_gm'] = line.rev_gm
    #
    #     # Prepare data for creating comparison lines
    #     comparison_lines = []
    #     for key, values in line_groups.items():
    #         line_vals = {
    #             'partner_id': key[0],
    #             'label': key[1],
    #             'create_uid': key[2],
    #             'sector_id': key[3],
    #             'project_type': key[4],
    #             'sales_bu_id': key[5],
    #             'rev_bu_id': key[6],
    #             'budget_forecast_id': self.id,  # Link to current record
    #         }
    #         line_vals.update(values)
    #         comparison_lines.append(line_vals)
    #
    #     # Create records in database
    #     self.env['comparison.line'].create(comparison_lines)
    #
    #     # Grouped totals for Sales BU
    #     sales_bu_totals_dict = defaultdict(lambda: {'sales': 0, 'rev': 0, 'gm': 0, 'rev_gm': 0})
    #     # Grouped totals for Revenue BU
    #     rev_bu_totals_dict = defaultdict(lambda: {'sales': 0, 'rev': 0, 'gm': 0, 'rev_gm': 0})
    #     for budget_forecast in all_budget_forecasts:
    #         for line in budget_forecast.budget_forecast_line_ids:
    #             if line.sales_bu_id:
    #                 sales_bu_totals_dict[line.sales_bu_id.id]['sales'] += line.sales
    #                 sales_bu_totals_dict[line.sales_bu_id.id]['rev'] += line.rev
    #                 sales_bu_totals_dict[line.sales_bu_id.id]['gm'] += line.gm
    #                 sales_bu_totals_dict[line.sales_bu_id.id]['rev_gm'] += line.rev_gm
    #             if line.rev_bu_id:
    #                 rev_bu_totals_dict[line.rev_bu_id.id]['sales'] += line.sales
    #                 rev_bu_totals_dict[line.rev_bu_id.id]['rev'] += line.rev
    #                 rev_bu_totals_dict[line.rev_bu_id.id]['gm'] += line.gm
    #                 rev_bu_totals_dict[line.rev_bu_id.id]['rev_gm'] += line.rev_gm
    #
    #     sales_bu_totals = [
    #         {
    #             'sales_bu_id': sales_bu_id,
    #             'sales': totals['sales'],
    #             'rev': totals['rev'],
    #             'gm': totals['gm'],
    #             'rev_gm': totals['rev_gm'],
    #             'budget_forecast_id': self.id,
    #         }
    #         for sales_bu_id, totals in sales_bu_totals_dict.items()
    #     ]
    #
    #     rev_bu_totals = [
    #         {
    #             'rev_bu_id': rev_bu_id,
    #             'sales': totals['sales'],
    #             'rev': totals['rev'],
    #             'gm': totals['gm'],
    #             'rev_gm': totals['rev_gm'],
    #             'budget_forecast_id': self.id,
    #         }
    #         for rev_bu_id, totals in rev_bu_totals_dict.items()
    #     ]
    #
    #     self.env['sales.bu.total'].create(sales_bu_totals)
    #     self.env['rev.bu.total'].create(rev_bu_totals)


class BudgetAndForecastLine(models.Model):
    _name = 'budget.forecast.line'

    budget_forecast_id = fields.Many2one(comodel_name='budget.forecast', string='Budget and Forecast')
    partner_id = fields.Many2one(comodel_name='res.partner', string='Client', required=True , store=True)
    partner_id_domain = fields.Char(compute="_compute_partner_id_domain")

    @api.depends('budget_forecast_id')
    def _compute_partner_id_domain(self):
        for rec in self:
            clients = []
            partners = self.env['res.partner'].search([('ref', '!=', False)])
            for partner in partners:
                if partner.ref[0] == 'C':
                    clients.append(partner.id)
            rec.partner_id_domain = json.dumps([('id', 'in', clients)])

    label = fields.Char(string='Label', required=True)
    create_uid = fields.Many2one(comodel_name='res.users', string='Created By', default=lambda self: self.env.user,
                                 readonly=True)
    sector_id = fields.Many2one(comodel_name='sector', related='partner_id.sector_id', string='Sector'   ,  store=True  # ✅ Add this
)
    project_type = fields.Selection([('qn', 'QN'), ('ql', 'QL')])
    type = fields.Selection([('adhoc', 'Adhoc'), ('tracker', 'Tracker'), ('syndicated', 'Syndicated'), ('wallet', 'Wallet')])
    sales_bu_id = fields.Many2one(comodel_name='crm.team', string='Sales BU')
    rev_bu_id = fields.Many2one(comodel_name='revenue.team', string='Rev BU')
    sales = fields.Float(string='Sales')
    rev = fields.Float(string='REV')
    gm = fields.Float(string='GM')
    rev_gm = fields.Float(string='GM%', compute='compute_rev_gm',store=True)
    secured_rev = fields.Float(string='Secured REV')
    secured_gm = fields.Float(string='Secured GM')

    tracked_fields = ['sales', 'rev', 'gm', 'rev_gm', 'secured_rev', 'secured_gm']


    @api.depends('rev', 'gm')
    def compute_rev_gm(self):
        for rec in self:
            if rec.rev:
                rec.rev_gm = (rec.gm / rec.rev) * 100
            else:
                rec.rev_gm = 0


    def write(self, vals):
        # Store old values BEFORE writing
        old_values = {
            line.id: {field: line[field] for field in self.tracked_fields if field in vals}
            for line in self
        }

        # Perform the write operation
        res = super(BudgetAndForecastLine, self).write(vals)

        # Post changes to the parent sale.order's chatter
        for line in self:
            if line.budget_forecast_id and old_values.get(line.id):
                message = "<b> Line Updated:</b><br/>"
                message += f"<b>Label:</b> {line.label}<br/>"

                for field in old_values[line.id]:
                    old_value = old_values[line.id][field]
                    new_value = line[field]
                    field_name = self._fields[field].string

                    # Handle special cases (e.g., Many2one fields)
                    if isinstance(self._fields[field], fields.Many2one):
                        old_value = old_value.display_name if old_value else "None"
                        new_value = new_value.display_name if new_value else "None"

                    message += (
                        f"<b>{field_name}:</b> "
                        f"{old_value} → {new_value}<br/>"
                    )

                line.budget_forecast_id.message_post(body=message)
        return res


class ComparisonLine(models.Model):
    _name = 'comparison.line'
    _description = 'Comparison Line'

    budget_forecast_id = fields.Many2one(comodel_name='budget.forecast', string='Budget and Forecast')
    partner_id = fields.Many2one(comodel_name='res.partner', string='Client')
    label = fields.Char(string='Label')
    create_uid = fields.Many2one(comodel_name='res.users', string='Created By', default=lambda self: self.env.user,
                                 readonly=True)
    created_by = fields.Char()
    sector_id = fields.Many2one(comodel_name='sector', related='partner_id.sector_id', string='Sector')
    project_type = fields.Selection([('qn', 'QN'), ('ql', 'QL')])
    type = fields.Selection([('adhoc', 'Adhoc'), ('tracker', 'Tracker'), ('syndicated', 'Syndicated'), ('wallet', 'Wallet')])
    sales_bu_id = fields.Many2one(comodel_name='crm.team', string='Sales BU')
    rev_bu_id = fields.Many2one(comodel_name='revenue.team', string='Rev BU')

    comparison_count = fields.Integer(related='budget_forecast_id.comparison_count', string='Comparison Count')

    # Q1 Fields
    q1_sales = fields.Float(string='Sales (1)')
    q1_rev = fields.Float(string='REV (1)')
    q1_gm = fields.Float(string='GM (1)')
    q1_rev_gm = fields.Float(string='GM% (1)', compute='compute_q1_rev_gm')

    @api.depends('q1_rev', 'q1_gm')
    def compute_q1_rev_gm(self):
        for rec in self:
            if rec.q1_rev:
                rec.q1_rev_gm = (rec.q1_gm / rec.q1_rev) * 100
            else:
                rec.q1_rev_gm = 0

    # Q2 Fields
    q2_sales = fields.Float(string='Sales (2)')
    q2_rev = fields.Float(string='REV (2)')
    q2_gm = fields.Float(string='GM (2)')
    q2_rev_gm = fields.Float(string='GM% (2)', compute='compute_q2_rev_gm')

    @api.depends('q2_rev', 'q2_gm')
    def compute_q2_rev_gm(self):
        for rec in self:
            if rec.q2_rev:
                rec.q2_rev_gm = (rec.q2_gm / rec.q2_rev) * 100
            else:
                rec.q2_rev_gm = 0

    # Q3 Fields
    q3_sales = fields.Float(string='Sales (3)')
    q3_rev = fields.Float(string='REV (3)')
    q3_gm = fields.Float(string='GM (3)')
    q3_rev_gm = fields.Float(string='GM% (3)', compute='compute_q3_rev_gm')

    @api.depends('q3_rev', 'q3_gm')
    def compute_q3_rev_gm(self):
        for rec in self:
            if rec.q3_rev:
                rec.q3_rev_gm = (rec.q3_gm / rec.q3_rev) * 100
            else:
                rec.q3_rev_gm = 0

    # Q4 Fields
    q4_sales = fields.Float(string='Sales (4)')
    q4_rev = fields.Float(string='REV (4)')
    q4_gm = fields.Float(string='GM (4)')
    q4_rev_gm = fields.Float(string='GM% (4)', compute='compute_q4_rev_gm')

    @api.depends('q4_rev', 'q4_gm')
    def compute_q4_rev_gm(self):
        for rec in self:
            if rec.q4_rev:
                rec.q4_rev_gm = (rec.q4_gm / rec.q4_rev) * 100
            else:
                rec.q4_rev_gm = 0

    # Q5 Fields
    q5_sales = fields.Float(string='Sales (5)')
    q5_rev = fields.Float(string='REV (5)')
    q5_gm = fields.Float(string='GM (5)')
    q5_rev_gm = fields.Float(string='GM% (5)', compute='compute_q5_rev_gm')

    @api.depends('q5_rev', 'q5_gm')
    def compute_q5_rev_gm(self):
        for rec in self:
            if rec.q5_rev:
                rec.q5_rev_gm = (rec.q5_gm / rec.q5_rev) * 100
            else:
                rec.q5_rev_gm = 0

    # Q6 Fields
    q6_sales = fields.Float(string='Sales (6)')
    q6_rev = fields.Float(string='REV (6)')
    q6_gm = fields.Float(string='GM (6)')
    q6_rev_gm = fields.Float(string='GM% (6)', compute='compute_q6_rev_gm')

    @api.depends('q6_rev', 'q6_gm')
    def compute_q6_rev_gm(self):
        for rec in self:
            if rec.q6_rev:
                rec.q6_rev_gm = (rec.q6_gm / rec.q6_rev) * 100
            else:
                rec.q6_rev_gm = 0


class SalesBuTotal(models.Model):
    _name = 'sales.bu.total'

    budget_forecast_id = fields.Many2one(comodel_name='budget.forecast', string='Budget and Forecast')
    sales_bu_id = fields.Many2one(comodel_name='crm.team', string='Sales BU')

    sales = fields.Float(string='Sales')
    rev = fields.Float(string='REV')
    gm = fields.Float(string='GM')
    rev_gm = fields.Float(string='GM%', compute='compute_rev_gm')

    @api.depends('rev', 'gm')
    def compute_rev_gm(self):
        for rec in self:
            if rec.rev:
                rec.rev_gm = (rec.gm / rec.rev) * 100
            else:
                rec.rev_gm = 0


class RevBuTotal(models.Model):
    _name = 'rev.bu.total'

    budget_forecast_id = fields.Many2one(comodel_name='budget.forecast', string='Budget and Forecast')
    rev_bu_id = fields.Many2one(comodel_name='revenue.team', string='Rev BU')

    sales = fields.Float(string='Sales')
    rev = fields.Float(string='REV')
    gm = fields.Float(string='GM')
    rev_gm = fields.Float(string='GM%', compute='compute_rev_gm')

    @api.depends('rev', 'gm')
    def compute_rev_gm(self):
        for rec in self:
            if rec.rev:
                rec.rev_gm = (rec.gm / rec.rev) * 100
            else:
                rec.rev_gm = 0
