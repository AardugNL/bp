# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Caret IT Solutions Pvt. Ltd. (Website: www.caretit.com).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

from odoo import api, exceptions, fields, models, _


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    resource_id = fields.Many2one('resource.resource', string='Machine')
    capacity_machine_id = fields.Many2one('capacity.machine',
        string='Machine Capacity')
    preproduction_time = fields.Float('Pre Production Time')
    production_time_1 = fields.Float('Production Time 1')
    production_time_2 = fields.Float('Production Time 2')
    production_time_3 = fields.Float('Production Time 3')
    postproduction_time = fields.Float('Post Production Time')
    max_production_time= fields.Float('Max Production Time')
