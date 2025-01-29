from odoo import models, fields, api

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    last_purchase_date = fields.Datetime(
        string="Fecha Última Compra",
        compute='_compute_last_purchase_info',
    )
    last_purchase_partner_id = fields.Many2one(
        'res.partner',
        string="Último Proveedor",
        compute='_compute_last_purchase_info',
    )
    last_purchase_cost = fields.Float(
        string="Último Costo de Compra",
        compute='_compute_last_purchase_info',
    )
    current_debt = fields.Float(
        string="Deuda Actual",
        compute='_compute_last_purchase_info',
    )

    @api.depends()
    def _compute_last_purchase_info(self):
        """
        Obtiene la última compra (purchase.order.line) para cualquiera de las variantes
        del producto y, a partir de esa orden de compra, busca las facturas (account.move)
        para calcular la deuda pendiente (amount_residual).
        """
        PurchaseOrderLine = self.env['purchase.order.line']
        AccountMove = self.env['account.move']

        for template in self:
            # Si no tiene variantes, no hay nada que calcular
            product_ids = template.product_variant_ids.ids
            if not product_ids:
                template.last_purchase_date = False
                template.last_purchase_partner_id = False
                template.last_purchase_cost = 0.0
                template.current_debt = 0.0
                continue

            # Buscar la LÍNEA de compra más reciente (orden confirmada o hecha)
            lines = PurchaseOrderLine.search([
                ('product_id', 'in', product_ids),
                ('order_id.state', 'in', ['purchase', 'done']),
            ], order='create_date desc', limit=1)

            if not lines:
                # No hay compras para este producto
                template.last_purchase_date = False
                template.last_purchase_partner_id = False
                template.last_purchase_cost = 0.0
                template.current_debt = 0.0
                continue

            # Tomar la línea más reciente
            line = lines[0]
            po = line.order_id

            template.last_purchase_date = po.date_order
            template.last_purchase_partner_id = po.partner_id
            template.last_purchase_cost = line.price_unit

            # Buscar las facturas relacionadas a ESA orden de compra
            moves = AccountMove.search([
                ('move_type', '=', 'in_invoice'),         # Facturas de proveedor
                ('invoice_origin', 'ilike', po.name),     # Relacionado con la PO
                ('partner_id', '=', po.partner_id.id),    # Mismo proveedor
                ('state', '=', 'posted'),                 # Factura publicada
                ('payment_state', '!=', 'paid'),          # Pendiente de pago
            ])

            # Sumar la deuda (amount_residual) de esas facturas
            total_deuda = sum(moves.mapped('amount_residual'))

            template.current_debt = total_deuda
