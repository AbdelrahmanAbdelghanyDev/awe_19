# -*- coding: utf-8 -*-
{
    'name': "hr_holidays_awe",

    'summary': """
        
        """,

    'description': """
        
    """,

    'author': "Co-partners",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/11.0/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',

    # any module necessary for this one to work correctly
    'depends': ['hr_holidays', 'hr'],

    # always loaded
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'data/data.xml',
        # 'views/views.xml',
    ],
}
