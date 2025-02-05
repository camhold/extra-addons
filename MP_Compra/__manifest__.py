{
    'name': 'MP Compra',
    'version': '17.0.0.1',
    'category': 'purchase',
    'author': 'Adrian Hernandez',
    'depends': ['base', 'stock', 'product','account','purchase'],
    'data': [
        'views/mp_compras_views.xml',
    ],
    'application': True,
    'installable': True,
    'auto_install': False,
}
