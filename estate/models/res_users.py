from odoo import models, fields

class UsersInherited(models.Model):
    _inherit = "res.users"

    property_ids = fields.One2many("estate_property", "user_id")