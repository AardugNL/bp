# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Caret IT Solutions Pvt. Ltd. (Website: www.caretit.com).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

from odoo.exceptions import ValidationError
from odoo import api, exceptions, fields, models, _


class aa_Project(models.Model):
    _inherit = 'project.project'

    production_project = fields.Boolean()


class aa_ProjectTask(models.Model):
    _inherit = 'project.task'

    aa_production_start_time = fields.Datetime('Production Start Time')
    aa_production_end_time = fields.Datetime('Production End Time')
    aa_production_time_count = fields.Float('Production Time')
    aa_capacity_machine_id = fields.Many2one('aa.capacity.machine', string='Machine Capacity')
    aa_resource_id = fields.Many2one('resource.resource', string='Machine')
    aa_production_state = fields.Selection([('done', 'Done'), ('blocked', 'Blocked')])

    # @api.onchange('aa_production_start_time', 'aa_production_end_time')
    # def _onchange_production_date(self):
    #     if self.aa_production_start_time and self.aa_production_end_time:
    #         diffInSecond = (self.production_end_time - self.aa_production_start_time).total_seconds()
    #         self.aa_production_time_count = float((diffInSecond // 60) / 60)
    #         if self.aa_production_time_count > 0:
    #             self.production_state = 'done'
    #         else:
    #             self.production_state = 'blocked'

    # @api.constrains('aa_capacity_machine_id')
    # def aa_check_parent_id(self):
    #     if self.aa_capacity_machine_id.aa_resource_id != self.aa_resource_id:
    #         raise ValidationError('\
    #             Warning! To Change Machine Capacity, You First Need To Change Machine')
