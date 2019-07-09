# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Caret IT Solutions Pvt. Ltd. (Website: www.caretit.com).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

from odoo.exceptions import ValidationError
from odoo import api, exceptions, fields, models, _


class Project(models.Model):
    _inherit = 'project.project'

    production_project = fields.Boolean()


class ProjectTask(models.Model):
    _inherit = 'project.task'

    production_start_time = fields.Datetime('Production Start Time')
    production_end_time = fields.Datetime('Production End Time')
    production_time_count = fields.Float('Production Time')
    capacity_machine_id = fields.Many2one('capacity.machine', string='Machine Capacity')
    resource_id = fields.Many2one('resource.resource', string='Machine')
    production_state = fields.Selection([('done', 'Done'), ('blocked', 'Blocked')])

    # @api.onchange('production_start_time', 'production_end_time')
    # def _onchange_production_date(self):
    #     if self.production_start_time and self.production_end_time:
    #         diffInSecond = (self.production_end_time - self.production_start_time).total_seconds()
    #         self.production_time_count = float((diffInSecond // 60) / 60)
    #         if self.production_time_count > 0:
    #             self.production_state = 'done'
    #         else:
    #             self.production_state = 'blocked'

    # ToDo write perfect code right now it create issue when confirm sale order
    # @api.constrains('capacity_machine_id')
    # def _check_parent_id(self):
    #     if self.capacity_machine_id.resource_id != self.resource_id:
    #         raise ValidationError('\
    #             Warning! To Change Machine Capacity, You First Need To Change Machine')
