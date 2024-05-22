from odoo import api, models, fields
from odoo.exceptions import ValidationError
from odoo.tools import float_compare, float_is_zero
from datetime import date, timedelta

class EstatePropertyOffer(models.Model):
    _name = "estate_property_offer"
    _description = "Real estate property offer"
    _order = "price desc"

    _sql_constraints = [
        (
            'check_offer_price', 'CHECK(price > 0)',
            'The price offer needs to be strictly positive'
        ),
    ]

    price = fields.Float("Price")
    status = fields.Selection(string="Status",
        selection = [("accepted", "Accepted"), ("refused", "Refused")],
        copy=False
    )
    partner_id = fields.Many2one("res.partner", string="Partner")
    property_id = fields.Many2one("estate_property", string="Property")
    validity = fields.Integer("Validity", default=7)
    date_deadline = fields.Date("Deadline",compute="_compute_deadline", inverse="_inverse_deadline")
    property_type_id = fields.Many2one("estate_property_type", related="property_id.property_type_id")
    
    @api.model
    def create(self, vals):
        property_id = self.env['estate_property'].browse(vals.get('property_id'))

        # Check if the offer price is lower than existing offers
        existing_offers = self.env['estate_property_offer'].search([('property_id', '=', vals.get('property_id'))])
        if existing_offers and any(vals.get('price') < offer.price for offer in existing_offers):
            raise ValidationError("The offer price cannot be lower than existing offers.")
    
        # Check if the property is sold
        if property_id.state == 'sold':
            raise ValidationError("Cannot create offer on sold property.")

        # Set property state to 'Offer Received'
        property_id.write({'state': 'offer_received'})

        return super(EstatePropertyOffer, self).create(vals)

    # -------------------------------------------------------------------------
    # COMPUTE METHODS
    # -------------------------------------------------------------------------

    @api.depends("validity")
    def _compute_deadline(self):
        for record in self:
            if record.create_date:
                if isinstance(record.create_date, date):
                    today_date = record.create_date.date()
                else:
                    today_date = date.today()
            else:
                today_date = date.today()
            record.date_deadline = today_date + timedelta(days=record.validity)
    
    def _inverse_deadline(self):
        for record in self:
            # if record.create_date:
            #     if isinstance(record.create_date, date):
            #         today_date = record.create_date.date()
            #     else:
            #         today_date = date.today()
            # else:
            #     today_date = date.today()
            validity = (record.date_deadline - record.create_date.date()).days
            record.validity = validity
    
    #@api.constrains("record.price")
    def action_confirm_offer(self):
        for record in self:
            # TODO
            if record.price  < (record.property_id.expected_price * 0.9):
                raise ValidationError("Offer should be at least 90 percent of the expected price.")

            property_offers = record.property_id.offer_ids.filtered(lambda offer: offer.id != record.id)
            property_offers.write({"status": "refused"})

            #record.property_id.write({"state": "sold"})
            record.property_id.write({
                "selling_price": record.price,
                "partner_id": record.partner_id,
                "state": "offer_accepted"
            })
            record.status = "accepted"
        return True
    
    def action_confirm_decline(self):
        for record in self:
            if record.status == "accepted":
                record.property_id.write({"selling_price": None})
                record.property_id.write({"partner_id": None})
            record.status = "refused"

        return True