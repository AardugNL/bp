# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Caret IT Solutions Pvt. Ltd. (Website: www.caretit.com).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################
{
    'name': "Task Description",
    'version': '12.0',
    'summary': """ Add Description Field In Project Task Kanban View""",
    'category': 'Project',
    'description': """ 
        Add Description Field In Project Task Kanban View
        Note: added task_advance module in depends because in description_on_task
        module remove actual description page and take it to top right in form
        so when we install task_adavance module in that module hr_timesheet
        module is in depends so that module set path after description page so
        it conflict with description page, so to fix that issue task_advace
        put in depends.
    """,
    'author': 'Caret IT Solutions Pvt. Ltd.',
    'website': 'http://www.caretit.com',
    'depends': ['project', 'task_advance'],
    'data': [
        # 'security/ir.model.access.csv',
        'views/project_views.xml',
    ],
    'images': [],
    'price': 00,
    'currency': 'EUR',
    'qweb': [],
}
