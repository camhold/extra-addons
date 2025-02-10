{
    'name': 'MP Compra',
    'version': '17.0.0.1',
    'category': 'purchase',
    'author': 'Adrian Hernandez',
    'depends': ['base', 'stock', 'product','account','purchase'],
    'data': [
        'security/mp_compras_security.xml',
        'security/ir.model.access.csv',
        'views/mp_compras_views.xml',
    ],
    'application': True,
    'installable': True,
    'auto_install': False,
}
