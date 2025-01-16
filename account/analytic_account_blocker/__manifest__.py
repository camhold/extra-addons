{
    'name': 'Analytic Account Blocker',
    'version': '1.0',
    'category': 'Accounting',
    'summary': 'Block analytic accounts while still allowing them to be viewed.',
    'description': """
        This module adds a boolean field to analytic accounts to block them
        from being used but allows users to still consult them.
    """,
    'depends': ['stock_request', 'account'],
    'data': [
        'views/analytic_account_views.xml',
    ],
    'installable': True,
    'application': False,
}
