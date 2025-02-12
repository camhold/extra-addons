{
    'name': 'Stock Request Auto Cleanup',
    'version': '17.0.0.1',
    'category': 'Stock',
    'author': 'Adrian Hernandez',
    'depends': ['stock'],
    'data': [
        'data/cron_stock_request.xml',  # Archivo que define el cron
        'views/res_config_settings_views.xml',  # Vista de configuración en Ajustes
    ],
    'installable': True,
    'application': False,
}
