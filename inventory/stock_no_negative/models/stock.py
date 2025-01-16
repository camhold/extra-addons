from odoo import _, models, api
from odoo.exceptions import UserError

class StockQuant(models.Model):
    _inherit = "stock.quant"

    def _prepare_error_params(self, product_id, location_id, quantity):
        return {
            "lot_qty": quantity,
            "product_name": product_id.name,
            "location_name": location_id.complete_name,
        }

    def _validate_production_stock(self, error_params):
        message = _(
            "Stock negativo detectado en ubicación de producción.\n"
            "• Producto: %(product_name)s\n"
            "• Ubicación: %(location_name)s\n"
            "• Stock resultante: %(lot_qty)s unidades\n\n"
            "Por favor, ajuste las cantidades o realice un ajuste de inventario."
        )
        raise UserError(message % error_params)

    def _validate_internal_stock(self, error_params):
        message = _(
            "Stock negativo detectado en almacén interno.\n"
            "• Producto: %(product_name)s\n"
            "• Ubicación: %(location_name)s\n"
            "• Stock resultante: %(lot_qty)s unidades\n\n"
            "Por favor, ajuste las cantidades o realice un ajuste de inventario."
        )
        raise UserError(message % error_params)

    def _validate_transit_stock(self, error_params):
        message = _(
            "Stock negativo detectado en ubicación de tránsito.\n"
            "• Producto: %(product_name)s\n"
            "• Ubicación: %(location_name)s\n"
            "• Stock resultante: %(lot_qty)s unidades\n\n"
            "Por favor, ajuste las cantidades o realice un ajuste de inventario."
        )
        raise UserError(message % error_params)


class StockMove(models.Model):
    _inherit = "stock.move"

    def action_assign(self):
        # No realizamos ninguna validación, simplemente llamamos al método original
        return super().action_assign()
