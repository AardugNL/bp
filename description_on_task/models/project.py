# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Caret IT Solutions Pvt. Ltd. (Website: www.caretit.com).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

from odoo.exceptions import ValidationError
from odoo import api, exceptions, fields, models, _


class ProjectTask(models.Model):
    _inherit = 'project.task'

    def checkTaskDescription(self, cusName):
        '''This Method Just For POC To Find Customer Name In Description Field'''
        productionProject = self.env.ref('task_advance.production_project')
        tasks = self.search([('project_id', '=', productionProject.id),
                ('description', 'not like', cusName)])
        return tasks.ids
