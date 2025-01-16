from odoo import models, fields, api
from odoo.exceptions import UserError


class StockPicking(models.Model):
    _inherit = "stock.picking"
    
    def action_assign(self):
        for picking in self:
            for move in picking.move_ids:
                self.validar_stock_total()
                # Validar según el tipo de ubicación origen
                if move.location_id.usage == "production":
                    self._validate_production_move(move)
                elif move.location_id.usage == "internal":
                    self._validate_internal_move(move)
                elif (
                    move.location_id.usage == "transit"
                    and move.location_id.name != "Traslado entre almacenes"
                ):
                    self._validate_transit_move(move)
                elif move.location_id.usage == "supplier":
                    return super(StockPicking, self).action_assign()
                else:
                    return super(StockPicking, self).action_assign()

            return super(StockPicking, self).action_assign() 

    def action_confirm(self):
        for picking in self:
            for move in picking.move_ids:
                self.validar_stock_total()
                # Validar según el tipo de ubicación origen
                if move.location_id.usage == "production":
                    self._validate_production_move(move)
                elif move.location_id.usage == "internal":
                    self._validate_internal_move(move)
                elif (
                    move.location_id.usage == "transit"
                    and move.location_id.name != "Traslado entre almacenes"
                ):
                    self._validate_transit_move(move) 
                elif move.location_id.usage == "supplier":
                    return super(StockPicking, self).action_confirm()
                else:
                    return super(StockPicking, self).action_confirm()

            return super(StockPicking, self).action_confirm() 
    def button_validate(self):
        for picking in self:
            for move in picking.move_ids:
                self.validar_stock_total()
                # Validar según el tipo de ubicación origen
                if move.location_id.usage == "production":
                    self._validate_production_move(move)
                elif move.location_id.usage == "internal":
                    self._validate_internal_move(move)
                elif (
                    move.location_id.usage == "transit"
                    and move.location_id.name != "Traslado entre almacenes"
                ):
                    self._validate_transit_move(move)
                elif move.location_id.usage == "supplier":
                    return super(StockPicking, self).button_validate()
                else:
                    return super(StockPicking, self).button_validate()

        return super(StockPicking, self).button_validate()

    def _get_available_quant(self, move):
        """
        Obtiene el quant disponible para un movimiento específico.
        
        Args:
            move: Registro de movimiento de stock
            
        Returns:
            stock.quant: Primer quant encontrado que cumple con los criterios
        """
        domain = [
            ("product_id", "=", move.product_id.id),
            ("location_id", "=", move.location_id.id), 
            ("available_quantity", ">", 0),
        ]
        if move.lot_ids:
            domain.append(("lot_id", "in", move.lot_ids.ids))
        return self.env["stock.quant"].search(domain, limit=1)

    def _get_line_quant(self, move_line):
        """
        Obtiene el quant asociado a una línea de movimiento específica.
        
        Args:
            move_line: Línea de movimiento de stock
            
        Returns:
            stock.quant: Primer quant encontrado que cumple con los criterios
        """
        domain = [
            ("product_id", "=", move_line.product_id.id),
            ("location_id", "=", move_line.location_id.id),
        ]
        if move_line.lot_id:
            domain.append(("lot_id", "=", move_line.lot_id.id))
        return self.env["stock.quant"].search(domain, limit=1)

    @api.onchange("state")
    def onchange_state_no_negative(self):
        """
        Método que se ejecuta al cambiar el estado del picking.
        Actualmente solo imprime un mensaje de debug.
        """
        for picking_id in self:
            print("smn")

    def _raise_insufficient_stock_error(self, move_line, quant):
        """
        Lanza un error cuando no hay suficiente stock disponible.
        
        Args:
            move_line: Línea de movimiento de stock
            quant: Quant asociado al movimiento
            
        Raises:
            UserError: Error con mensaje detallado sobre el stock insuficiente
        """
        message = (
            f"Stock insuficiente en la ubicación de origen.\n"
            f"• Producto: {move_line.product_id.display_name}\n"
            f"• Ubicación: {move_line.location_id.complete_name}\n"
            f"• Lote: {move_line.lot_id.name if move_line.lot_id else 'N/A'}\n"
            f"• Cantidad requerida: {move_line.quantity}\n"
            f"• Cantidad disponible: {quant.quantity}"
        )
        raise UserError(message)

    def _raise_no_stock_error(self, move_line):
        """
        Lanza un error cuando no existe stock disponible.
        
        Args:
            move_line: Línea de movimiento de stock
            
        Raises:
            UserError: Error con mensaje detallado sobre la falta de stock
        """
        message = (
            f"No hay stock disponible en la ubicación de origen.\n"
            f"• Producto: {move_line.product_id.display_name}\n"
            f"• Ubicación: {move_line.location_id.complete_name}\n"
            f"• Lote: {move_line.lot_id.name if move_line.lot_id else 'N/A'}\n"
            f"• Cantidad requerida: {move_line.quantity}\n"
            f"• Cantidad disponible: 0"
        )
        raise UserError(message)

    def _raise_stock_error(self, location_type, move):
        """
        Lanza un error cuando se detecta stock negativo.
        
        Args:
            location_type: Tipo de ubicación donde se detectó el error
            move: Movimiento de stock asociado
            
        Raises:
            UserError: Error con mensaje detallado sobre el stock negativo
        """
        message = (
            f"Stock negativo detectado en ubicación de {location_type}.\n"
            f"• Producto: {move.product_id.product_tmpl_id.display_name}\n"
            f"• Ubicación: {move.location_id.complete_name}\n"
            f"Por favor, ajuste las cantidades o realice un ajuste de inventario."
        )
        raise UserError(message)

    def validar_stock_total(self):
        for picking in self:
            for move in picking.move_ids:
                if (
                    move.location_id.usage == "transit"
                    and move.location_id.name == "Traslado entre almacenes"
                ):
                    continue
                elif move.location_id.usage == "supplier":
                    continue

                # Obtener el stock disponible
                quants = self.env["stock.quant"].search(
                    [
                        ("product_id", "=", move.product_id.id),
                        ("location_id", "=", move.location_id.id),
                    ]
                )
                stock_disponible = sum(quant.quantity for quant in quants)

                if move.quantity > 0 and move.quantity > stock_disponible:
                    message = (
                        f"No hay suficiente stock disponible para el producto {move.product_id.display_name}.\n"
                        f"• Cantidad solicitada: {move.quantity}\n"
                        f"• Stock disponible: {stock_disponible}\n"
                        f"• Ubicación: {move.location_id.complete_name}\n"
                        f"Por favor, ajuste las cantidades o realice un ajuste de inventario."
                    )
                    raise UserError(message)

        return True

    def _validate_internal_move(self, move):
        for move_line in move.move_line_ids:
            quant = self._get_line_quant(move_line)

            # Validar series/lotes
            if move_line.product_id.tracking != "none":
                self._validate_lots(move_line)

            # Validar cantidades
            if not quant:
                self._raise_no_stock_error(move_line)
            elif quant.quantity < move_line.quantity:
                self._raise_insufficient_stock_error(move_line, quant)

    def _validate_lots(self, move_line):
        move_lot_ids = move_line.lot_id.ids if move_line.lot_id else []
        quants_with_lots = self.env["stock.quant"].search(
            [
                ("product_id", "=", move_line.product_id.id),
                ("location_id", "=", move_line.location_id.id),
                ("lot_id", "!=", False),
            ]
        )
        location_lot_ids = quants_with_lots.mapped("lot_id").ids

        if move_lot_ids and not all(
            lot_id in location_lot_ids for lot_id in move_lot_ids
        ):
            message = (
                f"Series/Lotes no encontrados en la ubicación de origen.\n"
                f"• Producto: {move_line.product_id.display_name}\n"
                f"• Ubicación: {move_line.location_id.complete_name}\n"
                f"• Series requeridas: {move_line.lot_id.name}\n"
                f"Por favor, verifique que las series existan en la ubicación."
            )
            raise UserError(message)

    def _validate_production_move(self, move):
        quant = self._get_available_quant(move)

        # Validar según tracking y cantidades
        if (
            (move.product_id.tracking == "serial" and bool(quant.reserved_quantity))
            or (move.product_qty <= quant.reserved_quantity and quant.available_quantity > 0)
            or (move.product_qty == 0 and quant.reserved_quantity >= quant.available_quantity)
            or (quant.available_quantity == 0 and quant.reserved_quantity >= move.product_qty)
            or (quant.available_quantity >= move.product_qty)
        ):
            return

        if quant.available_quantity == 0 or quant.reserved_quantity < move.quantity:
            self._raise_stock_error("Producción", move)

    def _validate_transit_move(self, move):
        quant = self._get_available_quant(move)

        if (
            (move.product_id.tracking == "serial" and bool(quant.reserved_quantity))
            or (
                move.quantity <= quant.reserved_quantity
                and quant.available_quantity > 0
            )
            or (move.quantity == 0 and quant.quantity >= quant.available_quantity)
            or (quant.available_quantity == 0 and quant.quantity >= move.quantity)
        ):
            return

        self._raise_stock_error("Tránsito", move)
