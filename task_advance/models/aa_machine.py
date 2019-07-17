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


class aa_Capacity(models.Model):
    _name = 'aa.capacity.machine'
    _rec_name = 'aa_name'

    aa_name = fields.Char()
    aa_resource_id = fields.Many2one('resource.resource', string='Machine')
    aa_date = fields.Date('Date')
    aa_capacity = fields.Float('Capacity')
    aa_remain_capacity = fields.Float(string='Remain Capacity', compute='compute_remain_capacity',
        store=True)
    aa_task_ids = fields.One2many('project.task', 'aa_capacity_machine_id', string='Tasks')
    aa_total_Production_time = fields.Float(string="Total Production Time", compute='compute_total_time',
        store=True)

    @api.depends('aa_task_ids.aa_production_time_count')
    def aa_compute_total_time(self):
        for aa_record in self:
            aa_record.aa_total_Production_time = round(sum(
                aa_record.aa_task_ids.mapped('aa_production_time_count')), 2)

    @api.depends('aa_total_Production_time', 'aa_capacity')
    def aa_compute_remain_capacity(self):
        for aa_record in self:
            aa_record.aa_remain_capacity = aa_record.aa_capacity - aa_record.aa_total_Production_time

    # @api.multi
    # def name_get(self):
    #     res = []
    #     for capacity in self:
    #         name = '%s (%s)' % (capacity.name, '{0:02.0f}:{1:02.0f}'.format(*divmod(
    #             capacity.remain_capacity * 60, 60)))
    #         res.append((capacity.id, name))
    #     return res

    def aa_join_name_date(self, aa_name, date):
        # nameContent = []
        # for nm in name.split(' '):
        #     nameContent.append(nm[:2])
        #     nameContent.append(nm[-1:])
        # return''.join(nameContent) + ' ' + date.strftime('%d-%m/%W')
        aa_nameContent = aa_name[:2] + aa_name[-1:]
        aa_weekDay = ['MA', 'DI', 'WO', 'DO', 'VR', 'ZA', 'ZO']
        return aa_nameContent.upper() + ' ' + date.strftime('%d-%m/%W') + aa_weekDay[date.weekday()]

    @api.model
    def create(self, vals):
        aa_res = super(aa_Capacity, self).create(vals)
        if aa_res.aa_date and aa_res.aa_resource_id:
            aa_res.aa_name = self.aa_join_name_date(aa_res.aa_resource_id.name, aa_res.aa_date)
        return aa_res

    @api.multi
    def write(self, vals):
        aa_resource = self.env['resource.resource']
        if vals.get('aa_date') and not vals.get("aa_resource_id"):
            self.aa_name = self.aa_join_name_date(self.aa_resource_id.aa_name,
                datetime.datetime.strptime(vals.get('aa_date'), DFORMAT))
        if vals.get("aa_resource_id") and not vals.get("aa_date"):
            self.aa_name = self.aa_join_name_date(aa_resource.browse(
                vals.get("aa_resource_id")).aa_name, self.aa_date)
        if vals.get("aa_resource_id") and vals.get('aa_date'):
            self.aa_name = self.aa_join_name_date(aa_resource.browse(vals.get("aa_resource_id")).aa_name,
                datetime.datetime.strptime(vals.get('aa_date'), DFORMAT))
        return super(aa_Capacity, self).write(vals)
