from odoo import models, fields, api

class make_new_pdt_line(models.Model):
    _inherit = 'crm.lead'

    pdt_line_ql = fields.One2many('crm.product_line', 'pdt_crm_2', string="Product of qr")



    def new_cost_estimation(self):
      if self.pdt_line and self.research_type_id.name=="QN":
           vals = {'partner_id': self.partner_id.id,
                   'client_attendence_region_ids': [(6, 0 ,self.client_attendence_region_ids.ids)],
                   'criteria_usage':self.criteria_usage,
                   'objective':self.objective,
                   'sample_size_text':self.sample_size_text,
                   'sample_struct_per_reg':self.sample_struct_per_reg,
                   'sample_struct_per_sec':self.sample_struct_per_sec,
                   'sample_struct_per_age':self.sample_struct_per_age,
                   'sample_struct_per_gen':self.sample_struct_per_gen,
                   'sample_struct_per_bra':self.sample_struct_per_bra,
                   'viewing_facility': self.viewing_facility,
                   'transcript': self.transcript,
                   'no_of_client_attendees': self.no_of_client_attendees,
                   'viewing_facility': self.viewing_facility,
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
                   'translation': self.translation,
                   'dp': self.dp,
                   'reporting': self.reporting,
                   'presentation': self.presentation,
                   'viewing_facility': self.viewing_facility,
                   'client_attendance': self.client_attendance,
                   'details': self.details,
                   'estimation_type': self.research_type_id.id,
                   'pdt_line_view': [(6, 0 ,self.pdt_line.ids)]}

           estimation = self.env['opportunity.cost.estimation'].create(vals)

      elif self.pdt_line_ql and  self.research_type_id.name=="QL":
            vals = {'partner_id': self.partner_id.id,
                    'client_attendence_region_ids': [(6, 0, self.client_attendence_region_ids.ids)],
                    'criteria_usage': self.criteria_usage,
                    'objective': self.objective,
                    'sample_size_text': self.sample_size_text,
                    'sample_struct_per_reg': self.sample_struct_per_reg,
                    'sample_struct_per_sec': self.sample_struct_per_sec,
                    'sample_struct_per_age': self.sample_struct_per_age,
                    'sample_struct_per_gen': self.sample_struct_per_gen,
                    'sample_struct_per_bra': self.sample_struct_per_bra,
                    'viewing_facility': self.viewing_facility,
                    'transcript': self.transcript,
                    'no_of_client_attendees': self.no_of_client_attendees,
                    'viewing_facility': self.viewing_facility,
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
                    'translation': self.translation,
                    'dp': self.dp,
                    'reporting': self.reporting,
                    'presentation': self.presentation,
                    'viewing_facility': self.viewing_facility,
                    'client_attendance': self.client_attendance,
                    'details': self.details,
                    'estimation_type': self.research_type_id.id,
                    'pdt_line_view': [(6, 0, self.pdt_line_ql.ids)]
                    }
            estimation = self.env['opportunity.cost.estimation'].create(vals)

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