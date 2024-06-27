from odoo import http
from odoo.http import request


class CreateProposal(http.Controller):

    @http.route('/complaints', type='http', auth='public', website=True)
    def get_complaint(self, **kw):
        """
        Present complaint type in website complaint API
        """
        complaint_type_obj = request.env['complaints.type'].sudo().search([])
        values = {
            'complaint_type_obj': complaint_type_obj,
        }
        return http.request.render(
            'bloopark_complaints.create_complaints',
            values,
        )

    @http.route(
        '/create/complaints',
        type='http',
        auth='public',
        website=True,
    )
    def create_complaint(self, **kw):
        """
        Create complaint from website and send email
        """
        crm_team_member_ids = request.env['crm.team.member'].sudo().search([])
        complaints_stage_ids = request.env[
            'complaints.stage'].sudo().search([]).filtered(
                lambda l: l.name == 'New')
        complaint = request.env['complaints.main'].sudo().create({
            'name': kw.get('name'),
            'email': kw.get('email'),
            'flat_address': kw.get('flat_address'),
            'complaint_type_id': kw.get('complaint_type_id'),
            'description': kw.get('description'),
            'complaints_stage_id': complaints_stage_ids.id,
            'assigned_user_id': crm_team_member_ids[0].user_id.id,
        })

        mail_template = complaint.env.ref(
            'bloopark_complaints.complaints_email_template')
        mail_template.send_mail(complaint.id, force_send=True)

        return request.render('bloopark_complaints.complaint_received', {})
