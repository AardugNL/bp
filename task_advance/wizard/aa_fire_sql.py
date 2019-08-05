# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Caret IT Solutions Pvt. Ltd. (Website: www.caretit.com).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

from odoo import models, fields, api


class aa_fire_sql(models.TransientModel):
    _name = 'aa.fire.sql'

    aa_text = fields.Text()

    def aa_fire_sql(self):
    	print (">>",self.aa_text)