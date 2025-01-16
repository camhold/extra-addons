{
    'name': 'Stock Move Available',
    'license': 'LGPL-3',
    'version': '17.0.0.0.1',
    'category': 'Stock',
    'summary': 'Columna Stock Disponible Transferencias internas',
    'description': """
        This module removes the readonly restriction on the date_done field in stock.picking model.
    """,
    'author': 'I+D, Diego Gajardo, Camilo Neira, Diego Morales',
    'website': 'https://www.holdconet.com',
    'depends': ['stock'],
    'data': [
        'views/stock_picking_views.xml',
    ],
}
