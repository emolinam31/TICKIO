

from django.test import TestCase
from events.models import Event, TicketType
from decimal import Decimal

class TicketTypeModelTests(TestCase):
    def setUp(self):
        self.event = Event.objects.create(title='Evento Test', slug='evento-test')
        self.tt = TicketType.objects.create(
            event=self.event,
            name='VIP',
            price=Decimal('100.00'),
            capacity=10,
            sold=3,
            active=True
        )

    def test_remaining(self):
        self.assertEqual(self.tt.remaining, 7)

    def test_can_sell_true(self):
        self.assertTrue(self.tt.can_sell(2))

    def test_can_sell_false(self):
        self.assertFalse(self.tt.can_sell(8))
