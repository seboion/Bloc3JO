from django.test import TestCase
from app.models import Evenement
from datetime import datetime, timedelta

class TestEvenementModel(TestCase):

    def setUp(self):
        self.evenement = Evenement.objects.create(
            nom="Test sur Evenement",
            date=datetime.now() + timedelta(days=10),
            stock_initial=100,
            description="Teste le modele Evenement"
        )

    def test_date_limite_reservation(self):
        # Test que la date limite de réservation est bien définie à un jour avant la date de l'évènement
        self.evenement.save()
        self.assertEqual(self.evenement.date_limite_reservation, self.evenement.date - timedelta(days=1))

    def test_stock_restant_initialization(self):
        #Test que le stock restant est bien initialisé à la création
        self.assertEqual(self.evenement.stock_restant, 100)
