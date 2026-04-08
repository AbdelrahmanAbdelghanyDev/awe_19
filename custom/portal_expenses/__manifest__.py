# -*- coding: utf-8 -*-
{
    'name': "Portal Expenses",

    'summary': """
        Submit and Review Expenses for portal users""",

    'description': """
        Submit and Review Expenses for portal users,

If you have any inquiry please contact us at support@digizilla.net
    """,

    'author': "Digizilla",
    'website': "http://www.digizilla.net",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'HR',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','hr_expense','web','portal','website','hr','project','sale_management'],

    # always loaded
    'data': [
        'views/views.xml',
        # 'views/templates.xml',
    ],
    # only loaded in demonstration mode

    'qweb': [
        'static/src/xml/timestamp_button.xml',
    ],

    'js': ['static/src/js/timestamp_button.js'],

    'assets': {
        'web.assets_frontend': [
            '/portal_expenses/static/src/js/portal_expenses.js',

            '/portal_expenses/static/lib/bootstrap-datepicker-1.6.4-dist/css/bootstrap-datepicker.css',
            '/portal_expenses/static/lib/bootstrap-datepicker-1.6.4-dist/css/bootstrap-datepicker3.css',
            '/portal_expenses/static/lib/bootstrap-datepicker-1.6.4-dist/js/bootstrap-datepicker.js',
            '/portal_expenses/static/lib/bootstrap-datepicker-1.6.4-dist/locales/bootstrap-datepicker.ar.min.js',
            '/portal_expenses/static/lib/bootstrap-datepicker-1.6.4-dist/locales/bootstrap-datepicker.az.min.js',
            '/portal_expenses/static/lib/bootstrap-datepicker-1.6.4-dist/locales/bootstrap-datepicker.bg.min.js',
            '/portal_expenses/static/lib/bootstrap-datepicker-1.6.4-dist/locales/bootstrap-datepicker.bs.min.js',
            '/portal_expenses/static/lib/bootstrap-datepicker-1.6.4-dist/locales/bootstrap-datepicker.ca.min.js',
            '/portal_expenses/static/lib/bootstrap-datepicker-1.6.4-dist/locales/bootstrap-datepicker.cs.min.js',
            '/portal_expenses/static/lib/bootstrap-datepicker-1.6.4-dist/locales/bootstrap-datepicker.cy.min.js',
            '/portal_expenses/static/lib/bootstrap-datepicker-1.6.4-dist/locales/bootstrap-datepicker.da.min.js',

            '/portal_expenses/static/lib/bootstrap-datepicker-1.6.4-dist/locales/bootstrap-datepicker.de.min.js',
            '/portal_expenses/static/lib/bootstrap-datepicker-1.6.4-dist/locales/bootstrap-datepicker.el.min.js',
            '/portal_expenses/static/lib/bootstrap-datepicker-1.6.4-dist/locales/bootstrap-datepicker.en-AU.min.js',
            '/portal_expenses/static/lib/bootstrap-datepicker-1.6.4-dist/locales/bootstrap-datepicker.en-GB.min.js',
            '/portal_expenses/static/lib/bootstrap-datepicker-1.6.4-dist/locales/bootstrap-datepicker.eo.min.js',
            '/portal_expenses/static/lib/bootstrap-datepicker-1.6.4-dist/locales/bootstrap-datepicker.es.min.js',
            '/portal_expenses/static/lib/bootstrap-datepicker-1.6.4-dist/locales/bootstrap-datepicker.et.min.js',
            '/portal_expenses/static/lib/bootstrap-datepicker-1.6.4-dist/locales/bootstrap-datepicker.eu.min.js',
            '/portal_expenses/static/lib/bootstrap-datepicker-1.6.4-dist/locales/bootstrap-datepicker.fa.min.js',
            '/portal_expenses/static/lib/bootstrap-datepicker-1.6.4-dist/locales/bootstrap-datepicker.fi.min.js',
            '/portal_expenses/static/lib/bootstrap-datepicker-1.6.4-dist/locales/bootstrap-datepicker.fo.min.js',
            '/portal_expenses/static/lib/bootstrap-datepicker-1.6.4-dist/locales/bootstrap-datepicker.fr.min.js',
            '/portal_expenses/static/lib/bootstrap-datepicker-1.6.4-dist/locales/bootstrap-datepicker.fr-CH.min.js',
            '/portal_expenses/static/lib/bootstrap-datepicker-1.6.4-dist/locales/bootstrap-datepicker.gl.min.js',
            '/portal_expenses/static/lib/bootstrap-datepicker-1.6.4-dist/locales/bootstrap-datepicker.he.min.js',

            '/portal_expenses/static/lib/bootstrap-datepicker-1.6.4-dist/locales/bootstrap-datepicker.hr.min.js',
            '/portal_expenses/static/lib/bootstrap-datepicker-1.6.4-dist/locales/bootstrap-datepicker.hu.min.js',
            '/portal_expenses/static/lib/bootstrap-datepicker-1.6.4-dist/locales/bootstrap-datepicker.hy.min.js',
            '/portal_expenses/static/lib/bootstrap-datepicker-1.6.4-dist/locales/bootstrap-datepicker.id.min.js',
            '/portal_expenses/static/lib/bootstrap-datepicker-1.6.4-dist/locales/bootstrap-datepicker.is.min.js',
            '/portal_expenses/static/lib/bootstrap-datepicker-1.6.4-dist/locales/bootstrap-datepicker.it.min.js',
            '/portal_expenses/static/lib/bootstrap-datepicker-1.6.4-dist/locales/bootstrap-datepicker.it-CH.min.js',
            '/portal_expenses/static/lib/bootstrap-datepicker-1.6.4-dist/locales/bootstrap-datepicker.ja.min.js',
            '/portal_expenses/static/lib/bootstrap-datepicker-1.6.4-dist/locales/bootstrap-datepicker.ka.min.js',
            '/portal_expenses/static/lib/bootstrap-datepicker-1.6.4-dist/locales/bootstrap-datepicker.kh.min.js',
            '/portal_expenses/static/lib/bootstrap-datepicker-1.6.4-dist/locales/bootstrap-datepicker.kk.min.js',
            '/portal_expenses/static/lib/bootstrap-datepicker-1.6.4-dist/locales/bootstrap-datepicker.ko.min.js',

            '/portal_expenses/static/lib/bootstrap-datepicker-1.6.4-dist/locales/bootstrap-datepicker.kr.min.js',
            '/portal_expenses/static/lib/bootstrap-datepicker-1.6.4-dist/locales/bootstrap-datepicker.lt.min.js',
            '/portal_expenses/static/lib/bootstrap-datepicker-1.6.4-dist/locales/bootstrap-datepicker.lv.min.js',
            '/portal_expenses/static/lib/bootstrap-datepicker-1.6.4-dist/locales/bootstrap-datepicker.me.min.js',
            '/portal_expenses/static/lib/bootstrap-datepicker-1.6.4-dist/locales/bootstrap-datepicker.mk.min.js',
            '/portal_expenses/static/lib/bootstrap-datepicker-1.6.4-dist/locales/bootstrap-datepicker.mn.min.js',
            '/portal_expenses/static/lib/bootstrap-datepicker-1.6.4-dist/locales/bootstrap-datepicker.ms.min.js',
            '/portal_expenses/static/lib/bootstrap-datepicker-1.6.4-dist/locales/bootstrap-datepicker.nb.min.js',
            '/portal_expenses/static/lib/bootstrap-datepicker-1.6.4-dist/locales/bootstrap-datepicker.nl.min.js',
            '/portal_expenses/static/lib/bootstrap-datepicker-1.6.4-dist/locales/bootstrap-datepicker.nl-BE.min.js',
            '/portal_expenses/static/lib/bootstrap-datepicker-1.6.4-dist/locales/bootstrap-datepicker.no.min.js',
            '/portal_expenses/static/lib/bootstrap-datepicker-1.6.4-dist/locales/bootstrap-datepicker.pl.min.js',
            '/portal_expenses/static/lib/bootstrap-datepicker-1.6.4-dist/locales/bootstrap-datepicker.pt.min.js',
            '/portal_expenses/static/lib/bootstrap-datepicker-1.6.4-dist/locales/bootstrap-datepicker.pt-BR.min.js',
            '/portal_expenses/static/lib/bootstrap-datepicker-1.6.4-dist/locales/bootstrap-datepicker.ro.min.js',

            '/portal_expenses/static/lib/bootstrap-datepicker-1.6.4-dist/locales/bootstrap-datepicker.rs.min.js',
            '/portal_expenses/static/lib/bootstrap-datepicker-1.6.4-dist/locales/bootstrap-datepicker.rs-latin.min.js',
            '/portal_expenses/static/lib/bootstrap-datepicker-1.6.4-dist/locales/bootstrap-datepicker.ru.min.js',
            '/portal_expenses/static/lib/bootstrap-datepicker-1.6.4-dist/locales/bootstrap-datepicker.sk.min.js',
            '/portal_expenses/static/lib/bootstrap-datepicker-1.6.4-dist/locales/bootstrap-datepicker.sl.min.js',
            '/portal_expenses/static/lib/bootstrap-datepicker-1.6.4-dist/locales/bootstrap-datepicker.sq.min.js',
            '/portal_expenses/static/lib/bootstrap-datepicker-1.6.4-dist/locales/bootstrap-datepicker.sr.min.js',
            '/portal_expenses/static/lib/bootstrap-datepicker-1.6.4-dist/locales/bootstrap-datepicker.sr-latin.min.js',
            '/portal_expenses/static/lib/bootstrap-datepicker-1.6.4-dist/locales/bootstrap-datepicker.sv.min.js',
            '/portal_expenses/static/lib/bootstrap-datepicker-1.6.4-dist/locales/bootstrap-datepicker.sw.min.js',
            '/portal_expenses/static/lib/bootstrap-datepicker-1.6.4-dist/locales/bootstrap-datepicker.th.min.js',
            '/portal_expenses/static/lib/bootstrap-datepicker-1.6.4-dist/locales/bootstrap-datepicker.tr.min.js',
            '/portal_expenses/static/lib/bootstrap-datepicker-1.6.4-dist/locales/bootstrap-datepicker.uk.min.js',
            '/portal_expenses/static/lib/bootstrap-datepicker-1.6.4-dist/locales/bootstrap-datepicker.vi.min.js',
            '/portal_expenses/static/lib/bootstrap-datepicker-1.6.4-dist/locales/bootstrap-datepicker.zh-CN.min.js',
            '/portal_expenses/static/lib/bootstrap-datepicker-1.6.4-dist/locales/bootstrap-datepicker.zh-TW.min.js',

        ],
    },
}
