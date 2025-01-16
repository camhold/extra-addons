{
    'name': 'MP Inventario',
    'version': '17.0.0.1',
    'category': 'Inventory',
    'author': 'Adrian Hernandez',
    'depends': ['stock','stock_request'],
    'data': [
        'security/mp_inventario_security.xml',
        'security/ir.model.access.csv',
        'views/mp_inventario_view.xml',
    ],
    'installable': True,
    'application': True,
}
