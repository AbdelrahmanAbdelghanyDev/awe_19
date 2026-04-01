# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class SaleOrder(models.Model):
    _name = 'sale.order'
    _inherit = 'sale.order'

    def action_button_request_for_approval(self):

        manager_value = self.env["ir.config_parameter"].sudo().get_param(
            'custom_sale_approval_v11.managerrequired')

        officer_value = self.env["ir.config_parameter"].sudo().get_param(
            'custom_sale_approval_v11.officerrequired')

        final_manager_value = bool(manager_value)
        final_officer_value = bool(officer_value)

        flag_officer = self.env['res.users'].has_group(
            'custom_sale_approval_v11.group_sale_approval_officer')

        flag_agent = self.env['res.users'].has_group(
            'custom_sale_approval_v11.group_sale_approval_agent')

        if flag_officer is True:
            return self.write({'state': 'manager_approval'})

        elif flag_agent is True:
            if (
                (final_officer_value is True) or
                (final_officer_value is False and final_manager_value is False)
            ):
                return self.write({'state': 'officer_approval'})
            else:
                return self.write({'state': 'manager_approval'})
        else:
            raise UserError("You don't have the required authority for this action, Please contact the administrator")

    def action_button_reject(self):
        so_obj = self.browse(self.id)
        if not so_obj.note:
            raise UserError("You have to write down a note (Reject Reason).")
        else:
            return self.write({'state': 'rejected'})

    def action_confirm(self):

        so_obj = self.browse(self.id)

        manager_value = self.env["ir.config_parameter"].sudo().get_param(
            'custom_sale_approval_v11.managerrequired')

        officer_value = self.env["ir.config_parameter"].sudo().get_param(
            'custom_sale_approval_v11.officerrequired')

        final_manager_value = bool(manager_value)
        final_officer_value = bool(officer_value)

        flag_manager = self.env['res.users'].has_group(
            'custom_sale_approval_v11.group_sale_approval_manager')

        flag_officer = self.env['res.users'].has_group(
            'custom_sale_approval_v11.group_sale_approval_officer')

        flag_agent = self.env['res.users'].has_group(
            'custom_sale_approval_v11.group_sale_approval_agent')

        if (flag_manager is True):
            return super(SaleOrder, self).action_confirm()

        elif (flag_officer is True and so_obj.state != 'manager_approval'):
            if (final_manager_value is False):
                return super(SaleOrder, self).action_confirm()
            else:
                raise UserError("You have to request for approval first, As you don't have the authority")

        elif (flag_agent is True):
            if (final_manager_value is False and final_officer_value is False):
                return super(SaleOrder, self).action_confirm()
            else:
                raise UserError("You have to request for approval first, As you don't have the required authority")

        else:
            raise UserError("You don't have the required authority, Please contact the administrator")

    state = fields.Selection([
        ('draft', 'Draft Quotation'),
        ('sent', 'Quotation Sent'),
        ('cancel', 'Cancelled'),
        ('done', 'Done'),
        ('waiting_date', 'Waiting Schedule'),
        ('sale', 'Sales Order'),
        ('manager_approval', 'Manager Approval'),
        ('manual', 'Sale to Invoice'),
        ('officer_approval', 'Senior Approval'),
        ('shipping_except', 'Shipping Exception'),
        ('invoice_except', 'Invoice Exception'),
        ('rejected', 'Rejected'),
    ], 'Status', readonly=True, copy=False, select=True)


class AutoSaleSettings(models.TransientModel):

    _inherit = 'res.config.settings'

    managerrequired = fields.Boolean(
        string="Require Manager Approval",
    )

    officerrequired = fields.Boolean(
        string="Require Senior Approval",
    )

    @api.model
    def get_values(self):
        res = super(AutoSaleSettings, self).get_values()
        ICPSudo = self.env['ir.config_parameter'].sudo()

        managerrequired = ICPSudo.get_param(
            'custom_sale_approval_v11.managerrequired')

        officerrequired = ICPSudo.get_param(
            'custom_sale_approval_v11.officerrequired')

        res.update(
            managerrequired=bool(managerrequired),
            officerrequired=bool(officerrequired),
        )
        return res

    def set_values(self):
        super(AutoSaleSettings, self).set_values()
        ICPSudo = self.env['ir.config_parameter'].sudo()
        ICPSudo.set_param(
            'custom_sale_approval_v11.managerrequired', self.managerrequired)
        ICPSudo.set_param(
            'custom_sale_approval_v11.officerrequired', self.officerrequired)