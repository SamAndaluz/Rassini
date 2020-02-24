# -*- coding: utf-8 -*-
from collections import OrderedDict
from operator import itemgetter

from odoo import http, _
from odoo.exceptions import AccessError, MissingError
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager
from odoo.tools import groupby as groupbyelem

from odoo.osv.expression import OR

class CustomerPortal(CustomerPortal):

    @http.route(['/my/task/finish/<int:task_id>'], type='http', auth="public", website=True)
    def portal_my_task_finish_and_assign(self, task_id, access_token=None, **kw):
        try:
            task_sudo = self._document_check_access('project.task', task_id, access_token)
        except (AccessError, MissingError):
            return request.redirect('/my')

        # ensure attachment are accessible with access token inside template
        for attachment in task_sudo.attachment_ids:
            attachment.generate_access_token()
        # A. Márquez: asigna la tarea al administrador del proyecto y establece la tarea como hecha (done)
        task_sudo.user_id = task_sudo.project_id.user_id
        task_sudo.kanban_state = 'done'
        #
        values = self._task_get_page_view_values(task_sudo, access_token, **kw)
        return request.render("project.portal_my_task", values)
    
    def _task_get_page_view_values(self, task, access_token, **kwargs):
        print('-------------------- Entró al nuevo -----------------------')
        partner_id = task.project_id.partner_id.id
        user_ids = request.env['res.users'].sudo().search([('partner_id','child_of',partner_id)])
        print(user_ids)
        values = {
            'page_name': 'task',
            'task': task,
            'user': request.env.user,
            'user_ids': user_ids
        }
        return self._get_page_view_values(task, access_token, values, 'my_tasks_history', False, **kwargs)