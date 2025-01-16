from odoo import models, fields

class AccountMove(models.Model):
    _inherit = 'account.move'

    # Cambiamos a Many2one para simplificar la relación
    mp_flujo_id = fields.Many2one(
        'mp.flujo', 
        string='Flujo'
    )
    
    # Si solo necesitas un Grupo de Flujo principal, Many2one es suficiente
    mp_grupo_flujo_id = fields.Many2one(
        'mp.grupo.flujo', 
        string='Grupo de Flujo'
    )



# Modelo de AccountMoveLine que hereda relaciones de AccountMove
class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    # Campos related ajustados para mantener solo lo necesario
    mp_flujo_id = fields.Many2one(
        related='move_id.mp_flujo_id', 
        store=True,
        string='Flujo'
    )
    mp_grupo_flujo_id = fields.Many2one(
        related='move_id.mp_grupo_flujo_id', 
        store=True,
        string='Grupo de Flujo'
    )
    invoice_date = fields.Date(related='move_id.invoice_date', store=True)
    journal_id = fields.Many2one(related='move_id.journal_id', store=True)
    invoice_origin = fields.Char(related='move_id.invoice_origin', store=True)
    vat = fields.Char(related='move_id.partner_id.vat', store=True)
    code_account = fields.Char(
        related='account_id.code', 
        string='Número de Cuenta Contable', 
        store=True
    )
