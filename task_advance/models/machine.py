# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Caret IT Solutions Pvt. Ltd. (Website: www.caretit.com).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

import datetime
from odoo import api, exceptions, fields, models, _
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DFORMAT


class Capacity(models.Model):
    _name = 'capacity.machine'

    name = fields.Char()
    resource_id = fields.Many2one('resource.resource', string='Machine')
    date = fields.Date()
    capacity = fields.Float()
    remain_capacity = fields.Float(string='Remain Capacity', compute='compute_remain_capacity',
        store=True)
    task_ids = fields.One2many('project.task', 'capacity_machine_id', string='Tasks')
    total_Production_time = fields.Float(string="Total Production Time", compute='compute_total_time',
        store=True)

    @api.depends('task_ids.production_time_count')
    def compute_total_time(self):
        for record in self:
            record.total_Production_time = round(sum(
                record.task_ids.mapped('production_time_count')), 2)

    @api.depends('total_Production_time', 'capacity')
    def compute_remain_capacity(self):
        for record in self:
            record.remain_capacity = record.capacity - record.total_Production_time

    @api.multi
    def name_get(self):
        res = []
        for capacity in self:
            name = '%s (%s)' % (capacity.name, '{0:02.0f}:{1:02.0f}'.format(*divmod(
                capacity.remain_capacity * 60, 60)))
            res.append((capacity.id, name))
        return res

    def _join_name_date(self, name, date):
        nameContent = []
        for nm in name.split(' '):
            nameContent.append(nm[:2])
            nameContent.append(nm[-1:])
        return''.join(nameContent) + ' ' + date.strftime('%d-%m/%W')

    @api.model
    def create(self, vals):
        res = super(Capacity, self).create(vals)
        if res.date and res.resource_id:
            res.name = self._join_name_date(res.resource_id.name, res.date)
        return res

    @api.multi
    def write(self, vals):
        resource = self.env['resource.resource']
        if vals.get('date') and not vals.get("resource_id"):
            self.name = self._join_name_date(self.resource_id.name,
                datetime.datetime.strptime(vals.get('date'), DFORMAT))
        if vals.get("resource_id") and not vals.get("date"):
            self.name = self._join_name_date(resource.browse(
                vals.get("resource_id")).name, self.date)
        if vals.get("resource_id") and vals.get('date'):
            self.name = self._join_name_date(resource.browse(vals.get("resource_id")).name,
                datetime.datetime.strptime(vals.get('date'), DFORMAT))
        return super(Capacity, self).write(vals)
