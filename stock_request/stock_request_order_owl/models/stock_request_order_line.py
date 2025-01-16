from odoo import models, fields, api

class StockRequestOrderLine(models.Model):
    _inherit = 'stock.request.order.line'

    available_qty = fields.Float(string='Available Quantity', compute='_compute_available_qty')

    @api.depends('product_id', 'warehouse_id')
    def _compute_available_qty(self):
        for line in self:
            if line.product_id and line.warehouse_id:
                line.available_qty = line.product_id.with_context(warehouse=line.warehouse_id.id).qty_available
            else:
                line.available_qty = 0
