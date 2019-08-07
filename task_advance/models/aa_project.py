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
    aa_capacity_machine_id = fields.Many2one('aa.capacity.machine',
        string='Machine Capacity')
    aa_resource_id = fields.Many2one('resource.resource', string='Machine', readonly=True)
    aa_production_state = fields.Selection([('done', 'Done'), ('blocked', 'Blocked')])
    aa_freeze = fields.Boolean(string='aa_freeze')
    aa_startup = fields.Boolean(string='STARTUP', readonly=True)

    # @api.onchange('aa_production_start_time', 'aa_production_end_time')
    # def _onchange_production_date(self):
    #     if self.aa_production_start_time and self.aa_production_end_time:
    #         diffInSecond = (self.production_end_time - self.aa_production_start_time).total_seconds()
    #         self.aa_production_time_count = float((diffInSecond // 60) / 60)
    #         if self.aa_production_time_count > 0:
    #             self.aa_production_state = 'done'
    #         else:
    #             self.aa_production_state = 'blocked'

    # @api.constrains('aa_capacity_machine_id')
    # def aa_check_parent_id(self):
    #     if self.aa_capacity_machine_id.aa_resource_id != self.aa_resource_id:
    #         raise ValidationError('\
    #             Warning! To Change Machine Capacity, You First Need To Change Machine')

    @api.multi
    def write(self, vals):
        if vals.get('aa_capacity_machine_id'):
            if self.aa_freeze == True:
                raise ValidationError('\
                    Unable to move.')
            else:
                orderLine = (self.env['sale.order.line'].browse(
                    vals.get('sale_line_id')) if vals.get('sale_line_id') else self.sale_line_id)
                if orderLine:
                    orderLine.aa_capacity_machine_id = vals.get('aa_capacity_machine_id')
                return super(aa_ProjectTask, self).write(vals)
        else:
            return super(aa_ProjectTask, self).write(vals)

    @api.model
    def updateCapacityHtml(self):
        query = """ UPDATE aa_capacity_machine
                    SET aa_html='%s'
                    WHERE aa_plan_only=False
                """ %('<b>PArth</b>')
        self.env.cr.execute(query)
