from odoo.tests import common


class TestComplaintsstage(common.TransactionCase):

    def _create_complaints_stage(self):
        """
        Create complaints stage
        """
        self.env['complaints.stage'].create({
            'name': 'name',
            'sequence': 10,
        })
