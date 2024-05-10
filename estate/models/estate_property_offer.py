from odoo import models, fields

class EstatePropertyOffer(models.Model):
    _name = "estate_property_offer"
    _description = "Real estate property offer"

    price = fields.Float("Price")
    status = fields.Selection(string="Status",
        selection = [("accepted", "Accepted"), ("refused", "Refused")],
        copy=False
    )
    partner_id = fields.Many2one("res.partner", string="Partner")
    property_id = fields.Many2one("estate_property", string="Property")