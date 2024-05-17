{
    'name': 'Real Estate',
    'category': 'Real Estate/Brokerage',
    'depends': [
        'base'
    ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',

        'data/estate_property_type.csv',

        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_offer_views.xml',
        'views/res_users_views.xml',

        'views/estate_menus.xml',

        'report/estate_reports.xml',
        'report/estate_report_views.xml',
    ],
    'demo': [
        'demo/estate_property.xml'
    ],
    'application': True,
    'license': 'LGPL-3',
}