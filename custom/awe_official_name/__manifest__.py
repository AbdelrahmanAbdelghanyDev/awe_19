# -*- coding: utf-8 -*-
{
    'name': "awe_official_name",

    'summary': """
        Custom Invoice Reports
        """,

    'description': """
        Add field in partner (Official name) form " customer & vendor " invoice name so when selecting this partner in sales or purchase order and create invoice this name will fill automatically
    """,

    'author': "Digizilla",
    'website': "http://digizilla.net",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Invoice',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'account','awe_currency_num2words','l10n_ar','l10n_cl'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'security/security.xml',
        'views/views.xml',
        'views/templates.xml',
        'views/res_partner_inherit.xml',
        # 'views/sales_invoice_inherit.xml',
        'views/purchase_invoice_inherit.xml',
        'views/sales_report_inherit.xml',
        'views/ksa_arabic_invoice.xml',
        'views/company_views.xml',
        'views/account_move_inh.xml',
        'data/data.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
