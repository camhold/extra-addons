{
    'name': 'Stock Location Code',
    'version': '17.0.1.0.0',
    'category': 'Warehouse',
    'summary': 'Adds a unique alphanumeric code to stock locations',
    'author': 'I+D, Diego Gajardo, Camilo Neira, Diego Morales',
    'website': 'https://www.holdconet.com',
    'depends': ['stock'],
    'data': [
        'views/stock_location_views.xml',
        'data/ir.model.access.csv',
    ],
    'installable': True,
    'application': False,
}
