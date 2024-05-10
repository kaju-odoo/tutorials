from odoo import models, fields

class EstatePropertyType(models.Model):
    _name = "estate_property_type"
    _description = "Real estate property type"

    name = fields.Char("Name", required=True)