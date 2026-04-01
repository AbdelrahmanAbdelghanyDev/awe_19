# -*- coding: utf-8 -*-

from odoo import models, fields, api
from num2words import num2words


class ResCompanyInh(models.Model):
    _inherit = "res.company"

    Research_office = fields.Text(
        string=" Research office",
        required=False)

    operations_office = fields.Text(
        string=" Operations office",
        required=False)

    cr_number = fields.Char(
        string='CR Number',
        required=False)

    TAX_File_Number = fields.Char(
        string=' TAX File Number',
        required=False)

    TRN_Number = fields.Char(
        string=' TRN Number',
        required=False)

    PO_Box = fields.Char(
        string=' PO Box',
        required=False)


    # egypt
    Account_Name = fields.Text(
        string='Account Name',
        required=False)

    Account_Name2 = fields.Text(
        string='Account Name 2',
        required=False)

    Account_No_EGP = fields.Char(
        string=' Account No EGP',
        required=False)

    IBAN_No_EGP = fields.Char(
        string=' IBAN No EGP',
        required=False)

    Account_No_USD = fields.Char(
        string='Account No USD',
        required=False)
    IBAN_No_USD = fields.Char(
        string=' IBAN No USD',
        required=False)

    QNB_ALAHLI_SWIFT_CODE = fields.Text(
        string=" QNB ALAHLI, SWIFT CODE",
        required=False)
    Account_No_EGP2 = fields.Char(
        string='Account No EGP 2',
        required=False)

    EGP_IBAN = fields.Char(
        string=' EGP IBAN',
        required=False)
    Account_No_USD2 = fields.Char(
        string='Account No USD 2',
        required=False)
    USD_IBAN = fields.Char(
        string='USD IBAN',
        required=False)
    SWIFT_CODE = fields.Char(
        string='SWIFT CODE',
        required=False)

    # UAE
    Account_number_AED = fields.Char(
        string='Account Number AED ',
        required=False)

    Account_number_USD = fields.Char(
        string='Account Number USD ',
        required=False)

    Account_Name_UAE = fields.Text(
        string='Account Name',
        required=False)
    bank = fields.Char(
        string='Bank',
        required=False)
    Branch_name = fields.Char(
        string='Branch name',
        required=False)
    Swift = fields.Char(
        string='Swift',
        required=False)
    IBAN_AED = fields.Char(
        string='IBAN AED',
        required=False)
    IBAN_USD = fields.Char(
        string='IBAN USD',
        required=False)
    # ksa

    Account_No = fields.Char(
        string='Account No',
        required=False)

    IBAN_ksa = fields.Char(
        string=' IBAN ksa',
        required=False)

    SHB_SWIFT_CODE = fields.Char(
        string=' SHB, SWIFT CODE',
        required=False)

    Account_No2 = fields.Char(
        string='Account No 2',
        required=False)

    IBAN_ksa2 = fields.Char(
        string=' IBAN ksa 2',
        required=False)

    SHB_SWIFT_CODE2 = fields.Char(
        string=' SHB, SWIFT CODE 2',
        required=False)
    
    
    
# company ar
    company_name_ar = fields.Char(
        string='Company name ar', 
        required=False)
    
    address_ar = fields.Text(
        string="Address ar",
        required=False)
    
    mobile_ar = fields.Char(
        string='Mobile ar', 
        required=False)
    
    tax_number_ar = fields.Char(
        string='رقم السجل التجاري',
        required=False)
    tax_number2_ar = fields.Char(
        string='رقم التسجيل في ضريبة القيمة المضافة',
        required=False)
    file_number = fields.Char(
        string='رقم الملف',
        required=False)