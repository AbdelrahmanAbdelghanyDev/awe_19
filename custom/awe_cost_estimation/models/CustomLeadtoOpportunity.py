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


class CustomLeadtoOpportunity(models.TransientModel):
    _inherit = 'crm.lead2opportunity.partner'
    executive_team_id = fields.Many2one('executive.team')
    revenue_team_id = fields.Many2one('revenue.team')


    def _convert_opportunity(self, vals):
        self.ensure_one()

        res = False

        leads = self.env['crm.lead'].browse(vals.get('lead_ids'))
        for lead in leads:
            self_def_user = self.with_context(default_user_id=self.user_id.id)
            partner_id = self_def_user._create_partner(
                lead.id,
                self.action,
                vals.get('partner_id') or lead.partner_id.id
            )
            res = lead.convert_opportunity(partner_id, [], False)
        user_ids = vals.get('user_ids')

        leads_to_allocate = leads
        if self._context.get('no_force_assignation'):
            leads_to_allocate = leads_to_allocate.filtered(
                lambda lead: not lead.user_id)

        if user_ids:
            leads_to_allocate.allocate_salesman(
                user_ids,
                team_id=(vals.get('team_id')),
                executive_team_id=(
                    vals.get('executive_team_id')),
                revenue_team_id=(vals.get('revenue_team_id')),
            )

        return res


    def action_apply(self):
        """ Convert lead to opportunity or merge lead and opportunity and open
            the freshly created opportunity view.
        """
        self.ensure_one()
        values = {
            'team_id': self.team_id.id,
            'executive_team_id': self.executive_team_id.id,
            'revenue_team_id': self.revenue_team_id.id,
        }

        if self.partner_id:
            values['partner_id'] = self.partner_id.id

        if self.name == 'merge':
            leads = self.opportunity_ids.merge_opportunity()
            if leads.type == "lead":
                values.update(
                    {'lead_ids': leads.ids, 'user_ids': [self.user_id.id]})
                self.with_context(
                    active_ids=leads.ids)._convert_opportunity(values)
            elif not self._context.get('no_force_assignation') or not leads.user_id:
                values['user_id'] = self.user_id.id
                leads.write(values)
        else:
            leads = self.env['crm.lead'].browse(
                self._context.get('active_ids', []))
            values.update(
                {'lead_ids': leads.ids, 'user_ids': [self.user_id.id]})
            self._convert_opportunity(values)

        return leads[0].redirect_opportunity_view()

