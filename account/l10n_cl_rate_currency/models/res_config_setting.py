from datetime import timedelta
from odoo import api, fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    
    user_bc = fields.Char('Usuario BC', config_parameter='user_bc.setting')
    pass_bc = fields.Char('Password', config_parameter='pass_bc.setting')