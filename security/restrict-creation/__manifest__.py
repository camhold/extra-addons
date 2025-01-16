{
    'name': 'Restrict Creation',
    'version': '1.2',
    'category': 'Customization',
    'summary': 'Restrict creation of new products and contacts in selection fields',
    'author': 'I+D, Diego Gajardo, Camilo Neira, Diego Morales',
    'website': 'https://www.holdconet.com',
    'depends': ['product', 'contacts', 'account', 'sale','purchase','stock'],
    'data': [
        'views/restrict_account_invoice.xml',
        'views/restrict_purchase_order.xml',
        'views/restrict_sale_order_line.xml',
        'views/restrict_stock_picking.xml',
        'views/restrict_account_payment.xml',
        'views/res_config_settings_views.xml',
        'views/res_users_views.xml',

        'security/ir.model.access.csv'
    ],
    'installable': True,
    'application': False,
}
