from odoo import models, fields, api, _
from odoo.exceptions import UserError

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
    purchase_line_count = fields.Integer(
        string="Líneas de Compra",
        compute="_compute_purchase_line_count",
        store=True
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

    def action_view_sales(self):
        # Verifica la condición antes de continuar
        if not self.sale_ok:
            raise UserError(_("La acción no puede ejecutarse porque sale_ok es False."))
        # Lógica original de la acción...
        return True

    @api.depends('purchase_ok')
    def _compute_purchase_line_count(self):
        PurchaseLine = self.env['purchase.order.line']
        # Se cuenta sólo las líneas de compra de órdenes en estado 'purchase' o 'done'
        data = PurchaseLine.read_group(
            [
                ('product_id.product_tmpl_id', 'in', self.ids),
                ('order_id.state', 'in', ['purchase', 'done'])
            ],
            ['product_id'],
            ['product_id']
        )
        # Creamos un diccionario que asocie el id del producto con la cantidad contada
        mapped_data = {d['product_id'][0]: d['product_id_count'] for d in data}
        for product in self:
            product.purchase_line_count = mapped_data.get(product.id, 0)

    def action_view_purchase_lines(self):
        self.ensure_one()
        if not self.purchase_ok:
            raise UserError(_("El producto no está configurado para compras."))

        # Obtenemos la acción que muestra el historial de compra.
        try:
            action = self.env.ref('purchase.purchase_history_tree').read()[0]
        except ValueError:
            raise UserError(_("No se encontró la acción de historial de compras. Verifica que el módulo Purchase esté instalado y que el external id sea correcto."))

        # líneas de compra se relaciona el producto con 'product_id'
        action['domain'] = [('order_line.product_id', '=', self.id)]
        return action