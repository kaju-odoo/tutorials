from odoo import models, fields

class EstatePropertyTag(models.Model):
    _name = "estate_property_tag"
    _description = "Real estate property tag"
    _order = "name"

    _sql_constraints = [('property_tag_unique', 'unique(name)', "Property tag must be unique! Please choose another one.")]

    name = fields.Char("Name", required=True)
    color = fields.Integer()