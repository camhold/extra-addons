from odoo import api, fields, models

class ResCurrency(models.Model):
    _inherit = 'res.currency'
    
    series = fields.Char(string='Series')