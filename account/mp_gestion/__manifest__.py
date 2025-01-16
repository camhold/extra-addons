{
    'name': "MP Gestion",
    'summary': "Se agrega la gestión para la contabilidad",
    'author': 'I+D, Diego Gajardo, Camilo Neira, Diego Morales',
    'website': 'https://www.holdconet.com',
    'category': 'account',
    'version': '17.0.0.0.1',
    'depends': ['account', 'l10n_latam_invoice_document'],
    'data': [
        'security/mp_gestion_group.xml',
        'security/ir.model.access.csv',
        'views/account_move_views.xml',
    ],
    'license': 'Other proprietary',
}
