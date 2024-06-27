from odoo import _, api, fields, models
from datetime import datetime


class ComplaintsMain(models.Model):
    _name = 'complaints.main'
    _description = 'Complaints'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    complaint_number = fields.Char(
        string='Complaint Number',
        required=True,
        help='Complaint Number.',
        copy=False,
        readonly=False,
        index='trigram',
        default=lambda self: _('New'),
    )

    name = fields.Char(
        string='Name',
        tracking=True,
        required=True,
        help='Complainant Name.',
    )

    email = fields.Char(
        string='Email',
        tracking=True,
        required=True,
        help='Complainant Email.',
    )

    flat_address = fields.Char(
        string='Flat Address',
        tracking=True,
        required=True,
        help='Complaint Flat Address.',
    )

    complaint_type_id = fields.Many2one(
        'complaints.type',
        string='Complaint Type',
        required=True,
        tracking=True,
        help='Complaint Type.',
    )

    user_id = fields.Many2one(
        'res.users',
        string='User',
        default=lambda self: self.env.user,
        readonly=True,
        tracking=True,
        help='User creating this record.',
    )

    assigned_user_id = fields.Many2one(
        'crm.team.member',
        string='Assigned User',
        tracking=True,
        help='Complaint Assigned User.',
    )

    complaints_date = fields.Datetime(
        string='Complaint Date',
        default=lambda self: datetime.now(),
        tracking=True,
        help='Complaint Creation Date.',
    )

    description = fields.Text(
        string='Complaint Details...',
        help='Complaint Description.',
    )

    action_plan = fields.Text(
        string='Action Plan...',
        help='Complaint Action Plan.',
    )

    complaints_stage_id = fields.Many2one(
        'complaints.stage',
        string='Stage',
        index=True,
        tracking=True,
        group_expand='_read_group_stage_ids',
        readonly=False,
        store=True,
        copy=False,
        help='Complaint Stages.',
    )

    complaints_stage_name = fields.Char(
        related='complaints_stage_id.name',
        string='Stage Name',
    )

    color = fields.Integer('Color Index', default=0)

    active = fields.Boolean('Active', default=True)

    @api.model_create_multi
    def create(self, vals_list):
        """
        Auto set complaint number on creation
        """
        for vals in vals_list:
            if vals.get('complaint_number', _('New')) == _('New'):
                seq_date = fields.Datetime.context_timestamp(
                    self, fields.Datetime.to_datetime(vals['created_date']),
                ) if 'created_date' in vals else None
                vals['complaint_number'] = self.env[
                    'ir.sequence'].next_by_code(
                        'complaints.main', sequence_date=seq_date) or _('New')

        return super().create(vals_list)

    @api.model
    def _read_group_stage_ids(self, stages, domain, order):
        """
        Return complaints stages for complaints_stage_id
        """
        return self.env['complaints.stage'].search([], order=order)

    def action_send_message(self):
        """
        Send message to complainant
        """
        mail_template = self.env.ref(
            'bloopark_complaints.complaint_response_email_template')
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(False, 'form')],
            'view_id': False,
            'target': 'new',
            'context': {
                'partner_ids': self.assigned_user_id.user_id.partner_id,
                'default_template_id': mail_template.id,
            },
        }

    def action_close(self):
        """
        Close complaint and send mail to complainant
        """
        complaints_stage_obj = self.env['complaints.stage'].search([])
        self.complaints_stage_id = complaints_stage_obj.filtered(
            lambda l: l.name == 'Dropped')
        mail_template = self.env.ref(
            'bloopark_complaints.complaint_closed_email_template')
        mail_template.send_mail(self.id, force_send=True)

    def action_resolve(self):
        """
        Resolve complaint and send mail to complainant
        """
        complaints_stage_obj = self.env['complaints.stage'].search([])
        self.complaints_stage_id = complaints_stage_obj.filtered(
            lambda l: l.name == 'Solved')
        mail_template = self.env.ref(
            'bloopark_complaints.complaint_solved_email_template')
        mail_template.send_mail(self.id, force_send=True)

    def action_print_work_order(self):
        """
        Print Work Order
        """
        return self.env.ref(
            'bloopark_complaints.action_report_complaintsmain',
        ).report_action(self)
