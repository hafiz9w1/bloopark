from odoo import fields, models


class ComplaintsStage(models.Model):
    _name = 'complaints.stage'
    _description = 'Complaints Stages'
    _rec_name = 'name'
    _order = 'sequence, id'

    name = fields.Char(
        'Stage Name',
        required=True,
        translate=True,
    )

    sequence = fields.Integer(
        'Sequence',
        default=1,
        help='Used to order stages. Lower is better.',
    )

    fold = fields.Boolean(
        'Folded in Kanban',
        help='This stage is folded in the kanban view when there are no records in that stage to display.',
    )
