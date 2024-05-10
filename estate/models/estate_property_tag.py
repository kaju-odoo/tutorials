from odoo import models, fields

class EstatePropertyTag(models.Model):
    _name = "estate_property_tag"
    _description = "Real estate property tag"

    name = fields.Char("Name", required=True)