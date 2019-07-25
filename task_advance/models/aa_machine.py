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

    aa_name = fields.Char(string='Name')
    aa_resource_id = fields.Many2one('resource.resource', string='Machine')
    aa_date = fields.Date('Date')
    aa_capacity = fields.Float('Capacity')
    aa_remain_capacity = fields.Float(string='Remain Capacity', compute='aa_compute_remain_capacity',
        store=True)
    aa_task_ids = fields.One2many('project.task', 'aa_capacity_machine_id', string='Tasks')
    aa_total_Production_time = fields.Float(string="Total Production Time", compute='aa_compute_total_time',
        store=True)
    aa_machine_header = fields.Text('Machine Header')
    aa_machine_info = fields.Text('Machine Info')
    date_from = fields.Date('From', default=fields.Date.today())
    date_to = fields.Date('To', default=datetime.date.today() + datetime.timedelta(days=6))
    aa_plan_only = fields.Boolean(string='Plan Only')
    aa_progress = fields.Float(compute='_compute_progress', store=True, string='Progress')

    @api.depends('aa_capacity', 'aa_remain_capacity')
    def _compute_progress(self):
        for aa_rec in self:
            if aa_rec.aa_remain_capacity:
                aa_rec.aa_progress = round(
                    aa_rec.aa_remain_capacity / aa_rec.aa_capacity * 100, 2)

    @api.onchange('date_from', 'date_to')
    def aa_onchange_dates(self):
        res = {}
        if (not self.date_from) or (not self.date_to):
            return res
        aa_machines = self.search([
            ('aa_date', '>', self.date_from), ('aa_date', '<', self.date_to)])
        # aa_date_header_list = []
        # dateRange = self.date_to - self.date_from
        # for i in range(dateRange.days + 1):
        #     day = self.date_from + datetime.timedelta(days=i)
        #     aa_date_header_list.append(day.strftime(DFORMAT))
        aa_date_header_list = [aa_machine.aa_name for aa_machine in aa_machines]
        aa_date_header = [{'header': aa_date_header_list}]
        aa_all_machine_details = {}
        for aa_machine in aa_machines:
            aa_machineId = aa_machine.id
            aa_all_machine_details.setdefault(aa_machineId, {
                'name': aa_machine.aa_resource_id.name,
                'id': aa_machineId,
                # 'noOfDays': dateRange.days+1,
                'noOfDays': len(aa_machines),
                'progress': aa_machine.aa_progress})
        aa_all_machine_details = aa_all_machine_details.values()
        aa_sorted_all_machine_detail = sorted(
            aa_all_machine_details,
            key=lambda x: x['name'], reverse=True)
        self.aa_machine_header = str(aa_date_header)
        self.aa_machine_info = str(aa_sorted_all_machine_detail)
        return res

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

    def aa_join_name_date(self, aa_name, date, aa_plan_only):
        # nameContent = []
        # for nm in name.split(' '):
        #     nameContent.append(nm[:2])
        #     nameContent.append(nm[-1:])
        # return''.join(nameContent) + ' ' + date.strftime('%d-%m/%W')
        aa_nameContent = aa_name[:2] + aa_name[-1:]
        aa_weekDay = ['MA', 'DI', 'WO', 'DO', 'VR', 'ZA', 'ZO']
        if aa_plan_only == True:
            return aa_nameContent.upper() + ' ' + date.strftime('%d-%m/') + 'PLAN'
        else:
            return aa_nameContent.upper() + ' ' + date.strftime('%d-%m/%W') + aa_weekDay[date.weekday()]

    @api.model
    def create(self, vals):
        aa_res = super(aa_Capacity, self).create(vals)
        if aa_res.aa_date and aa_res.aa_resource_id:
            aa_res.aa_name = self.aa_join_name_date(
                aa_res.aa_resource_id.name, aa_res.aa_date, aa_res.aa_plan_only)
        return aa_res

    @api.multi
    def write(self, vals):
        aa_resource = self.env['resource.resource']
        aa_date = (datetime.datetime.strptime(vals.get('aa_date'), DFORMAT)
            if vals.get('aa_date') else self.aa_date)
        aa_res =  (aa_resource.browse(vals.get('aa_resource_id'))
            if vals.get('aa_resource_id') else self.aa_resource_id)
        aa_plan = (vals.get('aa_plan_only')
            if vals.get('aa_plan_only') in [True, False] else self.aa_plan_only)
        if (vals.get('aa_plan_only') in [True, False] or
            vals.get('aa_resource_id') or vals.get('aa_date')):
            self.aa_name = self.aa_join_name_date(aa_res.name, aa_date, aa_plan)
        return super(aa_Capacity, self).write(vals)
