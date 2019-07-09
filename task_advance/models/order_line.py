# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Caret IT Solutions Pvt. Ltd. (Website: www.caretit.com).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

from odoo import api, fields, models, _
import datetime

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    total_production_time = fields.Float(compute='_compute_total_production_time',
        string='Production Time', store=True)
    resource_id = fields.Many2one('resource.resource', string='Machine')
    capacity_machine_id = fields.Many2one('capacity.machine',
        string='Production Location', compute='_compute_machine_capacity')
    group = fields.Text()
    production_date = fields.Datetime('Production Date', compute='_compute_production_date')

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

    @api.depends('order_id.confirmation_date', 'product_id.product_lead_time')
    def _compute_production_date(self):
        for rec in self:
            if rec.order_id.confirmation_date and rec.product_id.product_lead_time:
                rec.production_date = rec.order_id.confirmation_date + datetime.timedelta(
                    minutes=rec.product_id.product_lead_time)

    @api.depends('production_date', 'resource_id')
    def _compute_machine_capacity(self):
        machine_obj = self.env['capacity.machine']
        for rec in self:
            if rec.production_date and rec.resource_id:
                machine_capacity = machine_obj.search([
                    ('resource_id', '=', rec.resource_id.id),
                    ('date', '=', rec.production_date.date())
                ])
                if not machine_capacity:
                    machine_capacity = machine_obj.create({
                        'resource_id': rec.resource_id.id,
                        'date': rec.production_date.date()
                    })
                    machine_capacity.write({
                        'name' : machine_capacity._join_name_date(rec.resource_id.name, rec.production_date.date())
                    })
                rec.capacity_machine_id = machine_capacity.id
