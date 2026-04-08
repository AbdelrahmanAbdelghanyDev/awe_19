# -*- coding: utf-8 -*-
{
    'name': "AWE Job Card",

    'author': "Abdelrahman ShamrouKh | Centione",
    'website': "http://www.centione.com",

    # any module necessary for this one to work correctly
    'depends': ['base', 'account', 'account_budget', 'crm', 'product', 'sector', 'awe_cost_estimation',
                'awe_sale_order_custom',
                'cost_estimation', 'web_domain_field'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/month.xml',
        'views/job_card.xml',
        'views/revenue_bu.xml',
        'wizard/job_card_wizard.xml',
        'wizard/revenue_bu_wizard.xml',
        'reports/job_card_report.xml',
    ],
}
