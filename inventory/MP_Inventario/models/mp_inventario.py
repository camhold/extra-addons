from odoo import models, fields, api

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    fecha_movimiento = fields.Datetime(compute='_compute_fecha_movimiento', string="Fecha Movimiento")
    origen_movimiento = fields.Char(related='origin', string="Origen del Movimiento")
    productos_tags = fields.Many2many('product.product', string="Productos (Tags)", compute='_compute_productos_tags')
    tipo_operacion = fields.Selection(related='picking_type_id.code', string="Tipo de Operación")
    ubicacion_origen = fields.Many2one('stock.location', related='location_id', string="Ubicación de Origen")
    ubicacion_destino = fields.Many2one('stock.location', related='location_dest_id', string="Ubicación de Destino")
    cantidad = fields.Float(compute='_compute_cantidad', string="Cantidad")
    demanda = fields.Float(compute='_compute_demanda', string="Demanda")
    # Campo Many2many para mostrar números de serie/lote como tags
    lotes_tags = fields.Many2many('stock.lot', string="Lotes (Tags)", compute='_compute_lotes_tags')
    #total_costo_unitario = fields.Float(compute='_compute_total_costo_unitario', string="Total Costo Unitario")
    analytic_account_ids = fields.Many2many('account.analytic.account', string="Cuentas Analíticas")

    @api.depends('move_ids_without_package.date')
    def _compute_fecha_movimiento(self):
        for record in self:
            fechas = record.move_ids_without_package.mapped('date')
            record.fecha_movimiento = fechas[0] if fechas else False
        
    @api.depends('move_line_ids.quantity')
    def _compute_cantidad(self):
        for record in self:
            cantidades = record.move_line_ids.mapped('quantity')
            record.cantidad = sum(cantidades)

    @api.depends('move_ids_without_package.product_uom_qty')
    def _compute_demanda(self):
        for record in self:
            cantidades_demandadas = record.move_ids_without_package.mapped('product_uom_qty')
            record.demanda = sum(cantidades_demandadas)
        ''' 
    @api.depends('move_line_ids.product_id', 'move_line_ids.quantity')
    def _compute_total_costo_unitario(self):
        for record in self:
            total = 0.0
            # Por cada línea, multiplicamos el costo unitario del producto por la cantidad movida
            for line in record.move_line_ids:
                total += line.product_id.standard_price * line.quantity
            record.total_costo_unitario = total
        '''
    @api.depends('move_ids_without_package.product_id')
    def _compute_productos_tags(self):
        for record in self:
            productos = record.move_ids_without_package.mapped('product_id')
            record.productos_tags = productos

    @api.depends('move_line_ids.lot_id')
    def _compute_lotes_tags(self):
        for record in self:
            lotes = record.move_line_ids.mapped('lot_id')
            record.lotes_tags = lotes
class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    fecha_movimiento = fields.Datetime(compute='_compute_fecha_movimiento', string="Fecha Movimiento")
    origen_movimiento = fields.Char(related='move_id.origin', string="Origen del Movimiento")
    producto = fields.Many2one('product.product', related='product_id', string="Producto")
    ubicacion_origen = fields.Many2one('stock.location', related='location_id', string="Ubicación de Origen")
    ubicacion_destino = fields.Many2one('stock.location', related='location_dest_id', string="Ubicación de Destino")
    cantidad = fields.Float(compute='_compute_cantidad', string="Cantidad")
    tipo_operacion = fields.Selection(related='picking_type_id.code', string="Tipo de Operación")
    #costo_unitario = fields.Float(compute='_compute_costo_unitario', string="Costo Unitario")
    lote_tags = fields.Many2many('stock.lot', string="Lotes (Tags)", compute='_compute_lote_tags')
    demanda = fields.Float(compute='_compute_demanda', string="Demanda")
    analytic_account_ids = fields.Many2many('account.analytic.account', string="Cuentas Analíticas")

    @api.depends('move_id.date')
    def _compute_fecha_movimiento(self):
        for record in self:
            record.fecha_movimiento = record.move_id.date

    @api.depends('quantity')
    def _compute_cantidad(self):
        for record in self:
            record.cantidad = record.quantity
    '''
    @api.depends('product_id.standard_price')
    def _compute_costo_unitario(self):
        for record in self:
            record.costo_unitario = record.product_id.standard_price
    '''
    @api.depends('lot_id')
    def _compute_lote_tags(self):
        for record in self:
            record.lote_tags = record.lot_id
            
    @api.depends('quantity_product_uom')
    def _compute_demanda(self):
        for record in self:
            cantidades_demandadas = record.mapped('quantity_product_uom')
            record.demanda = sum(cantidades_demandadas)
