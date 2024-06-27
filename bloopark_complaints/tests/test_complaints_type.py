from odoo.tests import common


class TestComplaintstype(common.TransactionCase):

    def _create_complaints_type(self):
        """
        Create complaints type
        """
        self.env['complaints.type'].create({
            'name': 'name',
            'description': 'description',
        })
