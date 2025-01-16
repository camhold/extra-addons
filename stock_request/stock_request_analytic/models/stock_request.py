from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)

class StockRequestOrder(models.Model):
    _inherit = 'stock.request.order'

    analytic_account_ids = fields.Many2many(
        'account.analytic.account',
        string='Analytic Accounts'
    )

    def action_confirm(self):
        res = super(StockRequestOrder, self).action_confirm()

        # Asignar cuentas analíticas a las transferencias creadas
        for order in self:
            analytic_accounts = order.analytic_account_ids
            if analytic_accounts:
                _logger.info(f"Assigning analytic accounts: {analytic_accounts.ids} to pickings created from order: {order.name}")

                # Asignar cuentas analíticas a los pickings creados
                for picking in order.picking_ids:
                    _logger.info(f"Processing picking ID: {picking.id} for order: {order.name}")

                    # Asignar las cuentas analíticas al picking
                    picking.write({'analytic_account_ids': [(6, 0, analytic_accounts.ids)]})

                    # Asignar cuentas analíticas a las líneas de movimiento del picking
                    if hasattr(picking, 'move_ids_without_package'):
                        move_lines = picking.move_ids_without_package
                    elif hasattr(picking, 'move_lines'):
                        move_lines = picking.move_lines
                    elif hasattr(picking, 'move_line_ids'):
                        move_lines = picking.move_line_ids
                    else:
                        move_lines = None

                    if move_lines:
                        _logger.info(f"Found move lines: {move_lines.ids} for picking: {picking.id}")
                        move_lines.write({'analytic_account_ids': [(6, 0, analytic_accounts.ids)]})
                    else:
                        _logger.warning(f"No move lines found for picking: {picking.id}")

        return res