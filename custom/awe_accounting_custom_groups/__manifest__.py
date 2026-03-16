# -*- coding: utf-8 -*-
{
    'name': "Accounting Custom Groups",

    'author': "Centione",
    'website': "http://www.centione.com",

    'depends': ['base', 'account'],

    'data': [
        # 'security/ir.model.access.csv',
        'security/groups.xml',
        'views/account_bank_statement.xml',
        'views/account_move.xml',
        # 'views/account_move_line.xml',
    ],
}
