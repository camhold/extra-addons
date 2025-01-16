from odoo import models, fields

class StockMove(models.Model):
    _inherit = 'stock.move'

    available_qty = fields.Float(string='Cantidad disponible', compute='compute_demand_qty')

    def compute_demand_qty(self):
        for move_id in self:
            move_id.available_qty = (self.env['stock.quant']._get_available_quantity(move_id.product_id, move_id.location_id))
