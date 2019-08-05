# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Caret IT Solutions Pvt. Ltd. (Website: www.caretit.com).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################
{
    'name': "Task Advance",
    'summary': """""",
    'description': """

    """,
    'author': 'Caret IT Solutions Pvt. Ltd.',
    'website': 'http://www.caretit.com',
    'category': 'Project',
    'version': '12.0',
    'depends': ['project', 'hr_timesheet', 'sale_management', 'product',
                'sale_timesheet','resource', 'sale'],
    'data': [
        'security/ir.model.access.csv',
        'data/aa_project.xml',
        'wizard/aa_split_task.xml',
        'wizard/aa_fire_sql.xml',
        'views/aa_assets.xml',
        'views/aa_project_views.xml',
        'views/aa_machine_view.xml',
        'views/aa_product_view.xml',
        'views/aa_orderline_view.xml',
        'views/aa_machine_resource.xml'
    ],
    'qweb': [
        'static/src/xml/aa_templates.xml',
        'static/src/xml/aa_machine_dashboard.xml'
    ],
    'demo': [
    ],
}
