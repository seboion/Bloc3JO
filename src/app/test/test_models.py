from django.test import TestCase
from app.models import Evenement, TypeBillet, Profile
from datetime import datetime, timedelta
from django.contrib.auth.models import User 

class TestEvenementModel(TestCase): #Test du modèle Evenement avec création d'un evenement comprenant un nom, une date un stock initial et une description

    def setUp(self):
        self.evenement = Evenement.objects.create(
            nom="Test sur Evenement",
            date=datetime.now() + timedelta(days=10),
            stock_initial=100,
            description="Teste le modele Evenement"
        )

    def test_date_limite_reservation(self):
        # Test que la date limite de réservation est bien définie à un jour avant la date de l'évènement
        self.evenement.save() #Sauvegarde l'instance evenement dans la bdd (important pour tester certaines logiques) 
        self.assertEqual(self.evenement.date_limite_reservation, self.evenement.date - timedelta(days=1)) #assertEqual va comparer les valeurs de date limite calculés automatiquement par la vue, et la comparer avec la date du jour -1)

    def test_stock_restant_initialisation(self):
        #Test que le stock restant est bien initialisé à la création
        self.assertEqual(self.evenement.stock_restant, 100)

class TestTypeBilletModel(TestCase): #Test du modèle type de billet : création d'une offre SOLO avec prix et description
    
    def setUp(self):
        self.typebillet = TypeBillet.objects.create(
            nom="SOLO",
            description="Un billet pour une seule personne",
            quantité_billet=1,
            prix=100
        )
    
    def test_type_billet_creation(self):
        # Test que le type de billet est bien créé avec le bon nom et la bonne quantité de billets
        self.assertEqual(self.typebillet.nom, "SOLO")
        self.assertEqual(self.typebillet.quantité_billet, 1)

class TestProfileModel(TestCase): #Test de la création d'un user et son mot de passe non stocké en clair

    def setUp(self):
        self.user = User.objects.create_user( #Ici on doit d'abbord définir les paramètres de gestion des Users de Django
            username = "toto",
            password="testdunmotdepasse123!",
            first_name="prénom",
            last_name="nomdefamille",
            email="email.email.com",
        )

        self.Profile = Profile.objects.create(
            user=self.user,
        
            adresse = "1 rue de la Ville 75000 Paris",
            telephone = "0123456789",
        )
    
    def test_profile_creation(self): #le mot de passe doit être différent ici car non stocké en clair
        self.assertEqual(self.Profile.user.username, "toto")
        self.assertNotEqual(self.Profile.user.password, "testdunmotdepasse123!")
        self.assertEqual(self.Profile.user.first_name, "prénom")
        self.assertEqual(self.Profile.user.last_name, "nomdefamille")
        self.assertEqual(self.Profile.user.email, "email.email.com")
        self.assertEqual(self.Profile.adresse, "1 rue de la Ville 75000 Paris")
        self.assertEqual(self.Profile.telephone, "0123456789")


