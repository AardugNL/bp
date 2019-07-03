# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Caret IT Solutions Pvt. Ltd. (Website: www.caretit.com).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

from odoo import api, fields, models, _

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    total_production_time = fields.Float(compute='_compute_total_production_time',
        string='Production Time', store=True)
    resource_id = fields.Many2one('resource.resource', string='Machine')
    capacity_machine_id = fields.Many2one('capacity.machine',
        string='Production Location')
    group = fields.Text()

    @api.depends('product_uom_qty', 'product_id.production_time_1')
    def _compute_total_production_time(self):
        for record  in self:
            record.total_production_time = record.product_uom_qty * record.product_id.production_time_1

    @api.onchange('product_id')
    def onchange_product(self):
        self.resource_id = self.product_id.resource_id
        self.capacity_machine_id = self.product_id.capacity_machine_id

    def _timesheet_create_task_prepare_values(self, project):
        res = super(SaleOrderLine, self)._timesheet_create_task_prepare_values(project)
        state = False
        if self.total_production_time > 0:
            state = 'done'
        res.update({
            'production_time_count': self.total_production_time,
            'resource_id': self.resource_id.id,
            'capacity_machine_id': self.capacity_machine_id.id,
            'production_state': state
            })
        return res
