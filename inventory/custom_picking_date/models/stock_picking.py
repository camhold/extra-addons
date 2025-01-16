from odoo import models, fields

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    date_done = fields.Datetime(readonly=False)
