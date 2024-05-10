from odoo import models,fields
from dateutil.relativedelta import relativedelta

class EstateProperty(models.Model):
    _name = "estate_property"
    _description = "Real estate property"

    name = fields.Char("Name", required=True)
    description = fields.Text("Description")
    active = fields.Boolean('Active', default=True)
    postcode = fields.Char("Postcode")
    date_availability = fields.Date(
        "Availability Date", 
        copy=False, 
        default=fields.Date.today() + relativedelta(months=3))
    expected_price = fields.Float("Expected Price", required=True)
    selling_price = fields.Float("Selling Price", readonly=True, copy=False)
    bedrooms = fields.Integer("Bedrooms", default=2)
    living_area = fields.Integer("Living Area")
    facades = fields.Integer("Facades")
    garage = fields.Boolean("Garage")
    garden = fields.Boolean("Garden")
    garden_area = fields.Integer("Garden Area")
    garden_orientation = fields.Selection(string = "Garden Orientation",
        selection=[("north", "North"),("south", "South"),("east", "East"),("west", "West")]
        )
    state = fields.Selection(string = "Status",
        selection=[("new", "New"), ("offer_received", "Offer Received"), ("offer_accepted", "Offer Accepted"), ("sold", "Sold"), ("cancelled", "Cancelled")],
        default="new",
        required=True,
        copy=False
        )
    user_id = fields.Many2one("res.users", string="Salesman", default=lambda self: self.env.user)
    partner_id = fields.Many2one("res.partner", string="Buyer")
    property_type_id = fields.Many2one("estate_property_type", string="Type")
    tag_ids = fields.Many2many("estate_property_tag", string="Tag(s)")
    offer_ids = fields.One2many("estate_property_offer", "property_id")