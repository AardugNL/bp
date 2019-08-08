# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Caret IT Solutions Pvt. Ltd. (Website: www.caretit.com).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

from odoo.exceptions import ValidationError
from odoo import models, fields, api

class aa_split_task(models.TransientModel):
    _name = 'aa.split.task'

    aa_no_of_split_task = fields.Integer(
        string='Number Of Split task')
    aa_split_task_line = fields.Many2many('project.task', string='Split task Lines')

    @api.multi
    def aa_create_split_task(self):
        aa_mainTask = self.env['project.task'].browse(
            self._context.get('active_id'))
        aa_taskList = []
        aa_seq = 0
        for task in range(self.aa_no_of_split_task):
            aa_seq += 1
            aa_task = self.env['project.task'].create({
                    'name': aa_mainTask.name + ' - ' + str(aa_seq),
                    'project_id': self.env.ref('task_advance.production_project').id,
                    'aa_resource_id': aa_mainTask.aa_resource_id.id,
                    'aa_capacity_machine_id': aa_mainTask.aa_capacity_machine_id.id,
            })
            aa_taskList.append(aa_task.id)
        self.aa_split_task_line = aa_taskList
        aa_mainTask.active = False
        return {
            'name': ('Split task Lines'),
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'aa.split.task',
            'views': [(self.env.ref('task_advance.aa_split_task_line_form').id, 'form')],
            'view_id': self.env.ref('task_advance.aa_split_task_line_form').id,
            'type': 'ir.actions.act_window',
            'res_id': self.id,
            'context': {'current_hrs': aa_mainTask.aa_production_time_count},
            'target': 'new'
        }       

    @api.multi
    def aa_save_split_task(self):
        aa_task_time = 0
        aa_timeCount = self._context['current_hrs']
        for time in self.aa_split_task_line:
            aa_task_time += time.aa_production_time_count
        if aa_task_time > aa_timeCount:
            raise ValidationError('\
                Warning! Please enter valid production time.')
