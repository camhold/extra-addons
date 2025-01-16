from odoo import api, Command, fields, models


class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    code = fields.Char(string='ID Netbox', related='location_dest_id.code')
    date_done = fields.Datetime(string='Fecha consumo', related='picking_id.date_done')
    name_trans = fields.Char(string='No Trans.', related='picking_id.name')
    location_origin_id = fields.Many2one(string='Ubicacion de Origen', related='picking_id.location_id')
    location_dest_id = fields.Many2one(string='Ubicacion de Destino', related='picking_id.location_dest_id')
    default_code = fields.Char(string='Referencia Interna', related='product_id.default_code')
    name_product = fields.Char(string='Nombre Articulo', related='product_id.name')
    standard_price = fields.Float(string='Costo Unitario', related='product_id.standard_price')
    total = fields.Float(string='Precio Total', compute='_compute_total')
    usage = fields.Selection(related='location_dest_id.usage')

    def _compute_total(self):
        for move_line_id in self:
            move_line_id.total = move_line_id.standard_price * move_line_id.quantity
