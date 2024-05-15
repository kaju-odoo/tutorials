from odoo import api, models, fields

class SaleBranch(models.Model):
    _name = "sale_branch"
    _description = "Sales branch"

    _sql_constraints = [('sale_branch_code_unique', 'unique(code)', "Branch code must be unique! as it is used as invoice sequence. Please choose another one.")]

    name = fields.Char(string="Name")
    active = fields.Boolean('Active', default=True)
    sequence_id = fields.Many2one("ir.sequence", string="Sequence")
    code = fields.Char(string="Code", size=3)

    @api.model
    def create(self, vals):
        branch = super(SaleBranch, self).create(vals)
        sequence = self.env['ir.sequence'].create({
            'name': 'Sales Order Branch-' + branch.name,
            'code': 'sale.order.' + branch.code.lower(),
            'padding': 5,
            'prefix': branch.code.upper()
        })
        branch.sequence_id = sequence.id
        return branch

