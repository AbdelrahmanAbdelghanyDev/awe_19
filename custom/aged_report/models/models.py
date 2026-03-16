# -*- coding: utf-8 -*-

from odoo import models, fields, api
from dateutil import relativedelta
from datetime import datetime


class SaleOrderLineAged(models.Model):
    _inherit = 'sale.order.line'

    is_revenue_button_clicked = fields.Boolean(string='Recognized', readonly=True)
    task_status = fields.Many2one('project.task.type',string='Task Status', readonly=True)


class ProjectTaskAged(models.Model):
    _inherit = 'project.task'

    # @api.constrains('stage_id')
    # def const_stage_id(self):
    #     self.sale_line_id.task_status = self.stage_id.id
    #
    # @api.constrains('is_revenue_button_clicked')
    # def const_recognized(self):
    #     self.sale_line_id.is_revenue_button_clicked = self.is_revenue_button_clicked

    def old_aged(self):
        tasks =self.search([])
        for line in tasks:
            if line.sale_line_id:
                line.sale_line_id.task_status = line.stage_id.id
                line.sale_line_id.is_revenue_button_clicked = line.is_revenue_button_clicked

class InvoiceLineAged(models.Model):
    _inherit = 'account.move.line'

    is_revenue_button_clicked = fields.Boolean(string='Recognized', readonly=True,
                                               related='sale_line_ids.is_revenue_button_clicked')
    task_status = fields.Many2one('project.task.type',string='Task Status', readonly=True,
                                  related='sale_line_ids.task_status')


class InvoiceAged(models.Model):
    _inherit = 'account.move'

    # open_date = fields.Datetime('Invoice Open Date',readonly=True)
    invoice_open_days = fields.Integer('Days of invoice in Open state', default=0,readonly=True)

    def count_days_open_invoice(self):
        invoices = self.sudo().search([('invoice_date','!=',False),('state','!=','paid')])
        for rec in invoices:
            invoice_date = datetime.strptime(rec.invoice_date, '%Y-%m-%d')
            date_now = datetime.strptime(fields.Datetime.now(), '%Y-%m-%d %H:%M:%S')
            diff = relativedelta.relativedelta(date_now,invoice_date).days
            rec.invoice_open_days = diff