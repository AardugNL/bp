# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Caret IT Solutions Pvt. Ltd. (Website: www.caretit.com).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

import datetime
from odoo import models, fields, api


class aa_procedures(models.TransientModel):
    _name = 'aa.procedure'

    def aa_create_capacity_machine(self):
        tomorrow = fields.date.today() + datetime.timedelta(days=1)
        resources = self.env['resource.resource'].search([('active', '=', True),
            ('resource_type', '=', 'material')])
        for resource in resources:
            for day in range(300):
                nextDay = tomorrow + datetime.timedelta(days=day)
                capacity = self.env['aa.capacity.machine'].search([
                  ('aa_resource_id', '=', resource.id),
                    ('aa_date', '=', nextDay)])
                if capacity:
                    continue
                self.env['aa.capacity.machine'].create(
                    {'aa_ersource_id': resource.id,
                     'aa_plan_only': False,
                     'aa_date': nextDay,})
        self.env.cr.execute(""" UPDATE aa_capacity_machine
                                SET aa_plan_only=True
                                WHERE aa_is_sunday=True""")
