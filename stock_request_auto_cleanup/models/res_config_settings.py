from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    stock_request_auto_cleanup_enabled = fields.Boolean(
        string="Activar Auto Cleanup de Stock Request Orders",
        config_parameter='stock_request_auto_cleanup.enabled',
        default=False
    )
    stock_request_auto_cleanup_days = fields.Integer(
        string="Días para Cleanup",
        config_parameter='stock_request_auto_cleanup.days',
        default=30,
        help="Número de días para considerar vencida la expected_date (valor entre 15 y 90)."
    )

    @api.constrains('stock_request_auto_cleanup_days')
    def _check_cleanup_days(self):
        for rec in self:
            if rec.stock_request_auto_cleanup_days:
                if rec.stock_request_auto_cleanup_days < 15 or rec.stock_request_auto_cleanup_days > 90:
                    raise ValidationError(_("El número de días debe estar entre 15 y 90."))

    def set_values(self):
        """ Actualiza el estado del cron según el checkbox en Ajustes """
        super(ResConfigSettings, self).set_values()

        param_obj = self.env['ir.config_parameter'].sudo()
        enabled = self.stock_request_auto_cleanup_enabled

        # Buscar el cron para actualizar su estado
        cron_job = self.env.ref('stock_request_auto_cleanup.ir_cron_delete_old_requests', raise_if_not_found=False)
        
        if cron_job:
            cron_job.write({'active': enabled})
            if enabled:
                print("[INFO] Auto Cleanup activado: El cron se ejecutará automáticamente.")
            else:
                print("[INFO] Auto Cleanup desactivado: El cron ha sido pausado.")
