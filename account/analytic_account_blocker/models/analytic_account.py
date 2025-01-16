from odoo import models, fields, api
from datetime import datetime

class AnalyticAccount(models.Model):
    _inherit = 'account.analytic.account'

    is_blocked = fields.Boolean(string="Bloqueado", default=False, help="If blocked, this analytic account cannot be used.", tracking=True)
    blocked_by_employee = fields.Many2one('hr.employee', string="Bloqueado por :", help="Employee who requested the blocking", tracking=True)
    blocked_date = fields.Datetime(string="Fecha Bloqueo", readonly=True, help="Date when the analytic account was blocked", tracking=True)
    blocked_reason = fields.Text(string="Descripcion del Bloqueo", help="Reason for blocking the analytic account", tracking=True)

    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        # Añadir el dominio para excluir cuentas bloqueadas
        args += [('is_blocked', '=', False)]
        return super(AnalyticAccount, self).search(args, offset=offset, limit=limit, order=order)

    @api.constrains('is_blocked')
    def _check_blocked(self):
        for record in self:
            if record.is_blocked and not record.blocked_date:
                # Registrar la fecha de bloqueo si no está ya establecida
                record.blocked_date = fields.Datetime.now()

    @api.onchange('is_blocked')
    def _onchange_is_blocked(self):
        if self.is_blocked:
            self.blocked_date = fields.Datetime.now()
        else:
            self.blocked_by_employee = False
            self.blocked_date = False
            self.blocked_reason = False
