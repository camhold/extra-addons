{
    'name': 'Stock Request Order OWL Plugin',
    'version': '1.0',
    'category': 'Warehouse',
    'summary': 'OWL Plugin for Stock Request Order Lines',
    'depends': ['stock', 'stock_account'],
    'data': [
        'views/stock_request_order_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'stock_request_order_owl/static/src/js/stock_request_order.js',
        ],
    },
}
