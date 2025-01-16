{
    'name': 'Custom L10n CL Red box',
    'version': '1.0',
    'category': 'Localization',
    'summary': 'Modificaciones personalizadas al reporte de factura de l10n_cl',
    'description': '''
        Este módulo hereda la vista de reporte de facturas de l10n_cl y modifica:
        1. El color del borde de la caja que contiene el RUT y la factura.
        2. Cambia "VAT" por "IVA" en los detalles de impuestos.
    ''',
    'author': 'Diego Gajardo',
    'website': 'http://www.Holdconet.cl',
    'depends': ['l10n_cl'],
    'data': [
        'views/report_invoice_template_inherit.xml',
        'views/report_invoice_template_inherit_red_text.xml'
        #'views/tax_totals_widget_inherit.xml'
    ],
    'installable': True,
    'auto_install': False,
}
