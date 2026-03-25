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

class SaleORderInh(models.Model):
    _inherit = 'sale.order'

    project_objective = fields.Many2one('project.objective')


class CustomCRMLead(models.Model):
    _inherit = 'crm.lead'

    phone = fields.Char(tracking=False)
    email_from = fields.Char(tracking=False)


    partner_phone = fields.Char(string="Phone", related='partner_id.phone',tracking=False)
    partner_email = fields.Char(string="Email", related='partner_id.email',tracking=False)

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        if self.partner_id:
            self.partner_phone = self.partner_id.phone
            self.partner_email = self.partner_id.email

    def _get_domain_research(self):

        return [('company_id', '=', self.env.user.company_id.id), ('name', 'in', ['QL', 'QN'])]

    executive_team_id = fields.Many2one('executive.team')
    revenue_team_id = fields.Many2one('revenue.team')
    project_objective = fields.Many2one('project.objective')
    working_country = fields.Many2one(
        'res.country', string="Filed Work Country")
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
    length_of_interview = fields.Char('Length of Interview')
    length_of_interview_sel = fields.Selection(
        [('15', '15'), ('15-30', '15-30'), ('30-45', '40-45'), ('45-60', '45-60'), ('60', '60+')],
        string='Length of Interview in Minutes'
    )

    translation = fields.Selection(
        [('yes', 'Yes'), ('no', 'No')],
        string="Simultaneous Translation"
    )
    other_translation = fields.Char(
        string="Other Translation"
    )
    dp = fields.Selection([('yes', 'Yes'), ('no', 'No')])
    reporting = fields.Selection([('yes', 'Yes'), ('no', 'No')])
    presentation = fields.Selection([('yes', 'Yes'), ('no', 'No')])
    viewing_facility = fields.Selection([('yes', 'Yes'), ('no', 'No')])
    client_attendance = fields.Selection([('yes', 'Yes'),
                                          ('no', 'No')])
    project_type = fields.Selection([
        ('0', 'Adhoc'),
        ('1', 'Tracker'),
        ('2', 'Desk Research'),
        ('3', 'syndicated')
    ])
    objective = fields.Char('Objective')
    methodology = fields.Char('Methodology', compute='_compute_methodology', readonly=True)
    methodology_desc = fields.Char('Methodology Desc')
    criteria_usage = fields.Text('Criteria / Usage')
    sample_size_text = fields.Float('Sample Size', compute='_compute_sample_size', readonly=True)
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
    research_type_id = fields.Many2one('product.category', required=True, domain=_get_domain_research)
    research_type_name = fields.Char(
        'Reaseach Type Name',
        related="research_type_id.name",
        readonly=True,
    )
    research_type_company = fields.Many2one('res.company', related="research_type_id.company_id", readonly=True, )

    details = fields.Text("Other Details:")
    details_ql = fields.Text("Other Details:")
    data_capture = fields.Selection([('capi', 'CAPI'),
                                     ('papi', 'PAPI')])

    project_objective = fields.Many2one('project.objective')
    restore_done = fields.Boolean(string="restore done", default=False)


    def restore_ql(self):
        records = self.env['crm.lead'].search([])
        for record in records:
            for line in record.pdt_line:
                if line.pdt_crm_research_id == 'QL':
                    print("hhahahahahahhahhah", line.pdt_crm_2, line.pdt_crm)
                    line.pdt_crm_2 = line.pdt_crm

            record.restore_done = True

    @api.onchange('pdt_line', 'product_line')

    def _compute_sample_size(self):
        total = 0.0

        for record in self:

            for rec in record.pdt_line:
                total += rec.product_uom_qty
            for rec_qn in record.product_line:
                quantity = 0
                if record.research_type_name == 'QN':
                    quantity = rec_qn.quantity_qn
                if record.research_type_name == 'QL':
                    quantity = rec_qn.quantity
                total += quantity
            record.sample_size_text = total

    @api.onchange('product_line', 'pdt_line')

    def _compute_methodology(self):
        for rec in self:
            rec.methodology = ''
        if self.product_line and not self.pdt_line:
            for record in self:
                record.methodology = ''
                if record.cost_estimation_number > 0 and record.product_line:
                    record.methodology = record.product_line[0].product_id.name
                else:
                    if record.product_line:
                        record.methodology = record.product_line[0].product_id.name
        if self.pdt_line:
            for record in self:
                record.methodology = record.pdt_line[0].product_id.name

    @api.onchange('research_type_id')
    def onchange_research_id(self):
        obj = self.research_type_id
        while True:
            if not obj.parent_id:
                self.research_type_name = obj.name
                return {'research_type_name': obj.name}
            else:
                # print()
                obj = obj.parent_id

    def new_cost_estimation(self):
        vals = {'partner_id': self.partner_id.id,
                'client_attendence_region_ids': [(6, 0, self.client_attendence_region_ids.ids)],
                'viewing_facility': self.viewing_facility,
                'transcript': self.transcript,
                'no_of_client_attendees': self.no_of_client_attendees,
                'translation': self.translation,
                'ex_transcript': self.ex_transcript,
                'printing_material': self.printing_material,
                'transcript_lang': self.transcript_lang,
                'other_translation': self.other_translation,
                'no_of_units_attendees': self.no_of_units_attendees,
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
                'length_of_interview': self.length_of_interview,
                'dp': self.dp,
                'reporting': self.reporting,
                'presentation': self.presentation,
                'client_attendance': self.client_attendance,
                'details': self.details,
                'estimation_type': self.research_type_id.id,
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
                'fw_country': i.fw_country.id,
                'project_objective': i.project_objective.id,
                'research_type': i.research_type,
                'data_capture': i.data_capture,
                'gender': i.gender,
                'sec': i.sec,
                'age': i.age,
                'number_of_legs': i.number_of_legs,
                'client_attendance': i.client_attendance,
            }

            product.create(product_value)

        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'opportunity.cost.estimation',
            'target': 'current',
            'res_id': estimation.id,
            'views': [(self.env.ref(
                'custom_opportunity_cost_estimation_v11.opportunity_cost_estimation_form').id,
                       'form')],
        }


    def allocate_salesman(self, user_ids=None, team_id=False, executive_team_id=False, revenue_team_id=False):
        """ Assign salesmen and salesteam to a batch of leads.  If there are more
            leads than salesmen, these salesmen will be assigned in round-robin.
            E.g.: 4 salesmen (S1, S2, S3, S4) for 6 leads (L1, L2, ... L6).  They
            will be assigned as followed: L1 - S1, L2 - S2, L3 - S3, L4 - S4,
            L5 - S1, L6 - S2.

            :param list ids: leads/opportunities ids to process
            :param list user_ids: salesmen to assign
            :param int team_id: salesteam to assign
            :return bool
        """
        index = 0
        for lead in self:
            value = {}
            if team_id:
                value['team_id'] = team_id
            if executive_team_id:
                value['executive_team_id'] = executive_team_id
            if revenue_team_id:
                value['revenue_team_id'] = revenue_team_id
            if user_ids:
                value['user_id'] = user_ids[index]
                # Cycle through user_ids
                index = (index + 1) % len(user_ids)
            if value:
                lead.write(value)
        return True


    # new todo 26/10/2022
    name = fields.Char(
        'Opportunity', index=True, required=True,
        readonly=False, store=True)

    @api.depends('partner_id')
    def _compute_name(self):
        for lead in self:
            if not lead.name and lead.partner_id and lead.partner_id.name:
                lead.name = ''