# -*- coding: utf-8 -*-

from odoo import models, fields, api
from num2words import num2words
import base64


class InvoiceTaf(models.Model):
    _inherit = "account.move"


    invoice_date_time = fields.Datetime(
        string='Invoice Date',
        required=False, store=True)

    @api.onchange('invoice_date')
    def get_invoice_date_time(self):
        if self.invoice_date:
            self.invoice_date_time = self.invoice_date
        else:
            self.invoice_date_time = False



    # this function to cancel what l10n_gcc_invoice module do in invoice report
    def _get_name_invoice_report(self):
        self.ensure_one()
        if self.company_id.country_id in self.env.ref('base.gulf_cooperation_council').country_ids:
            return 'account.report_invoice_document'
        return super()._get_name_invoice_report()

    amount_to_text = fields.Text(
        store=True,compute="_amount_to_words"

    )
    amount_to_text_arabic = fields.Text(
        store=True,compute="_amount_to_words"
        
    )

    custom_payment_terms = fields.Text(string="Payment Terms",
                                       default='Payment is due within 30 days of invoice date. \n'
                                               'Please use our invoice number reference upon payment.')

    # @api.depends('amount_total')
    from num2words import num2words

    def _amount_to_words(self):
        for rec in self:
            rec.amount_to_text = rec.currency_id.en_amount_to_text(rec.amount_total)
            rec.amount_to_text_arabic = rec.currency_id.ar_amount_to_text(rec.amount_total)


# class InvAr(models.Model):
#     _inherit = 'res.users'
#
#     @api.onchange('company_ids')
#     def read_arabic_invoice(self):
#         group = self.env['res.groups'].search([('name', '=', 'Invoice Arabic')])
#         # print('group',group)
#         # print(' self.company_ids.id', self.company_ids.id)
#         # if 4 in self.company_ids.ids:
#         # group.users = [(4,3)]
#         group.write({'users':[4,5]})
#         # else:
#         #     group.write({'users': [(3, self._origin.id)]}) # Delete
#
#

    l10n_sa_delivery_date = fields.Date(string='Delivery Date', default=fields.Date.context_today, copy=False)
    l10n_sa_show_delivery_date = fields.Boolean(compute='_compute_show_delivery_date')
    l10n_sa_qr_code_str = fields.Char(string='Zatka QR Code', compute='_compute_qr_code_str')
    l10n_sa_confirmation_datetime = fields.Datetime(string='Confirmation Date', copy=False, readonly=True,
                                                    default=fields.Datetime.now())

    @api.depends('company_id', 'move_type', 'delivery_date')
    def _compute_show_delivery_date(self):
        super()._compute_show_delivery_date()

        for move in self:
            move.l10n_sa_show_delivery_date = (
                    move.company_id.country_id.code == 'SA'
                    and move.is_sale_document()
            )
    @api.depends('amount_total', 'amount_untaxed', 'l10n_sa_confirmation_datetime', 'company_id', 'company_id.vat')
    def _compute_qr_code_str(self):
        """ Generate the qr code for Saudi e-invoicing. Specs are available at the following link at page 23
        https://zatca.gov.sa/ar/E-Invoicing/SystemsDevelopers/Documents/20210528_ZATCA_Electronic_Invoice_Security_Features_Implementation_Standards_vShared.pdf
        """

        def get_qr_encoding(tag, field):
            # Ensure that the field is a string before encoding
            if isinstance(field, bool):
                field = str(field)  # Convert boolean to string ('True' or 'False')

            company_name_byte_array = field.encode('UTF-8')
            company_name_tag_encoding = tag.to_bytes(length=1, byteorder='big')
            company_name_length_encoding = len(company_name_byte_array).to_bytes(length=1, byteorder='big')

            return company_name_tag_encoding + company_name_length_encoding + company_name_byte_array

        for record in self:
            qr_code_str = ''
            if record.l10n_sa_confirmation_datetime and record.company_id.vat:
                # Ensure the fields passed are strings
                seller_name_enc = get_qr_encoding(1, str(record.company_id.company_tax_name))
                company_vat_enc = get_qr_encoding(2, str(record.company_id.vat))

                time_sa = fields.Datetime.context_timestamp(self.with_context(tz='Asia/Riyadh'),
                                                            fields.Datetime.from_string(
                                                                record.l10n_sa_confirmation_datetime))
                timestamp_enc = get_qr_encoding(3, time_sa.isoformat())

                invoice_total_enc = get_qr_encoding(4, str(record.amount_total))
                total_vat_enc = get_qr_encoding(5, str(record.currency_id.round(
                    record.amount_total - record.amount_untaxed)))

                # Combine all encoded fields
                str_to_encode = seller_name_enc + company_vat_enc + timestamp_enc + invoice_total_enc + total_vat_enc

                # Base64 encode the result to generate the QR code string
                qr_code_str = base64.b64encode(str_to_encode).decode('UTF-8')

            # Assign the result to the field
            record.l10n_sa_qr_code_str = qr_code_str

    # def action_post(self):
    #     res = super(AccountMoveInherit, self).action_post()
    #     # res = super().action_post()
    #     for record in self:
    #         if record.company_id.country_id.code == 'SA' and record.move_type in ('out_invoice', 'out_refund'):
    #             if not record.l10n_sa_show_delivery_date:
    #                 raise UserError(_('Delivery Date cannot be empty'))
    #             if record.l10n_sa_delivery_date < record.invoice_date:
    #                 raise UserError(_('Delivery Date cannot be before Invoice Date'))
    #             record.write({
    #                 'l10n_sa_confirmation_datetime': fields.Datetime.now()
    #             })
    #     return res
    #


class AccountMoveLineInh(models.Model):
    _inherit = 'account.move.line'

    balance = fields.Monetary(string='Balance', store=True,
        currency_field='company_currency_id',
        compute='_compute_balance',
        help="Technical field holding the debit - credit in order to open meaningful graph views from reports",tracking=True)

    partner_id = fields.Many2one('res.partner', string='Partner', ondelete='restrict',tracking=True)
    name = fields.Char(string='Label', tracking=True)
