# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
from collections import defaultdict
from odoo.exceptions import AccessError


class ir_attachment_inherit(models.Model):

    _inherit = 'ir.attachment'

    @api.model
    def check(self, mode, values=None):
        """ Restricts the access to an ir.attachment, according to referred mode """
        if self.env.is_superuser():
            return True
        # Always require an internal user (aka, employee) to access to a attachment
        # if not (self.env.is_admin() or self.env.user.has_group('base.group_user')):
        #     raise AccessError(_("Sorry, you are not allowed to access this document."))
        # collect the records to check (by model)
        model_ids = defaultdict(set)            # {model_name: set(ids)}
        if self:
            # DLE P173: `test_01_portal_attachment`
            self.env['ir.attachment'].flush(['res_model', 'res_id', 'create_uid', 'public', 'res_field'])
            self._cr.execute('SELECT res_model, res_id, create_uid, public, res_field FROM ir_attachment WHERE id IN %s', [tuple(self.ids)])
            for res_model, res_id, create_uid, public, res_field in self._cr.fetchall():
                if public and mode == 'read':
                    continue
                # if not self.env.is_system() and (res_field or (not res_id and create_uid != self.env.uid)):
                #     raise AccessError(_("Sorry, you are not allowed to access this document."))
                if not (res_model and res_id):
                    continue
                model_ids[res_model].add(res_id)
        if values and values.get('res_model') and values.get('res_id'):
            model_ids[values['res_model']].add(values['res_id'])

        # check access rights on the records
        for res_model, res_ids in model_ids.items():
            # ignore attachments that are not attached to a resource anymore
            # when checking access rights (resource was deleted but attachment
            # was not)
            if res_model not in self.env:
                continue
            if res_model == 'res.users' and len(res_ids) == 1 and self.env.uid == list(res_ids)[0]:
                # by default a user cannot write on itself, despite the list of writeable fields
                # e.g. in the case of a user inserting an image into his image signature
                # we need to bypass this check which would needlessly throw us away
                continue
            records = self.env[res_model].browse(res_ids).exists()
            # For related models, check if we can write to the model, as unlinking
            # and creating attachments can be seen as an update to the model
            access_mode = 'write' if mode in ('create', 'unlink') else mode
            records.check_access_rights(access_mode)
            records.check_access_rule(access_mode)

class User(models.Model):
    _inherit = 'res.users'

    allowed_sales_bu_ids = fields.Many2many(comodel_name="crm.team", string="Allowed Sales BU")



# class CRMTeam(models.Model):
#     _inherit = 'crm.team'
#
#     search_ids = fields.Char(compute="_compute_search_ids", search='search_ids_search')
#
#     def _compute_search_ids(self):
#         print('my compute')
#     def search_ids_search(self, operator, operand):
#         obj = self.env['crm.team'].search([('id', 'in', self.env.user.allowed_sales_bu_ids.ids)]).ids
#         return [('id', 'in', obj)]



class SaleOrder(models.Model):
    _inherit = 'sale.order'

    # @api.multi
    def _get_sales_bu_domain(self):
        return [('id', 'in', self.env.user.allowed_sales_bu_ids.ids),'|', ('company_id', '=', False), ('company_id', '=',self.env.company.id)]

    team_id = fields.Many2one(
        'crm.team', 'Sales Team',
        ondelete="set null", tracking=True,
        change_default=True, check_company=True,  # Unrequired company
        domain=_get_sales_bu_domain)

class CRMLead(models.Model):
    _inherit = 'crm.lead'

    # @api.multi
    def _get_sales_bu_domain(self):
        return [('id', 'in', self.env.user.allowed_sales_bu_ids.ids)]

    team_id = fields.Many2one('crm.team', string='Sales Channel', oldname='section_id',
                              default=lambda self: self.env['crm.team'].sudo()._get_default_team_id(
                                  user_id=self.env.uid),
                              index=True, tracking=True,
                              help='When sending mails, the default email address is taken from the sales channel.',
                              domain=_get_sales_bu_domain)

    count_percentage = fields.Float()

    @api.model
    def read_group(self, domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True):
        # overrides the default read_group in order to compute the computed fields manually for the group

        fields_list = {'count_percentage'}


        # Not any of the fields_list support aggregate function like :sum
        def truncate_aggr(field):
            field_no_aggr = field.split(':', 1)[0]
            if field_no_aggr in fields_list:
                return field_no_aggr
            return field

        fields = {truncate_aggr(field) for field in fields}

        # Read non fields_list fields
        result = super(CRMLead, self).read_group(
            domain, list(fields - fields_list), groupby, offset=offset,
            limit=limit, orderby=orderby, lazy=lazy)
        if result:
            last_percentage = sum(item['__count'] for item in result) if '__count' in result[-1] else 0
        else:
            last_percentage = 0

        # Populate result with fields_list values
        if fields_list:
            for group_line in result:

                # initialise fields to compute to 0 if they are requested
                if 'count_percentage' in fields:
                    group_line['count_percentage'] =  (group_line.get('__count') / last_percentage) if last_percentage != 0 else 0

        return result
