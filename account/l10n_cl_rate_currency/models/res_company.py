# -*- coding: utf-8 -*-
import logging
import bcchapi
from odoo import api, fields, models
from odoo.addons.currency_rate_live.models.res_config_settings import CURRENCY_PROVIDER_SELECTION

CURRENCY_PROVIDER_SELECTION_EXTEND = [
    (['CL'], 'cl_bank', '[CL] Banco Central API'),
]

CURRENCY_PROVIDER_SELECTION.extend(CURRENCY_PROVIDER_SELECTION_EXTEND)

class ResCompany(models.Model):
    _inherit = 'res.company'
    
    currency_provider = fields.Selection(
        selection_add=[
            ('cl_bank', '[CL] Banco Central API')
        ],
    )

    def _parse_cl_bank_data(self, available_currencies):
        
        icp = self.env['ir.config_parameter'].sudo()
        user_bc = icp.get_param('user_bc.setting')
        pass_bc = icp.get_param('pass_bc.setting')
        
        available_currency_series = available_currencies.mapped('series')
        available_currency_name = available_currencies.mapped('name')
        today_date = fields.Date.context_today(self.with_context(tz='America/Santiago'))
        
        # Incluyendo credenciales explícitamente
        siete = bcchapi.Siete(user_bc, pass_bc)
        
        value = siete.cuadro(
            series=available_currency_series[1:],  
            nombres=available_currency_name[1:],
            desde=str(today_date),
            hasta=str(today_date), 
        )
        
        value = value.fillna('None')
        
        rslt = {
            'CLP': (1.0, fields.Date.to_string(today_date)),
        }

        for index, row in value.iterrows():
            for col, value in row.items():
                if value != 'None':
                    date = str(index.date())
                    rate = value
                    rslt[col] = (1.0 / rate,  date)
            
        return rslt