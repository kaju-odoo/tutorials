from odoo import api, models, fields

class EstatePropertyType(models.Model):
    _name = "estate_property_type"
    _description = "Real estate property type"
    _order = "name"

    _sql_constraints = [('property_tag_unique', 'unique(name)', "Property type must be unique! Please choose another one.")]

    name = fields.Char("Name", required=True)
    sequence = fields.Integer('Sequence', default=1, help="Used to order stages. Lower is better")
    property_ids = fields.One2many("estate_property","property_type_id")

    offer_ids = fields.One2many("estate_property_offer", "property_type_id", string="Offers")
    offer_count = fields.Integer("Number of Offers", compute="_compute_offer_count")

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)