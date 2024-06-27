from odoo.tests import common


class TestComplaintsMain(common.TransactionCase):

    def _create_complaints_main(self):
        """
        Create complaints main
        """
        dummy_complaints_type = self.env['complaints.type'].create([{
            'name': 'question',
            'description': 'description of question',
        }])
        crm_team_member_ids = self.env['crm.team.member'].search([])
        dummy_complaints_stage = self.env['complaints.stage'].create([{
            'name': 'New',
            'sequence': 10,
        }])
        self.env['complaints.main'].create({
            'name': 'name',
            'email': 'test@test.com',
            'flat_address': 'flat_address',
            'complaint_type_id': dummy_complaints_type.id,
            'description': 'description',
            'complaints_stage_id': dummy_complaints_stage.id,
            'assigned_user_id': crm_team_member_ids[0].user_id.id,
        })

    def test_complaints_sequence(self):
        """
        Test sequence complaint number
        """
        dummy_complaints_type = self.env['complaints.type'].create([{
            'name': 'question',
            'description': 'description of question',
        }])
        crm_team_member_ids = self.env['crm.team.member'].search([])
        dummy_complaints_stage = self.env['complaints.stage'].create([{
            'name': 'New',
            'sequence': 10,
        }])
        complaints_main = self.env['complaints.main'].create({
            'name': 'name',
            'email': 'test@test.com',
            'flat_address': 'flat_address',
            'complaint_type_id': dummy_complaints_type.id,
            'description': 'description',
            'complaints_stage_id': dummy_complaints_stage.id,
            'assigned_user_id': crm_team_member_ids[0].user_id.id,
        })
        self.env['ir.sequence'].search([
            ('code', '=', 'complaints.main'),
        ]).write({
            'use_date_range': True, 'prefix': 'COM/%(range_year)s/',
        })
        complaints_main = complaints_main.copy(
            {'complaints_date': '2019-01-01'})
        self.assertTrue(complaints_main.complaint_number.startswith(
            'COM/'))
        complaints_main = complaints_main.copy(
            {'complaints_date': '2020-01-01'})
        self.assertTrue(complaints_main.complaint_number.startswith(
            'COM/'))
        complaints_main = complaints_main.with_context(
            tz='Europe/Brussels').copy(
                {'complaints_date': '2019-12-31 23:30:00'})
        self.assertTrue(complaints_main.complaint_number.startswith('COM/'))

    def test_action_send_message(self):
        """
        Test action_send_message function
        """
        dummy_complaints_type = self.env['complaints.type'].create([{
            'name': 'question',
            'description': 'description of question',
        }])
        crm_team_member_ids = self.env['crm.team.member'].search([])
        dummy_complaints_stage = self.env['complaints.stage'].create([{
            'name': 'New',
            'sequence': 10,
        }])
        complaints_main = self.env['complaints.main'].create({
            'name': 'name',
            'email': 'test@test.com',
            'flat_address': 'flat_address',
            'complaint_type_id': dummy_complaints_type.id,
            'description': 'description',
            'complaints_stage_id': dummy_complaints_stage.id,
            'assigned_user_id': crm_team_member_ids[0].user_id.id,
        })
        email_act = complaints_main.action_send_message()
        email_ctx = email_act.get('context', {})
        complaints_main.with_context(
            **email_ctx).message_post_with_template(
                email_ctx.get('default_template_id'))
