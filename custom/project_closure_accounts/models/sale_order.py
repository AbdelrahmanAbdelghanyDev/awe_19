from odoo import models, fields, api
from datetime import datetime , timedelta



class SaleOrder(models.Model):
    _inherit = 'sale.order'


    def action_confirm(self):
        """ revenue and tag . """
        result = super(SaleOrder, self).action_confirm()
        # flag = self.env['res.users'].has_group('project_closure_accounts.group_project_task_revenue')
        # if not flag:
        #     return result
        for order in self.order_line:
            task = self.env['project.task'].search([('sale_line_id', '=', order.id)])
            if task:
                # rate = self.env['res.currency.rate'].search([()])
            # task.original_currency = order.currency_id.id
            # task.base_currency = self.env.user.company_id.currency_id.id  # task.sale_line_id.company_id.currency_id.id
            #     if (order.company_id.currency_id.rate!= 0):
            #         converted_revenue = order.price_subtotal / order.company_id.currency_id.rate#order.currency_id.rate
                if order.currency_id.id != self.env.user.company_id.currency_id.id and order.currency_id.rate != 0:
                    converted_revenue = order.price_subtotal / order.currency_id.rate
                else:
                    converted_revenue = order.price_subtotal
                print('action confirm converted revenue!!', converted_revenue)
                DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
                date_field1 = datetime.strptime(str(self.date_order), DATETIME_FORMAT)
                task.write({'revenue': order.price_subtotal,
                            'original_currency_id': order.currency_id.id,
                            'converted_revenue': converted_revenue,
                            'order_date': self.date_order,
                            'traveling_time':str(date_field1 + timedelta(days=45, hours=0, minutes=0)),
                            'Revenue_bu':self.revenue_team_id.id,
                            'Sales_bu':self.team_id.id,
                            'executive_person': self.executive_team_id.id
                            })
                for tag in self.tag_ids:
                    task.write({'tag_id': tag.id})
        return result
