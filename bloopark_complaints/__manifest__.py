{
    'name': 'Complaints',
    'version': '16.0.0.0.1',
    'author': 'Hafiz Abbas',
    'email': 'hafizabbas9w1@gmail.com',
    'sequence': 2,
    'category': 'Technical',
    'Summary': 'Realestate X Website Complaints',
    'description': """
        Website complaint system for a real estate company
    """,
    'depends': [
        'crm',
        'website',
    ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',

        'report/ir_actions_report_templates.xml',
        'report/ir_actions_report.xml',

        'data/ir_sequence_data.xml',
        'data/complaints_stage_data.xml',
        'data/complaints_mail_template_data.xml',

        'views/complaints_main_view.xml',
        'views/complaints_type_view.xml',
        'views/complaints_stage_view.xml',
        'views/complaints_menu_view.xml',

        'static/src/xml/website_complaints.xml',
    ],
    'qweb': [
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
