from odoo import models, _, fields
from odoo.exceptions import RedirectWarning


class StockQuant(models.Model):
    _inherit = 'stock.quant'

    code = fields.Char(related='location_id.code')
