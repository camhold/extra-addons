# -*- encoding: utf-8 -*-

{
    'name': 'Rate Currency Chile',
    'version': '17.0.1.0.0',
    'category': 'Localization/Account',
    'license':'LGPL-3',
    "description": """
    	Actualiza Monedas Chilenas
	    (https://www.bcentral.cl)
    """,
    'author': 'Iván Masías - ivan.masias.ortiz@gmail.com',
    'website': 'https://github.com/esfingex',
    'depends': ['base','currency_rate_live'],
    'data': [
    	'data/currency_series.xml',
    	'views/res_currency.xml',
        'views/res_config_setting_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
