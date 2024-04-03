from odoo import models, fields

class AhmedAccidents(models.Model):
    _name = 'accident'
    driver_name = fields.Many2one('res.partner', string="Driver Name")
    car_name = fields.Many2one('fleet.vehicle', string="Car Name")
    car_license = fields.Binary(string="Car License")