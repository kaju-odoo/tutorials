{
    'name': 'Real Estate Account',
    'depends': [
        'estate',
        'account',
    ],
    "data": [
        'security/ir.model.access.csv',

        "report/estate_reports.xml",
        'report/custom_invoice_report.xml',
        
        "report/contact_reports.xml",
        'report/contact_report_views.xml',
    ],
    'application': True,
    'license': 'LGPL-3',
}