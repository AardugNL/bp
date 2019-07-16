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

    def aa_checkTaskDescription(self, aa_cusName):
        '''To Find Customer Name In Description Field'''
        aa_productionProject = self.env.ref('task_advance.production_project')
        aa_tasks = self.search([('project_id', '=', aa_productionProject.id),
                ('description', 'not like', aa_cusName)])
        return aa_tasks.ids

    def aa_checkTagDescription(self, aa_taxt):
        '''To Find Search Tag In Description Field'''
        aa_productionProject = self.env.ref('task_advance.production_project')
        aa_tasks = self.search([('project_id', '=', aa_productionProject.id),
                ('description', 'like', aa_taxt)])
        return aa_tasks.ids