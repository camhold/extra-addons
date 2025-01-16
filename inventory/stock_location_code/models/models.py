from odoo import models, fields, api
from odoo.exceptions import ValidationError

class StockLocation(models.Model):
    _inherit = 'stock.location'

    code = fields.Char(string='Código Netbox')

