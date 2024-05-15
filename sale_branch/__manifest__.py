{
    'name': 'Sale Branch',
    'depends': [
        'sale',
        'account',
    ],
    'data': [
        'security/ir.model.access.csv',

        'views/sale_order_views.xml',
        'views/sale_menus.xml',
    ],
    'application': True,
    'license': 'LGPL-3',
}