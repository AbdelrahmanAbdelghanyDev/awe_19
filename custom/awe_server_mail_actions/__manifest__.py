# -*- coding: utf-8 -*-
{
    'name': "Awe Server Mail Action",

    # any module necessary for this one to work correctly
    'depends': ['base','hr_holidays'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        # 'views/hr_leave_and_allocation_server_action.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}