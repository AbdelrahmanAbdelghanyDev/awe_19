# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request
from datetime import datetime, timedelta


class PortalTimesheet(http.Controller):

    @http.route('/portal/timesheet/create', type='http', auth="user", website=True)
    def portal_timesheet_create(self, **kw):
        """Render the timesheet creation form in the portal."""
        project_obj = request.env['project.project'].sudo()
        task_obj = request.env['project.task'].sudo()
        return request.render('mo_portal_timesheet.portal_timesheet_create', {
            'projects': project_obj.search([('company_id', '=', request.env.company.id)]),
            'tasks': task_obj.search([]),
        })

    @http.route('/portal/timesheet/submit', type='http', auth="user", website=True)
    def portal_timesheet_submit(self, **kw):
        """Create a new timesheet from the portal."""
        timesheet_obj = request.env['account.analytic.line'].sudo()
        project = request.env['project.project'].sudo().browse(int(kw.get('project_id')))
        data = {
            'project_id': int(kw.get('project_id')),
            'task_id': int(kw.get('task_id')),
            'date': kw.get('date'),
            # 'date': datetime.strptime(kw['date'], "%Y-%m-%d"),
            'validated_status': 'draft',
            'name': kw.get('name'),
            'unit_amount': float(kw.get('hours')) if kw.get('hours') else 0.0,
            'employee_id': request.env.user.employee_ids.id,
            # 'company_id': int(project.company_id.id),
        }
        print(data)
        timesheet_obj.create(data)
        return request.redirect('/my/timesheets')

    @http.route(['/get_project_tasks'], type='json', auth="user", website=True)
    def get_project_tasks(self, **kw):
        tasks = request.env['project.task'].sudo().search([('project_id', '=', int(kw.get('project_id')))])
        tasks = [
            {'id': task.id,
             'name': task.name} for task in tasks]
        return {
            'tasks': tasks

        }

