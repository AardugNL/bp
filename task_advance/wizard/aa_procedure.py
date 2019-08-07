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
                    {'aa_resource_id': resource.id,
                     'aa_plan_only': False,
                     'aa_date': nextDay,})
                 
        #should not be necessary TODO
        self.env.cr.execute(""" DELETE FROM aa_capacity_machine 
                                    WHERE aa_resource_id IS NULL;
                            """)
        
        #should not be necessary TODO
        self.env.cr.execute(""" DELETE FROM project_task 
                                    WHERE aa_capacity_machine_id IS NULL; 
                            """)
        
        #should not be necessary TODO this is not correct for tasks without aa_capacity_machine!!
        self.env.cr.execute("""
                            DELETE FROM aa_capacity_machine where aa_date < '2019-08-01';
                            DELETE FROM project_task WHERE date_start < '2019-08-01';
                            """)
        
        
        
        self.env.cr.execute("""  UPDATE aa_capacity_machine 
                                    SET aa_plan_only = False
                            """)
        
        self.env.cr.execute("""
                                UPDATE aa_capacity_machine 
                                    SET aa_plan_only = True WHERE EXTRACT(DOW FROM aa_date) = 0;
                            """)

        self.env.cr.execute("""
                                UPDATE aa_capacity_machine
                                    SET aa_name = CONCAT(resource_resource.aa_code,'|', TO_CHAR( aa_date, 'DD-MON-YYYY (IW|DY)')) 
                                    FROM resource_resource
                                    WHERE aa_plan_only = FALSE AND  resource_resource.id = aa_capacity_machine.aa_resource_id;

                                UPDATE aa_capacity_machine
                                    SET aa_name = CONCAT(resource_resource.aa_code,'|', TO_CHAR( aa_date, 'DD-MON-YYYY'), '(PLAN)') 
                                    FROM resource_resource
                                    WHERE aa_plan_only = TRUE AND  resource_resource.id = aa_capacity_machine.aa_resource_id;
                            """)

        self.env.cr.execute("""
                                UPDATE aa_capacity_machine 
                                    SET aa_html = CONCAT('<div style="width: 200px; background-color : #7c7bad; color: white; padding-left: 4px">PLAN ONLY (SUN)</div>')
                                    WHERE aa_plan_only = True;
                            """)

        self.env.cr.execute("""
                                UPDATE aa_capacity_machine SET aa_html = 
                                    CONCAT('<div style="width: 220px; opacity: ', CASE WHEN aa_capacity_machine.aa_date < current_date THEN '0.1' ELSE '1' END, '">',
                                            '<div style="padding: 2px; border: 1px solid #ededed; border-radius: 2px">',
                                            '<div style="display:inline-block; width: ', RANDOM() * 50,'%; background-color: #00a09d; border-top-left-radius: 2px; border-bottom-left-radius: 2px">&nbsp;</div>',
                                            '<div style="display:inline-block; width: ', RANDOM() * 50,'%; background-color: darkorange; border-top-right-radius: 2px; border-bottom-right-radius: 2px">&nbsp;</div>',
                                            '</div>', 
                                            '<div style="margin: 2px; padding: 0 2px 0 2px; background-color: #e2e2e0; color: white; border-radius: 2px; width: 62px; display:inline-block">TASK:<div style="width:20px; text-align: right; display:inline-block">', floor(random() * 10 + 1)::int, '</div></div>',
                                            '<div style="margin: 2px; padding: 0 2px 0 2px; background-color: #e2e2e0; color: white; border-radius: 2px; width: 62px; display:inline-block">PRIO:<div style="width:20px; text-align: right; display:inline-block">', floor(random() * 10 + 1)::int, '</div></div>',
                                            '<div style="margin: 2px; padding: 0 2px 0 2px; background-color: #b5383a; color: white; border-radius: 2px; width: 62px; display:inline-block">LATE:<div style="width:20px; text-align: right; display:inline-block">', floor(random() * 10 + 1)::int, '</div></div>',
                                            '</div>')
                                    WHERE aa_plan_only = False;
                            """)
                            
        self.env.cr.execute("""
                            UPDATE project_task 
                                SET description = aa_capacity_machine.aa_html
                                FROM aa_capacity_machine
                                WHERE aa_capacity_machine.id = project_task.aa_capacity_machine_id AND project_task.aa_startup = True;
                            """)

        self.env.cr.execute("""
                             UPDATE project_task 
                                SET description = CONCAT('<div style="">' , 
                                '<span style="color: ', CASE WHEN aa_freeze = True THEN 'darkorange' ELSE 'grey' END,'; margin: 0 2px 0 2px"><li class="fa fa-lock fa-2x"></li></span>',
                                '<span style="color: grey; margin: 0 2px 0 2px"><li class="fa fa-exchange fa-2x"></li></span>',
                                '<span style="color: grey; margin: 0 2px 0 2px"><li class="fa fa-chevron-circle-right fa-2x"></li></span>',
                                '<span style="color: darkorange; margin: 0 2px 0 2px"><li class="fa fa-exclamation-circle fa-2x"></li></span>',
                                '<table border="0px solid black" cellpadding="2">
                                <tr><td>CUST:</td><td style="color: black" colspan="3" nowrap>',UPPER(SUBSTRING(res_partner.display_name FROM 0 FOR 16)), ',', UPPER(SUBSTRING(res_partner.city FROM 0 FOR 16)),'</td></tr>
                                <tr><td>REFE:</td><td style="color: black" colspan="3" nowrap>',UPPER(SUBSTRING(sale_order.client_order_ref FROM 0 FOR 32)),'</td></tr>
                                <tr><td>PLAN:</td><td style="color: black" nowrap>',TO_CHAR(sale_order.confirmation_date, 'DD-MON-YYYY'),'</td><td style=" color: black" nowrap>','','</td><td></td></tr>
                                <tr style="background-color: #e2e2e0"><td>PRN1:</td><td style=" color: black; width: 120px" nowrap>TASK 1</td><td style="width:40px; text-align: right; color: black"  nowrap>30-JUL-2019</td><td><span style="font-size: 12px; color: dodgerblue; margin-left: 0 2px 0 2px"><li class="fa fa-check-square fa-1x"></li></span></td></tr>
                                <tr><td>PRN3:</td><td style="color: black; width: 120px" nowrap>TASK 2</td><td style="width:40px; text-align: right; color :black" nowrap>30-JUL-2019</td><td><span style="font-size: 12px; color: grey;       margin-left: 0 2px 0 2px"><li class="fa fa-check-square fa-1x"></li></span></td></tr>
                                <tr><td>CAR1:</td><td style="color: black; width: 120px" nowrap>TASK 3</td><td style="width:40px; text-align: right; color: black nowrap">31-JUL-2019</td><td><span style="font-size: 12px; color: #1d9e74;    margin-left: 0 2px 0 2px"><li class="fa fa-arrow-right  fa-1x"></li></span></td></tr>
                                <tr><td>SUPP:</td><td style="color: black; width: 120px" nowrap>TASK 4</td><td style="width:40px; text-align: right; color :red" nowrap>31-JUL-2019</td><td><span style="font-size: 12px; color: grey;       margin-left: 0 2px 0 2px"><li class="fa fa-arrow-left   fa-1x"></li></span></td></tr>
                                <tr><td>STUD</td><td style="color: black; width: 120px" nowrap>TASK 5</td><td style="width: 40px; text-align: right; color: black" nowrap>31-JUL-2019</td><td><span style="font-size: 12px; color: dodgerblue; margin-left: 0 2px 0 2px"><li class="fa fa-check-square fa-1x"></li></span></td></tr>
                                <tr><td>QUAL</td><td style="color: black; width: 120px" nowrap>TASK 5</td><td style="width:40px; text-align: right; color :red"  nowrap>31-JUL-2019</td><td><span style="font-size: 12px; color: grey;       margin-left: 0 2px 0 2px"><li class="fa fa-check-square fa-1x"></li></span></td></tr>
                                </table>',
                                '</div>'
                                )
                            FROM sale_order
                            INNER JOIN res_partner ON res_partner.id = sale_order.partner_id 
                            WHERE sale_order.id = project_task.sale_order_id AND project_task.aa_startup = False;
                            """)



