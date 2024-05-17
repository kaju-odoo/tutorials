from odoo import api, models, Command

class EstateProperty(models.Model):
    _inherit = "estate_property"

    def action_property_sold(self):
        try:
            # This verifies whether the current user has access to the model itself.
            self.check_access_rights('write') 
            self.check_access_rule('write')
        except exceptions.AccessError as e:
            print("Access Denied:", e)
            return

        partner_id = self.partner_id.id
        move_type = 'out_invoice'
        
        # Find the journal_id for the accounting journal
        journal_id = self.env['account.journal'].search([('type', '=', 'sale')], limit=1).id
        
        # Create the values dictionary for the account.move
        move_values = {
            'partner_id': partner_id,
            'move_type': move_type,
            'journal_id': journal_id,
        }
        
        # Create an empty account.move
        new_invoice = self.env['account.move'].sudo().create(move_values)

        # Add invoice lines
        line_values = [
            Command.create({
                'name': 'Property Sale (6% of selling price)',
                'quantity': 1,
                'price_unit': self.selling_price * 0.06, 
            }),
            Command.create({
                'name': 'Administrative Fees',
                'quantity': 1,
                'price_unit': 100.00,
            })
        ]
        
        # Add the invoice lines to the account.move
        new_invoice.sudo().write({'invoice_line_ids': line_values})
        res = super(EstateProperty, self).action_property_sold()
        return res