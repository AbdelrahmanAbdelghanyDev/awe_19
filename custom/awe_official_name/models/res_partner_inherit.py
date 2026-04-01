from odoo import models, fields, api


class awe_res_partner_inherit(models.Model):
    _inherit = 'res.partner'
    _rec_name = 'official_name'

    official_name = fields.Char(string='Official Name')
    cr_numb = fields.Char(string="CR Number", required=False)

    #
    # def name_get(self):
    #     new_format=[]
    #     for degree in self:
    #         new_info+=degree.official_name
    #         new_format.append((degree.id,new_info))
    #     return new_format

    #
    # def name_get(self):
    #     result = super(awe_res_partner_inherit, self).name_get()
    #     if self.official_name:
    #         for rec in self:
    #            result.append((rec.id, rec.official_name))
    #     return result

   #
   #  def name_get(self):
   #      if self.env.context.get('display_full_name', False):
   #          pass
   #      else:
   #          return super(Document, self).name_get()
   #
   # @ api.multi
   # def name_get(self):
   #          if self.env.context.get('name_show_user'):
   #              res = []
   #              for task in self:
   #                  res.append(
   #                (task.id, "[%s] %s" % (task.user_id.name, task.name)))
   #                  return res
   #              return super(ProjectTask, self).name_get()


