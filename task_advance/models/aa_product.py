# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Caret IT Solutions Pvt. Ltd. (Website: www.caretit.com).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

from odoo import api, exceptions, fields, models, _


class aa_ProductTemplate(models.Model):
    _inherit = 'product.template'

    aa_resource_id = fields.Many2one('resource.resource', string='Machine')
    # aa_capacity_machine_id = fields.Many2one('aa.capacity.machine',
    #     string='Machine Capacity')
    aa_preproduction_time = fields.Float('Pre Production Time')
    aa_production_time_1 = fields.Float('Production Time 1')
    aa_production_time_2 = fields.Float('Production Time 2')
    aa_production_time_3 = fields.Float('Production Time 3')
    aa_postproduction_time = fields.Float('Post Production Time')
    aa_max_production_time= fields.Float('Max Production Time')
    aa_product_lead_time = fields.Float('Product Lead Time')
