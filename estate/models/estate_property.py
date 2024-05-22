from odoo import api, models,fields
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare, float_is_zero
from dateutil.relativedelta import relativedelta

class EstateProperty(models.Model):
    _name = "estate_property"
    _description = "Real estate property"
    _order = "id desc"

    _sql_constraints = [
        (
            'check_expected_price', 'CHECK(expected_price > 0)',
            'The expected price needs to be strictly positive'
        ),
        (
            'check_selling_price', 'CHECK(selling_price >= 0)',
            'The selling price needs to be strictly positive'
        ),
    ]

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
    total_area = fields.Integer(compute="_compute_total_area")
    best_offer = fields.Float(compute="_compute_best_offer", default=0)

    @api.ondelete(at_uninstall=False)
    def _unlink_if_new_or_cancel(self):
        if any(estate_property.state not in ['new', 'cancelled'] for estate_property in self):
            raise UserError("You cannot delete property which is not in new or cancelled state")

    # -------------------------------------------------------------------------
    # COMPUTE METHODS
    # -------------------------------------------------------------------------

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area
    
    @api.depends('offer_ids.price')
    def _compute_best_offer(self):
        for record in self:
            if len(record.offer_ids) != 0:
                record.best_offer = max(record.offer_ids.mapped('price'))
            else:
                record.best_offer = 0

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = False

    @api.constrains("expected_price")
    def _check_expected_price(self):
        for record in self:
            # TODO
            #if record.selling_price != 0 and record.expected_price > (record.selling_price * 0.9):
            #    raise ValidationError("You cannot change the expected price to higher than 90 percent of the current selling price, try accepting a higher offer first")
            return True

    
    def action_property_sold(self):
        for record in self:
            if record.state == "cancelled":
                raise UserError("Cancelled properties cannot be sold")
            if not any(offer.status == 'accepted' for offer in record.offer_ids):
                raise UserError("Cannot sell a property without any accepted offers")
            record.state = "sold"
            return True
    
    def action_property_cancel(self):
        for record in self:
            if record.state == "sold":
                raise UserError("Sold properties cannot be cancelled")
            record.state = "cancelled"
            return True
