from odoo import fields, models


class ComplaintsType(models.Model):
    _name = 'complaints.type'
    _description = 'Complaints Type'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(
        string='Name',
        tracking=True,
        required=True,
    )

    description = fields.Text(string='Complaint Details...')

    active = fields.Boolean('Active', default=True)
