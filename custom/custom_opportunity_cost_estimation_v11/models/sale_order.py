from odoo import models, fields, api, _
from odoo.exceptions import UserError, AccessError
from odoo.tools import float_is_zero
from itertools import groupby
import json

class CustomQuotation(models.Model):
    _inherit = 'sale.order'
    parent_opportunity = fields.Many2one(
        'crm.lead', string="parent_opportunity")

    # opportunity_cost_estimation = fields.Many2many(
    #     'opportunity.cost.estimation',
    #     store=True,
    #     domain="[('parent_opportunity.id', '=', parent_opportunity), ('state','=','done')]"
    # )

    opportunity_cost_estimation = fields.Many2many(comodel_name="opportunity.cost.estimation",
                                     relation="opportunity_cost_estimation_sale_order",
                                     column1="sale_order_1", column2="cost_estimation_1",
                                     store=True,
                                     domain="[('parent_opportunity.id', '=', parent_opportunity), ('state','=','done')]"
                                     )
    opportunity_total_cost = fields.Float()
    opportunity_total_cost_2 = fields.Float(
        related='opportunity_total_cost',
        readonly=True
    )

    # project_objective = fields.Many2one('project.objective', string="Project Objective",
    #                                     compute="onchange_parent_opportunity")
    project_type = fields.Selection([
        ('0', 'Adhoc'),
        ('1', 'Tracker'),
        ('2', 'Desk Research'),
        ('3', 'syndicated')
    ], string="Project Type", compute="onchange_parent_opportunity")
    sector_id = fields.Many2one('sector', 'Sector', compute="onchange_parent_opportunity")


    @api.depends('parent_opportunity')
    def onchange_parent_opportunity(self):
        for rec in self:
            if rec.parent_opportunity:
                # rec.project_objective = rec.parent_opportunity.project_objective
                rec.project_type = rec.parent_opportunity.project_type
                rec.sector_id = rec.partner_id.sector_id.id
            else:
                # rec.project_objective = False
                rec.project_type = False
                rec.sector_id = False


    def action_confirm(self):
        res = super(CustomQuotation, self).action_confirm()
        for order in self:
            # order._timesheet_service_generation()
            try:
                # print(order)
                # prints(order.order_line.ids)
                # print(order.tasks_ids)
                order.tasks_ids = self.env['project.task'].search(
                    [('sale_line_id', 'in', order.order_line.ids)])
                # print(order.tasks_ids)
                project_id = order.tasks_ids[0].project_id

                for i in order.opportunity_cost_estimation:
                    for j in i.order_line:
                        project_id.estimation_ids.create({
                            'project_id': project_id.id,
                            'product_id': j.product_id.id,
                            'product_uom': self.env['product.product'].search(
                                [('id', '=', j.product_id.id)]).uom_id.id,
                            'name': self.env['product.product'].search(
                                [('id', '=', j.product_id.id)]).name,
                            'price_unit': j.price_unit,
                            'product_uom_qty': j.product_uom_qty,
                            'parent_cost': i.id,
                        })
                        project_id.tasks_estimations_ids_report.create({
                            'project_id': project_id.id,
                            'product_id': j.product_id.id,
                            'product_uom': self.env['product.product'].search(
                                [('id', '=', j.product_id.id)]).uom_id.id,
                            'name': self.env['product.product'].search([
                                ('id', '=', j.product_id.id)]).name,
                            'price_unit': j.price_unit,
                            'product_uom_qty': j.product_uom_qty,
                            'parent_cost': i.id,
                        })
            except Exception:
                continue

        return res

    #
    @api.onchange('opportunity_cost_estimation')
    def onchange_opportunity_cost_estimation(self):
        tmp_total = 0
        for i in self.opportunity_cost_estimation:
            tmp_total += i.amount_total

        values = {
            'opportunity_total_cost': tmp_total,
        }
        self.update(values)

    @api.onchange('opportunity_id')
    def onchange_opportunity_id(self):
        self.parent_opportunity = self.opportunity_id

    @api.model
    def initiate_field(self):
        sales = self.env['sale.order'].search([])
        for i in sales:
            i.parent_opportunity = i.opportunity_id


    def action_invoice_create(self, grouped=False, final=False):
        """
        Create the invoice associated to the SO.
        :param grouped: if True, invoices are grouped by SO id. If False, invoices are grouped by
                        (partner_invoice_id, currency)
        :param final: if True, refunds will be generated if necessary
        :returns: list of created invoices
        """
        inv_obj = self.env['account.move']
        precision = self.env['decimal.precision'].precision_get('Product Unit of Measure')
        invoices = {}
        references = {}
        invoices_origin = {}
        invoices_name = {}

        for order in self:
            group_key = order.id if grouped else (order.partner_invoice_id.id, order.currency_id.id)
            for line in order.order_line.sorted(key=lambda l: l.qty_to_invoice < 0):
                # if float_is_zero(line.qty_to_invoice, precision_digits=precision):
                #     continue
                if group_key not in invoices:
                    inv_data = order._prepare_invoice()
                    invoice = inv_obj.create(inv_data)
                    references[invoice] = order
                    invoices[group_key] = invoice
                    invoices_origin[group_key] = [invoice.invoice_origin]
                    invoices_name[group_key] = [invoice.name]
                elif group_key in invoices:
                    if order.name not in invoices_origin[group_key]:
                        invoices_origin[group_key].append(order.name)
                    if order.client_order_ref and order.client_order_ref not in invoices_name[group_key]:
                        invoices_name[group_key].append(order.client_order_ref)

                # if line.qty_to_invoice > 0:
                #     line.invoice_line_create(invoices[group_key].id, line.qty_to_invoice)
                # elif line.qty_to_invoice < 0 and final:
                #     line.invoice_line_create(invoices[group_key].id, line.qty_to_invoice)

            if references.get(invoices.get(group_key)):
                if order not in references[invoices[group_key]]:
                    references[invoices[group_key]] |= order

        for group_key in invoices:
            invoices[group_key].write({'name': ', '.join(invoices_name[group_key]),
                                       'invoice_origin': ', '.join(invoices_origin[group_key])})

        # if not invoices:
        #     raise UserError(_('There is no invoiceable line.'))

        for invoice in invoices.values():
            # invoice.compute_taxes()
            # if not invoice.invoice_line_ids:
            #     raise UserError(_('There is no invoiceable line.'))
            # If invoice is negative, do a refund invoice instead
            if invoice.amount_total < 0:
                invoice.move_type = 'out_refund'
                for line in invoice.invoice_line_ids:
                    line.quantity = -line.quantity
            # Use additional field helper function (for account extensions)
            for line in invoice.invoice_line_ids:
                line._set_additional_fields(invoice)
            # Necessary to force computation of taxes and cash rounding. In account_invoice, they are triggered
            # by onchanges, which are not triggered when doing a create.
            # invoice.compute_taxes()
            # invoice._onchange_cash_rounding()
            # invoice.message_post_with_view('mail.message_origin_link',
            #                                values={'self': invoice, 'origin': references[invoice]},
            #                                subtype_id=self.env.ref('mail.mt_note').id)
        return [inv.id for inv in invoices.values()]



# new todo

    def _get_invoiceable_lines(self, final=False):
        """Return the invoiceable lines for order `self`."""
        down_payment_line_ids = []
        invoiceable_line_ids = []
        pending_section = None
        precision = self.env['decimal.precision'].precision_get('Product Unit of Measure')

        for line in self.order_line:
            print("line :>",line.display_type)
            print("line.product_uom_qty :>",line.product_uom_qty)

            if line.display_type == 'line_section':
                # Only invoice the section if one of its lines is invoiceable
                pending_section = line
                continue
            # if line.display_type != 'line_note' :
            #     continue
            # if  line.display_type == 'line_note':
            print("line.product_uom_qty:> ",line.product_uom_qty)
            if line.product_uom_qty > 0 or line.display_type == 'line_note':
                if line.is_downpayment:
                    # Keep down payment lines separately, to put them together
                    # at the end of the invoice, in a specific dedicated section.
                    down_payment_line_ids.append(line.id)
                    continue
                if pending_section:
                    invoiceable_line_ids.append(pending_section.id)
                    pending_section = None
                print("line.id :> ",line.id)
                invoiceable_line_ids.append(line.id)
            print("invoiceable_line_ids :>",invoiceable_line_ids)
        return self.env['sale.order.line'].browse(invoiceable_line_ids + down_payment_line_ids)


    def _create_invoices(self, grouped=False, final=False, date=None):
        """
        Create the invoice associated to the SO.
        :param grouped: if True, invoices are grouped by SO id. If False, invoices are grouped by
                        (partner_invoice_id, currency)
        :param final: if True, refunds will be generated if necessary
        :returns: list of created invoices
        """
        if not self.env['account.move'].check_access_rights('create', False):
            try:
                self.check_access_rights('write')
                self.check_access_rule('write')
            except AccessError:
                return self.env['account.move']

        # 1) Create invoices.
        invoice_vals_list = []
        invoice_item_sequence = 0 # Incremental sequencing to keep the lines order on the invoice.
        for order in self:
            order = order.with_company(order.company_id)
            current_section_vals = None
            down_payments = order.env['sale.order.line']

            invoice_vals = order._prepare_invoice()
            invoiceable_lines = order._get_invoiceable_lines(final)
            print("invoiceable_lines :> ",invoiceable_lines)

            if not any(not line.display_type for line in invoiceable_lines):
                continue

            invoice_line_vals = []
            down_payment_section_added = False
            for line in invoiceable_lines:
                if not down_payment_section_added and line.is_downpayment:
                    # Create a dedicated section for the down payments
                    # (put at the end of the invoiceable_lines)
                    invoice_line_vals.append(
                        (0, 0, order._prepare_down_payment_section_line(
                            sequence=invoice_item_sequence,
                        )),
                    )
                    down_payment_section_added = True
                    invoice_item_sequence += 1
                invoice_line_vals.append(
                    (0, 0, line._prepare_invoice_line(
                        sequence=invoice_item_sequence,
                    )),
                )
                invoice_item_sequence += 1

            invoice_vals['invoice_line_ids'] += invoice_line_vals
            invoice_vals_list.append(invoice_vals)

        if not invoice_vals_list:
            raise self._nothing_to_invoice_error()

        # 2) Manage 'grouped' parameter: group by (partner_id, currency_id).
        if not grouped:
            new_invoice_vals_list = []
            invoice_grouping_keys = self._get_invoice_grouping_keys()
            invoice_vals_list = sorted(
                invoice_vals_list,
                key=lambda x: [
                    x.get(grouping_key) for grouping_key in invoice_grouping_keys
                ]
            )
            for grouping_keys, invoices in groupby(invoice_vals_list, key=lambda x: [x.get(grouping_key) for grouping_key in invoice_grouping_keys]):
                origins = set()
                payment_refs = set()
                refs = set()
                ref_invoice_vals = None
                for invoice_vals in invoices:
                    if not ref_invoice_vals:
                        ref_invoice_vals = invoice_vals
                    else:
                        ref_invoice_vals['invoice_line_ids'] += invoice_vals['invoice_line_ids']
                    origins.add(invoice_vals['invoice_origin'])
                    payment_refs.add(invoice_vals['payment_reference'])
                    refs.add(invoice_vals['ref'])
                ref_invoice_vals.update({
                    'ref': ', '.join(refs)[:2000],
                    'invoice_origin': ', '.join(origins),
                    'payment_reference': len(payment_refs) == 1 and payment_refs.pop() or False,
                })
                new_invoice_vals_list.append(ref_invoice_vals)
            invoice_vals_list = new_invoice_vals_list

        # 3) Create invoices.

        # As part of the invoice creation, we make sure the sequence of multiple SO do not interfere
        # in a single invoice. Example:
        # SO 1:
        # - Section A (sequence: 10)
        # - Product A (sequence: 11)
        # SO 2:
        # - Section B (sequence: 10)
        # - Product B (sequence: 11)
        #
        # If SO 1 & 2 are grouped in the same invoice, the result will be:
        # - Section A (sequence: 10)
        # - Section B (sequence: 10)
        # - Product A (sequence: 11)
        # - Product B (sequence: 11)
        #
        # Resequencing should be safe, however we resequence only if there are less invoices than
        # orders, meaning a grouping might have been done. This could also mean that only a part
        # of the selected SO are invoiceable, but resequencing in this case shouldn't be an issue.
        if len(invoice_vals_list) < len(self):
            SaleOrderLine = self.env['sale.order.line']
            for invoice in invoice_vals_list:
                sequence = 1
                for line in invoice['invoice_line_ids']:
                    line[2]['sequence'] = SaleOrderLine._get_invoice_line_sequence(new=sequence, old=line[2]['sequence'])
                    sequence += 1

        # Manage the creation of invoices in sudo because a salesperson must be able to generate an invoice from a
        # sale order without "billing" access rights. However, he should not be able to create an invoice from scratch.
        moves = self.env['account.move'].sudo().with_context(default_move_type='out_invoice').create(invoice_vals_list)

        # 4) Some moves might actually be refunds: convert them if the total amount is negative
        # We do this after the moves have been created since we need taxes, etc. to know if the total
        # is actually negative or not
        if final:
            moves.sudo().filtered(lambda m: m.amount_total < 0).action_switch_invoice_into_refund_credit_note()
        for move in moves:
            move.message_post_with_view('mail.message_origin_link',
                values={'self': move, 'origin': move.line_ids.mapped('sale_line_ids.order_id')},
                subtype_id=self.env.ref('mail.mt_note').id
            )
        return moves


class CustomSaleOrderLine(models.Model):
    _name = 'custom.sale.order.line'
    _inherit = 'sale.order.line'

    order_id = fields.Many2one(
        'sale.order',
        required=False,
        ondelete='cascade',
        index=True,
        copy=False
    )
    parent_cost = fields.Many2one(
        'opportunity.cost.estimation',
        string='parent_cost'
    )

    product_uom_qty = fields.Float(string='Quantity',digits = (16, 2), required=True,
                                   default=0.0)

    no_of_waves = fields.Integer(default=1)  # Based on customer request.
    no_of_units = fields.Float(default=1)  # Based on customer request.
    # Based on customer request.
    price_subtotal_new = fields.Float(compute='_amount_subtotal_new')

    # used for estimation line in tasks.
    actual_qty = fields.Float(default=0)
    actual_unit_price = fields.Float(default=0)
    actual_total = fields.Float(compute='_amount_actual_total')

    @api.depends('actual_qty', 'actual_qty')
    def _amount_actual_total(self):
        for i in self:
            i.actual_total = i.actual_qty * i.actual_unit_price

    @api.depends('product_uom_qty', 'price_unit')
    def _amount_subtotal_new(self):
        for i in self:
            i.price_subtotal_new = i.product_uom_qty * i.price_unit

    @api.depends('product_uom_qty', 'discount', 'price_unit', 'tax_ids', 'no_of_waves', 'price_subtotal_new',
                 'no_of_units')
    def _compute_amount(self):
        """
        Compute the amounts of the SO line.
        """
        for line in self:
            price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
            taxes = line.tax_ids.compute_all(
                price_unit=price * line.no_of_units * line.no_of_waves,
                currency=line.order_id.currency_id,
                quantity=line.product_uom_qty,
                product=line.product_id,
                partner=line.order_id.partner_shipping_id
            )
            line.update({
                'price_tax': taxes['total_included'] - taxes['total_excluded'],
                'price_total': taxes['total_included'],
                'price_subtotal': line.price_subtotal_new * line.no_of_waves,
            })


    invoice_lines = fields.Many2many(comodel_name="account.move.line", relation="account_line_sale_line", column1="account_line_1", column2="sale_line_1", string="", )


class SaleOrderLineInhd(models.Model):
    _inherit = 'sale.order.line'

    def invoice_line_create(self, invoice_id, qty):
        """ Create an invoice line. The quantity to invoice can be positive (invoice) or negative (refund).
            :param invoice_id: integer
            :param qty: float quantity to invoice
            :returns recordset of account.invoice.line created
        """
        invoice_lines = self.env['account.move.line']
        precision = 2
        for line in self:
            if not float_is_zero(qty, precision_digits=precision):
                vals = line._prepare_invoice_line(qty=qty)
                vals.update({'invoice_id': invoice_id, 'sale_line_ids': [(6, 0, [line.id])]})
                invoice_lines |= self.env['account.move.line'].create(vals)
        return invoice_lines

    def _prepare_invoice_line(self, **optional_values):
        """
        Prepare the dict of values to create the new invoice line for a sales order line.

        :param qty: float quantity to invoice
        :param optional_values: any parameter that should be added to the returned invoice line
        """
        self.ensure_one()
        res = {
            'display_type': self.display_type,
            'sequence': self.sequence,
            'name': self.name,
            'product_id': self.product_id.id,
            'product_uom_id': self.product_uom.id,
            'quantity': self.product_uom_qty,
            'discount': self.discount,
            'price_unit': self.price_unit,
            'tax_ids': [(6, 0, self.tax_ids.ids)],
            'analytic_tag_ids': [(6, 0, self.analytic_tag_ids.ids)],
            'sale_line_ids': [(4, self.id)],
        }
        if self.order_id.analytic_account_id:
            res['analytic_account_id'] = self.order_id.analytic_account_id.id
        if optional_values:
            res.update(optional_values)
        if self.display_type:
            res['account_id'] = False
        return res

    def _timesheet_create_task_prepare_values(self, project):
        self.ensure_one()
        planned_hours = self._convert_qty_company_hours(self.company_id)
        sale_line_name_parts = self.name.split('\n')
        title = sale_line_name_parts[0] or self.product_id.name
        description = '<br/>'.join(sale_line_name_parts[1:])
        return {
            'name': self.order_id.name + " / " + title if project.sale_line_id else '%s: %s' % (self.order_id.name or '', title),
            'planned_hours': planned_hours,
            'partner_id': self.order_id.partner_id.id,
            'email_from': self.order_id.partner_id.email,
            'description': description,
            'project_id': project.id,
            'sale_line_id': self.id,
            'sale_order_id': self.order_id.id,
            'company_id': project.company_id.id,
            'user_ids': False,  # force non assigned task, as created as sudo()
        }
