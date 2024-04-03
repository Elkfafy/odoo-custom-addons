# -*- coding: utf-8 -*-

from odoo import models, fields, api

class order(models.Model):
    _name = 'order'
    _description = "order for car rental"

    name = fields.Char(string="Name")
    state = fields.Selection(
        selection=[
            ("draft", 'Draft'), 
            ('review', "Review"), 
            ('accepted', "Accepted"), 
            ('rejected', "Rejected")],
        string="Status", 
        required=True, 
        copy=False,
        tracking=True,
        default="draft")
    driver_id = fields.Many2one("hr.employee", string="Driver")
    driver_license = fields.Binary(string="Driving License")
    
# class custom-delivery(models.Model):
#     _name = 'custom-delivery.custom-delivery'
#     _description = 'custom-delivery.custom-delivery'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

