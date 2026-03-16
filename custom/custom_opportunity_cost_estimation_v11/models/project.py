from odoo import models, fields, api
# from odoo.exceptions import UserError


class CustomProjectTask(models.Model):
    _inherit = "project.task"

    estimation_ids = fields.One2many(
        'custom.task.est.line',
        'task_id',
        string="estimation_line"
    )


    def to_warehouse(self):
        lines = self.env['custom.task.est.line'].search(
            [('task_id', '=', self.id)])
        products = []
        for i in lines:
            if i.to_WH and not i.done_to_WH:
                products.append((0, 0, {
                    'product_id': i.product_id.id,
                    'product_uom': i.product_uom.id,
                    'name': i.name,
                    'product_uom_qty': i.actual_qty,
                }))
                i.done_to_WH = True

        vals = {
            'picking_type_id': self.env.ref(
                "custom_opportunity_cost_estimation_v11.custom_warehouse_operation").id,
            'location_id': self.env.ref("stock.stock_location_stock").id,
            'location_dest_id': self.env.ref(
                "custom_opportunity_cost_estimation_v11.custom_warehouse_location").id,
            'move_lines': products,
            'origin': self.project_id.name + '/' + self.name,
        }
        self.env['stock.picking'].create(vals)

    # @api.onchange('estimation_ids')
    # def onchange_estimation_ids(self):
    #     pass


class CustomProjectReport(models.Model):
    _name = "project.custom.estimation"
    _inherit = 'custom.sale.order.line'

    order_id = fields.Many2one(
        'sale.order',
        required=False,
        ondelete='cascade',
        index=True,
        copy=False
    )
    task_id = fields.Many2one('project.task')
    project_id = fields.Many2one('project.project')
    task_name = fields.Char(string="Tasks")
    combined = fields.Boolean(string="Combined Line")
    exceed_limit = fields.Boolean()
    is_used = fields.Boolean(default=False)

    total_actual_qty = fields.Float()
    total_actual_total = fields.Float()


    def show_details(self):
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'tree',
            'view_mode': 'tree',
            'res_model': 'custom.task.est.line',
            'target': 'new',
            'views': [(self.env.ref(
                'custom_opportunity_cost_estimation_v11.custom_task_estimation_line_tree').id,
                'tree')],
            "domain": [["project_id", "=", self.project_id.id],
                       ["parent_cost", "=", self.parent_cost.id],
                       ["product_id", "=", self.product_id.id]],
        }

    invoice_lines = fields.Many2many(comodel_name="account.move.line", relation="account_line_sale_line_2", column1="account_line_2", column2="sale_line_2", string="", )
class CustomProjectProject(models.Model):
    _inherit = "project.project"

    estimation_ids = fields.One2many(
        'custom.project.est.line',
        'project_id'
    )
    tasks_estimations_ids = fields.One2many(
        'custom.task.est.line',
        'project_id'
    )

    tasks_estimations_ids_report = fields.One2many(
        'project.custom.estimation',
        'project_id'
    )


    def to_warehouse(self):
        lines = self.env['custom.task.est.line'].search(
            [('project_id', '=', self.id)])
        products = []
        for i in lines:
            if i.to_WH and not i.done_to_WH:
                products.append((0, 0, {'product_id': i.product_id.id,
                                        'product_uom': i.product_uom.id,
                                        'name': i.name,
                                        'product_uom_qty': i.actual_qty,
                                        }))
                i.done_to_WH = True

        vals = {
            'picking_type_id': self.env.ref(
                "custom_opportunity_cost_estimation_v11.custom_warehouse_operation").id,
            'location_id': self.env.ref("stock.stock_location_stock").id,
            'location_dest_id': self.env.ref(
                "custom_opportunity_cost_estimation_v11.custom_warehouse_location").id,
            'move_lines': products,
            'origin': self.name,
        }
        self.env['stock.picking'].create(vals)
