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
                'sale_timesheet'],
    'data': [
        'security/ir.model.access.csv',
        'data/project.xml',
        'views/assets.xml',
        'views/project_views.xml',
        'views/machine_view.xml',
        'views/product_view.xml',
        'views/orderline_view.xml'
    ],
    'qweb': [
        'static/src/xml/templates.xml',
    ],
    'demo': [
    ],
}
