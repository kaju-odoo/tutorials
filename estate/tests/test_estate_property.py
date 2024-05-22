from odoo.tests.common import TransactionCase, Form
from odoo.exceptions import UserError, ValidationError

class TestEstateProperty(TransactionCase):

    def setUp(self):
        super(TestEstateProperty, self).setUp()
        self.property_model = self.env['estate_property']
        self.offer_model = self.env['estate_property_offer']

        self.property = self.property_model.create({
            'name': 'Test Property',
            'expected_price': 100000,
            'living_area': 100,
            'garden_area': 20,
        })

        self.property_sold = self.property_model.create({
            'name': 'Sold Property',
            'expected_price': 200000,
            'living_area': 200,
            'garden_area': 40,
            'state': 'sold',
        })

    def test_create_offer_for_sold_property(self):
        with self.assertRaises(UserError):
            self.offer_model.create({
                'property_id': self.property_sold.id,
                'price': 199000,
            })

    def test_sell_property_with_no_accepted_offers(self):
        with self.assertRaises(UserError):
            self.property.action_property_sold()

    def test_sell_property_with_accepted_offer(self):
        offer = self.offer_model.create({
            'property_id': self.property.id,
            'price': 95000,
        })
        offer.status = 'accepted'
        self.property.action_property_sold()
        self.assertEqual(self.property.state, 'sold')

    def test_garden_onchange(self):
        with Form(self.property) as f:
            f.garden = True
            f.save()
            self.assertEqual(f.garden_area, 10)
            self.assertEqual(f.garden_orientation, 'north')

        with Form(self.property) as f:
            f.garden = False
            f.save()
        self.assertEqual(self.property.garden_area, 0)
        self.assertEqual(self.property.garden_orientation, False)
