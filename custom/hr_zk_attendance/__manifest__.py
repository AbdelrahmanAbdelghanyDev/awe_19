# -*- coding: utf-8 -*-
{
    'name': 'ZK Attendance Device',
    'summary': """Integrating Zk Device With HR Attendance""",
    'author': "Digizilla",
    'website': "https://www.Digizilla.net/",



    'depends': ['base_setup','hr', 'hr_attendance','resource'],
    'data': [
        'security/ir.model.access.csv',
        'views/zk_machine_view.xml',
        'views/zk_machine_attendance_view.xml',
        # 'views/attendance.xml',
#        'data/download_data.xml',

    ],
    'external_dependencies': {
        'python': ['zk']
    },
    'installable': True,
    'auto_install': False,
    'application': False,
}
