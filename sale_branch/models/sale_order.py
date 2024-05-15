from odoo import api, models, fields

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    branch_id = fields.Many2one('sale_branch', string='Branch')

    def create(self, vals):
        if 'branch_id' in vals:
            branch = self.env['sale_branch'].browse(vals['branch_id'])
            if branch.sequence_id:
                vals['name'] = branch.sequence_id.next_by_id()
        return super(SaleOrder, self).create(vals)