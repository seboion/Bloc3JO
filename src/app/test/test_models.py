from django.test import TestCase
from app.models import Evenement, TypeBillet, Profile, Billet, Reservation
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.utils import timezone 
import uuid



class TestEvenementModel(TestCase): #Test du modèle Evenement avec création d'un evenement comprenant un nom, une date un stock initial et une description

    def test_evenement_creation(self):
        nom="Test sur Evenement"
        date=datetime.now() + timedelta(days=10)
        stock_initial=100
        description="Teste le modele Evenement"

        evenement = Evenement.objects.create(
            nom=nom,
            date=date,
            stock_initial=stock_initial,
            description=description,
        )
        # Test que l'evenement est bien créé avec le bon nom et la bonne quantité de billets
        self.assertEqual(evenement.nom, nom)
        self.assertEqual(evenement.date, date)
        self.assertEqual(evenement.stock_initial, stock_initial)
        self.assertEqual(evenement.description, description)


        #test ici ce que la db renvoie vraiment
        evenementDB = Evenement.objects.get(nom=nom)
        self.assertEqual(evenementDB.nom, nom)
        self.assertEqual(evenementDB.date, date)
        self.assertEqual(evenementDB.stock_initial, stock_initial)
        self.assertEqual(evenementDB.description, description)

    def test_date_limite_reservation(self):
        nom="Test sur Evenement"
        date=datetime.now() + timedelta(days=10)
        stock_initial=100
        description="Teste le modele Evenement"

        evenement = Evenement.objects.create(
            nom=nom,
            date=date,
            stock_initial=stock_initial,
            description=description,
        )

        
        # Test que la date limite de réservation est bien définie à un jour avant la date de l'évènement
        self.assertEqual(evenement.date_limite_reservation, evenement.date - timedelta(days=1)) #assertEqual va comparer les valeurs de date limite calculés automatiquement par la vue, et la comparer avec la date du jour -1)

    def test_stock_restant_initialisation(self):
        nom="Test sur Evenement"
        date=datetime.now() + timedelta(days=10)
        stock_initial=100
        description="Teste le modele Evenement"

        evenement = Evenement.objects.create(
            nom=nom,
            date=date,
            stock_initial=stock_initial,
            description=description,
        )


        #Test que le stock restant est bien initialisé à la création
        self.assertEqual(evenement.stock_restant, stock_initial)

class TestTypeBilletModel(TestCase): #Test du modèle type de billet : création d'une offre SOLO avec prix et description

    def test_type_billet_creation(self):
        nom="SOLO"
        description="Un billet pour une seule personne"
        quantité_billet=1
        prix=100
        
        # Test que le type de billet est bien créé avec le bon nom et la bonne quantité de billets
        typebillet = TypeBillet.objects.create(
            nom=nom,
            description=description,
            quantité_billet=quantité_billet,
            prix=prix,
        )
        # Test ici que ce qu'on a envoyé est bien ce qui sera envoyé à la db
        self.assertEqual(typebillet.nom, nom)
        self.assertEqual(typebillet.quantité_billet, quantité_billet)
        self.assertEqual(typebillet.description, description)
        self.assertEqual(typebillet.prix, prix)

        #test ici ce que la db renvoie vraiment
        typebilletDB = TypeBillet.objects.get(nom=nom)
        self.assertEqual(typebilletDB.nom, nom)
        self.assertEqual(typebilletDB.description, description)
        self.assertEqual(typebilletDB.quantité_billet, quantité_billet)
        self.assertEqual(typebilletDB.prix, prix)


class TestProfileModel(TestCase): #Test de la création d'un user et son mot de passe non stocké en clair

    def setUp(self):
        self.username = "toto"
        self.password="testdunmotdepasse123!"
        self.first_name="prénom"
        self.last_name="nomdefamille"
        self.email="email.email.com"


        self.user = User.objects.create_user( #Ici on doit d'abbord définir les paramètres de gestion des Users de Django
            username = self.username,
            password=self.password,
            first_name=self.first_name,
            last_name=self.last_name,
            email=self.email,
        )


    
    def test_profile_creation(self): #le mot de passe doit être différent ici car non stocké en clair
        adresse = "1 rue de la Ville 75000 Paris"
        telephone = "0123456789"

        profiletested = Profile.objects.create(
            user=self.user,
        
            adresse = adresse,
            telephone = telephone,
        )


        self.assertEqual(profiletested.user.username, self.username)
        self.assertNotEqual(profiletested.user.password, self.password)
        self.assertEqual(profiletested.user.first_name, self.first_name)
        self.assertEqual(profiletested.user.last_name, self.last_name)
        self.assertEqual(profiletested.user.email, self.email)
        self.assertEqual(profiletested.adresse, adresse)
        self.assertEqual(profiletested.telephone, telephone)

class TestBilletModel(TestCase): #Test du modèle Billet (renseignement de donnée dans la bdd sans passer par le processus d'achat)
    
    def setUp(self):
        #création d'un user
        self.user = User.objects.create_user(
            username = "toto",
            password="testdunmotdepasse123!",
            first_name="prénom",
            last_name="nomdefamille",
            email="email.email.com",
        )

        self.Profile = Profile.objects.create(
            user = self.user,
            adresse = "1 rue de la Ville 75000 Paris",
            telephone = "0123456789",
        )
        #création d'un type de billet (offre)
        self.typebillet = TypeBillet.objects.create(
            nom="FAMILLE",
            description="4 billets",
            quantité_billet=4,
            prix=400,
        )

    def test_billet_creation(self):
        #création d'un billet
        billet = Billet.objects.create(
            utilisateur = self.user,
            type_billet = self.typebillet,

        )


        # Test ici que ce qu'on a envoyé est bien ce qui sera envoyé à la db
        self.assertEqual(billet.utilisateur, self.user)
        self.assertEqual(billet.type_billet, self.typebillet)
        self.assertEqual(billet.est_valide, True)
        #Vérification date d'achat
        now = timezone.now()
        self.assertAlmostEqual(billet.date_achat, now, delta=timedelta(seconds=1) )
        #Vérification qu'un uuid est générée
        self.assertIsInstance(billet.security_key_billet, uuid.UUID)

        #test ici ce que la db renvoie vraiment
        billetDB = Billet.objects.get(utilisateur=self.user)
        self.assertEqual(billetDB.utilisateur, self.user)
        self.assertEqual(billetDB.type_billet, self.typebillet)
        self.assertEqual(billetDB.est_valide, True)
        #Vérification date d'achat
        now = timezone.now()
        self.assertAlmostEqual(billetDB.date_achat, now, delta=timedelta(seconds=1) )
        #Vérification qu'un uuid est générée
        self.assertIsInstance(billetDB.security_key_billet, uuid.UUID)


class TestReservationModel(TestCase): #Test du modèle Billet (renseignement de donnée dans la bdd sans passer par le processus d'achat)
    
    def setUp(self):
        #création d'un user
        self.user = User.objects.create_user(
            username = "toto",
            password="testdunmotdepasse123!",
            first_name="prénom",
            last_name="nomdefamille",
            email="email.email.com",
        )

        self.Profile = Profile.objects.create(
            user = self.user,
            adresse = "1 rue de la Ville 75000 Paris",
            telephone = "0123456789",
        )
        #création d'un type de billet (offre)
        self.typebillet = TypeBillet.objects.create(
            nom="FAMILLE",
            description="4 billets",
            quantité_billet=4,
            prix=400,
        )

        #création d'un type evenement
        self.evenement = Evenement.objects.create(
            nom="Test sur Evenement",
            date=datetime.now() + timedelta(days=10),
            stock_initial=100,
            description="Teste le modele Evenement",
        )

        #création d'un billet (qui sera utilisé pour la reservation)
        self.billet = Billet.objects.create(
            utilisateur = self.user,
            type_billet = self.typebillet,

        )

    def test_reservation_creation(self):
        #création d'une reservation
        reservation = Reservation.objects.create(
            utilisateur = self.user,
            billet = self.billet,
            evenement = self.evenement,
        )

        # Test ici que ce qu'on a envoyé est bien ce qui sera envoyé à la db
        self.assertEqual(reservation.utilisateur, self.user)
        self.assertEqual(reservation.billet, self.billet)
        self.assertEqual(reservation.evenement, self.evenement)
        #Vérification date d'achat
        now = timezone.now()
        self.assertAlmostEqual(reservation.date_reservation, now, delta=timedelta(seconds=1) )
        #Vérification qu'un token est générée
        self.assertIsInstance(reservation.token, uuid.UUID)



        #test ici ce que la db renvoie vraiment
        reservationDB = Reservation.objects.get(utilisateur=self.user)
        self.assertEqual(reservationDB.utilisateur, self.user)
        self.assertEqual(reservationDB.billet, self.billet)
        self.assertEqual(reservationDB.evenement, self.evenement)
        #Vérification date d'achat
        now = timezone.now()
        self.assertAlmostEqual(reservationDB.date_reservation, now, delta=timedelta(seconds=1) )
        #Vérification qu'un token est générée
        self.assertIsInstance(reservationDB.token, uuid.UUID)

