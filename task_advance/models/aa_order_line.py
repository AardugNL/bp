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

    aa_total_production_time = fields.Float(compute='aa_compute_total_production_time',
        string='Production Time', store=True)
    aa_resource_id = fields.Many2one('resource.resource', string='Machine')
    aa_capacity_machine_id = fields.Many2one('aa.capacity.machine',
        string='Production Location', compute='aa_compute_machine_capacity')
    aa_group = fields.Text()
    aa_production_date = fields.Datetime('Production Date', compute='aa_compute_production_date')

    @api.depends('product_uom_qty', 'product_id.aa_production_time_1')
    def aa_compute_total_production_time(self):
        for aa_record  in self:
            aa_record.aa_total_production_time = aa_record.product_uom_qty * aa_record.product_id.aa_production_time_1

    @api.onchange('product_id')
    def onchange_product(self):
        self.aa_resource_id = self.product_id.aa_resource_id
        if self.product_id.aa_capacity_machine_id:
            self.aa_capacity_machine_id = self.product_id.aa_capacity_machine_id

    def _timesheet_create_task_prepare_values(self, project):
        aa_res = super(SaleOrderLine, self)._timesheet_create_task_prepare_values(project)
        state = False
        if self.aa_total_production_time > 0:
            state = 'done'
        aa_res.update({
            'aa_production_time_count': self.aa_total_production_time,
            'aa_resource_id': self.aa_resource_id.id,
            'aa_capacity_machine_id': self.aa_capacity_machine_id.id,
            'aa_production_state': state
            })
        return aa_res

    @api.multi
    def _timesheet_create_task(self, project):
        aa_res = super(SaleOrderLine, self)._timesheet_create_task(project)
        aa_res.aa_capacity_machine_id.aa_compute_total_time()
        aa_res.aa_capacity_machine_id.aa_compute_remain_capacity()
        return aa_res

    @api.depends('order_id.confirmation_date', 'product_id.aa_product_lead_time')
    def aa_compute_production_date(self):
        for aa_rec in self:
            if aa_rec.order_id.confirmation_date and aa_rec.product_id.aa_product_lead_time:
                aa_rec.aa_production_date = aa_rec.order_id.confirmation_date + datetime.timedelta(
                    minutes=aa_rec.product_id.aa_product_lead_time)

    @api.depends('aa_production_date', 'aa_resource_id')
    def aa_compute_machine_capacity(self):
        aa_machine_obj = self.env['aa.capacity.machine']
        for aa_rec in self:
            if aa_rec.aa_production_date and aa_rec.aa_resource_id:
                aa_machine_capacity = aa_machine_obj.search([
                    ('aa_resource_id', '=', aa_rec.aa_resource_id.id),
                    ('aa_date', '=', aa_rec.aa_production_date.date())
                ])
                if not aa_machine_capacity:
                    aa_machine_capacity = aa_machine_obj.create({
                        'aa_resource_id': aa_rec.aa_resource_id.id,
                        'aa_date': aa_rec.aa_production_date.date(),
                        'aa_capacity': 18.0
                    })
                    aa_machine_capacity.write({
                        'aa_name' : aa_machine_capacity.aa_join_name_date(
                            aa_rec.aa_resource_id.name, aa_rec.aa_production_date.date(), False)
                    })
                aa_rec.aa_capacity_machine_id = aa_machine_capacity.id
