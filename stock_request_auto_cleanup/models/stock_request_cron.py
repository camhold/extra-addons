from datetime import timedelta
from odoo import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)

class StockRequestOrderCron(models.Model):
    _name = 'stock.request.order.cron'
    _description = 'Cron para cancelar órdenes de stock con expected_date vencida'

    def cancel_old_requests(self):
        """ Encuentra órdenes con expected_date vencida y estado en draft o submitted, y las pone en estado cancel. 
            También cancela las solicitudes (`stock.request`) asociadas a la orden cancelada. """
        param_obj = self.env['ir.config_parameter'].sudo()
        enabled = param_obj.get_param('stock_request_auto_cleanup.enabled', default='False')

        if enabled != 'True':
            print("[INFO] Auto Cleanup de Stock Request Order está desactivado en configuración.")
            _logger.info("Auto Cleanup de Stock Request Order está desactivado en configuración.")
            return

        try:
            days = int(param_obj.get_param('stock_request_auto_cleanup.days', default='30'))
            if days < 15 or days > 90:
                days = 30
        except ValueError:
            days = 30

        today = fields.Date.today()
        threshold_date = today - timedelta(days=days)

        stock_request_order_model = self.env['stock.request.order']
        old_orders = stock_request_order_model.search([
            ('expected_date', '<', threshold_date),
            ('state', 'in', ['draft', 'submitted'])  # Solo cancelar si están en draft o enviado
        ])

        odoobot = self.env.ref('base.partner_root')  # Referencia a OdooBot

        if not old_orders:
            print("[INFO] No se encontraron órdenes de stock vencidas para cancelar.")
            _logger.info("No se encontraron órdenes de stock vencidas para cancelar.")
            return

        # Obtener las opciones de estado del modelo
        state_selection = dict(self.env['stock.request.order'].fields_get()['state']['selection'])

        for order in old_orders:
            previous_state = order.state  # Guardamos el estado anterior

            order.write({'state': 'cancel'})  # Cambia el estado a cancelado
            
            # Ejecutar la acción de cancelación del modelo si existe
            if hasattr(order, '_action_cancel'):
                order._action_cancel()

            # Obtener el nombre del estado anterior
            previous_state_name = state_selection.get(previous_state, previous_state)

            # Agregar un mensaje en el chatter como si fuera OdooBot
            order.message_post(
                body=_(
                    "Esta orden de stock fue cancelada por OdooBot debido a que excedió los {} días desde su creación. "
                    "El estado anterior era: {}."
                ).format(days, previous_state_name),
                author_id=odoobot.id
            )

            # ** Cancela las solicitudes de stock (`stock.request`) asociadas**
            stock_requests = self.env['stock.request'].search([('order_id', '=', order.id)])

            for request in stock_requests:
                previous_request_state = request.state
                request.write({'state': 'cancel'})

                # Registrar el mensaje en el chatter
                request.message_post(
                    body=_(
                        "Esta solicitud de stock fue cancelada automáticamente porque la orden asociada ({}) "
                        "fue cancelada por OdooBot."
                    ).format(order.name),
                    author_id=odoobot.id
                )

                print(f"[INFO] Se canceló la solicitud de stock: {request.name} "
                      f"(ID: {request.id}) porque su orden asociada fue cancelada.")

                _logger.info(f"Solicitud de stock '{request.name}' cancelada automáticamente "
                             f"porque la orden '{order.name}' fue cancelada.")

            # Imprimir en consola
            print(f"[INFO] Se canceló la orden de stock: {order.name} (ID: {order.id}) "
                  f"Estado anterior: {previous_state_name} → Estado actual: cancel")

            # Registrar log en Odoo
            _logger.info(f"Orden de stock '{order.name}' cancelada por OdooBot (excedió {days} días). "
                         f"Estado anterior: {previous_state_name} → Estado actual: cancel")

        print(f"[INFO] Total de órdenes canceladas: {len(old_orders)} con expected_date anterior a {threshold_date}")
        _logger.info(f"Total de órdenes canceladas: {len(old_orders)} con expected_date anterior a {threshold_date}")
