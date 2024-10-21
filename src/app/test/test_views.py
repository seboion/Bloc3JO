import uuid
from django.test import TestCase
from django.urls import reverse #pour obtenir l'url de la vue à partir de son nom
#Impors des formulaires Django et personalisés
from django.contrib.auth.forms import AuthenticationForm
from app.forms import CustomAuthenticationForm, CustomUserCreationForm
from django.contrib.auth.models import User
from django.utils import timezone
from app.models import Evenement, Profile, TypeBillet, Reservation, Billet
from datetime import date
from django.contrib import messages


class CustomLoginViewTests(TestCase): #Test la vue login

    def setUp(self): #création d'un user de test
        self.user = User.objects.create_user(username='testuser', password='Mo2Pas!!!!')
        
    def test_renders_login_template(self): #Test que la vue utilise bien le template login.html
        reponse = self.client.get(reverse('login'))
        self.assertTemplateUsed(reponse, 'login.html')

    def test_uses_custom_authentication_form(self): #Teste si la vue utilise bien le form custom
        response = self.client.get(reverse('login'))
        self.assertIsInstance(response.context['form'], CustomAuthenticationForm)

    def test_login_success_redirects(self): #test la redirection après un login OK

        # Effectue un login avec les bonnes informations
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'Mo2Pas!!!!'})
        
        # Vérifie que l'utilisateur est redirigé après un login réussi
        self.assertEqual(response.status_code, 302)  # Redirection
    
    def test_login_fail_redirects(self): #test la redirection après un login KO

        # Effectue un login avec les mauvaises informations
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'password'})
        
        # Vérifie que l'utilisateur n'est redirigé après un login échoué
        self.assertNotEqual(response.status_code, 302)  # Redirection

class HomeViewTest(TestCase): #Test la vue Home, ses affichages d'évenement "à la une" et son message perso pour utilisateurs

    def setUp(self):
        # Création d'un user test
        self.user = User.objects.create_user(username='testuser', password='mo2PaFort!')

        # Création d'événements pour tester le filtrage "à la une" : 1 event futur A la une (celui qui doit s'afficher) et 2 events qui ne devront pas s'afficher : un event pas "à la une" et un event "a la une" mais dont la date est expirée
        self.event_future_une = Evenement.objects.create(
            nom="Evenement Futur à la Une",
            date=timezone.now() + timezone.timedelta(days=10),
            a_la_une=True,
            description="Event futur à la une",
            stock_initial = 5
        )
        self.event_future_not_une = Evenement.objects.create(
            nom="Evenement Futur pas à la Une",
            date=timezone.now() + timezone.timedelta(days=10),
            a_la_une=False,
            description="Event futur pas à la une",
            stock_initial = 5
        )
        self.event_past_une = Evenement.objects.create(
            nom="Evenement passé à la Une",
            date=timezone.now() - timezone.timedelta(days=10),
            a_la_une=True,
            description="Evenement à la une mais passé",
            stock_initial = 5
        )

    def test_home_view_not_user(self): # Test avec un utilisateur non authentifié
        
        response = self.client.get(reverse('home'))

        self.assertEqual(response.status_code, 200)  # Vérifie que la page se charge bien
        self.assertTemplateUsed(response, 'home.html')  # Vérifie que le bon template est utilisé

        # Vérifie que le contexte contient bien les événements "à la une" futurs seulement
        evenements_une = response.context['evenements_une']
        self.assertIn(self.event_future_une, evenements_une)
        self.assertNotIn(self.event_future_not_une, evenements_une)
        self.assertNotIn(self.event_past_une, evenements_une)

        # Vérifie que l'utilisateur n'est pas authentifié
        self.assertIsNone(response.context['utilisateur'])

    def test_home_view_authenticated_user(self):
        # Test avec un utilisateur authentifié
        self.client.login(username='testuser', password='mo2PaFort!')
        response = self.client.get(reverse('home'))

        self.assertEqual(response.status_code, 200)  # Vérifie que la page se charge bien
        self.assertTemplateUsed(response, 'home.html')  # Vérifie que le bon template est utilisé

        # Vérifie que le contexte contient bien les événements "à la une" futurs
        evenements_une = response.context['evenements_une']
        self.assertIn(self.event_future_une, evenements_une)
        self.assertNotIn(self.event_future_not_une, evenements_une)
        self.assertNotIn(self.event_past_une, evenements_une)

        # Vérifie que l'utilisateur est bien authentifié
        self.assertEqual(response.context['utilisateur'], self.user)

class BilletsViewTest(TestCase): #Test la vue de présentation des offres
    
    def setUp(self):
        # Création d'offres pour les utiliser dans les tests
        self.type_billet_1 = TypeBillet.objects.create(nom='SOLO', description='1 billet', prix=50, quantité_billet = 1)
        self.type_billet_2 = TypeBillet.objects.create(nom='DUO', description='2 billets', prix=90, quantité_billet = 2)
       
    def test_billets_view_context_contains_type_billets(self):
        # Vérifie que les offres sont bien dans le contexte
        response = self.client.get(reverse('billets'))
        billets = response.context['billets']
        self.assertIn(self.type_billet_1, billets)
        self.assertIn(self.type_billet_2, billets)
        self.assertEqual(len(billets), 2)  # Vérifie que deux offres sont bien récupérés
    
    def test_billets_view_content(self):
        # Vérifie que les informations des billets sont bien dans le rendu
        response = self.client.get(reverse('billets'))
        self.assertContains(response, 'SOLO') 
        self.assertContains(response, 'DUO') 
        self.assertContains(response, '1 billet')
        self.assertContains(response, '2 billets')

class EvenementsViewTEST(TestCase): #Test de la vue de présentation des évenements

    def setUp(self):
        #création d'évènements pour la vue :
        self.event_future_une = Evenement.objects.create(
            nom="Evenement Futur à la Une",
            date=timezone.now() + timezone.timedelta(days=10),
            a_la_une=True,
            description="Event futur à la une",
            stock_initial = 5
        )
        self.event_future_not_une = Evenement.objects.create(
            nom="Evenement Futur pas à la Une",
            date=timezone.now() + timezone.timedelta(days=10),
            a_la_une=False,
            description="Event futur pas à la une",
            stock_initial = 5
        )
        self.event_past_une = Evenement.objects.create(
            nom="Evenement passé à la Une",
            date=timezone.now() - timezone.timedelta(days=10),
            a_la_une=True,
            description="Evenement à la une mais passé",
            stock_initial = 5
        )

    def Test_evenement_view(self):
        response = self.client.get(reverse('evenements'))
        # Vérifie que le contexte contient bien les événements tous les évènements créés
        evenements = response.context['evenements']
        self.assertIn(self.event_future_une, evenements)
        self.assertIn(self.event_future_not_une, evenements)
        self.assertIn(self.event_past_une, evenements)
    
    def Test_events_reservation_possible(self):
        #pour les évènements futurs 
        response = self.client.get(reverse('evenements'))
        evenements = response.context['evenements']
        for evenement in evenements:
            if evenement.date > timezone.now():
                self.assertTrue(evenement.reservation_possible)
            else:
                # Vérifie que pour les événements passés, la réservation est impossible
                self.assertFalse(evenement.reservation_possible)

    def test_evenements_content(self):
        # Vérifie que le contenu des événements est bien affiché sur la page
        response = self.client.get(reverse('evenements'))
        self.assertContains(response, "Evenement Futur à la Une")
        self.assertContains(response, "Evenement Futur pas à la Une")
        self.assertContains(response, "Evenement passé à la Une")

class InscriptionViewTest(TestCase): #Tests sur la page d'inscription

    def test_inscription_view_post_valide(self):

        # Test qu'un utilisateur est créé avec des données valides (POST)
        valid_data = {
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@test.com',
            'adresse': '123 Rue de la ville',
            'telephone': '0123456789',
            'password1': 'Mo2Pass1234!',
            'password2': 'Mo2Pass1234!',
        }
        response = self.client.post(reverse('inscription'), data=valid_data)
        
        # Vérifie que l'utilisateur est créé
        self.assertEqual(User.objects.count(), 1)
        user = User.objects.first()
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.first_name, 'Test')
        self.assertEqual(user.last_name, 'User')
        
        # Vérifie la redirection vers la page de login
        self.assertRedirects(response, reverse('login'))

    def test_inscription_view_post_invalide(self):
        # Test avec des données invalides
        invalid_data = {
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@test.com',
            'adresse': '123 Rue',
            'telephone': '0123456789',
            'password1': 'Pass1234!',
            'password2': 'Pass5678!',  # bug ici : pas de corresp
        }
        response = self.client.post(reverse('inscription'), data=invalid_data)
        
        # Vérifie que l'utilisateur n'est pas créé
        self.assertEqual(User.objects.count(), 0)
        
        # Vérifie que le formulaire est retourné avec des erreurs
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'inscription.html')
        self.assertIsInstance(response.context['form'], CustomUserCreationForm)
        self.assertTrue(response.context['form'].errors)

class AchatBilletViewTest(TestCase): #Tests vue achat billets
    
    def setUp(self):
        # Création des offres pour les tests
        self.billet_solo = TypeBillet.objects.create(nom="SOLO", prix=50, quantité_billet=1)
        self.billet_duo = TypeBillet.objects.create(nom="DUO", prix=90, quantité_billet=2)
        self.billet_famille = TypeBillet.objects.create(nom="FAMILLE", prix=160, quantité_billet=4)

        # Création d'un user pour passer une cde
        self.user = User.objects.create_user(username='testuser', password='SuperMo2pas!')

    
    def test_achat_billet_view_get(self):
        # Authentifier l'utilisateur
        self.client.login(username='testuser', password='SuperMo2pas!')


        # Test que la page d'achat de billets est accessible (avec GET)
        response = self.client.get(reverse('achat_billet'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'achat_billet.html')
        self.assertIn('types_billet', response.context)
        types_billet = response.context['types_billet']
        self.assertEqual(len(types_billet), 3)  # Vérifie que les 3 types de billets sont bien renvoyés
    
    def test_achat_billet_view_post_empty(self):
        # Authentifier l'utilisateur
        self.client.login(username='testuser', password='SuperMo2pas!')

        # Test avec un formulaire vide (aucun billet sélectionné)
        response = self.client.post(reverse('achat_billet'), data={})
        
        # Vérifie que l'utilisateur est redirigé vers la page d'achat avec un message d'erreur
        self.assertRedirects(response, reverse('achat_billet'))
        
        # Vérifie qu'un message d'erreur est bien affiché
        messages_list = list(response.wsgi_request._messages)
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].message, "Veuillez sélectionner au moins une offre.")
    
    def test_achat_billet_view_post_valid(self):
        # Authentifier l'utilisateur
        self.client.login(username='testuser', password='SuperMo2pas!')
        
        # Test avec un formulaire où des billets sont sélectionnés
        data = {
            'quantities[{}]'.format(self.billet_solo.id): 2,  # 2 billets SOLO
            'quantities[{}]'.format(self.billet_duo.id): 1,   # 1 billet DUO
        }
        response = self.client.post(reverse('achat_billet'), data=data)
        
        # Vérifie que l'utilisateur est redirigé vers la page de récapitulatif
        self.assertRedirects(response, reverse('recap_achat'))

        # Vérifie que les informations sont bien stockées dans la session
        session = self.client.session
        self.assertIn('panier', session)
        self.assertIn('montant_total', session)
        self.assertIn('nombre_billet', session)
        
        panier = session['panier']
        montant_total = session['montant_total']
        nombre_billet = session['nombre_billet']

        # Vérifie que le panier contient bien les informations correctes
        self.assertEqual(len(panier), 2)  # Il y a deux types de billets dans le panier
        self.assertEqual(panier[0]['quantity'], 2)  # 2 billets SOLO
        self.assertEqual(panier[1]['quantity'], 1)  # 1 billet DUO
        
        # Vérifie le montant total et le nombre de billets
        self.assertEqual(montant_total, 190)
        self.assertEqual(nombre_billet, 4)

    def test_achat_billet_view_no_quantity(self):
                # Authentifier l'utilisateur
        self.client.login(username='testuser', password='SuperMo2pas!')

        # Test si le formulaire ne contient aucune quantité (pas d'offres selectionnées)
        response = self.client.post(reverse('achat_billet'), data={})
        self.assertRedirects(response, reverse('achat_billet'))

        # Vérifie le msg d'erreur
        messages_list = list(response.wsgi_request._messages)
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].message, "Veuillez sélectionner au moins une offre.")
        
class ReserverEvenementViewTest(TestCase): #Test la vue des reservations

    def setUp(self):
        # Création d'un utilisateur pour faire les résa
        self.user = User.objects.create_user(username='testuser', password='SuperMo2pas!')

        # Création d'un événement
        self.evenement = Evenement.objects.create(
            nom="Événement Test",
            date=timezone.now() + timezone.timedelta(days=10),
            description="Description de l'événement test",
            stock_initial=5
        )

        # Création d'offres pour les utiliser dans les tests
        self.type_billet_1 = TypeBillet.objects.create(nom='SOLO', description='1 billet', prix=50, quantité_billet = 1)
        self.type_billet_2 = TypeBillet.objects.create(nom='DUO', description='2 billets', prix=90, quantité_billet = 2)


        # Création d'un billet valide pour l'utilisateur
        self.billet = Billet.objects.create(
            utilisateur=self.user,
            est_valide=True,
            type_billet = self.type_billet_1
        )

    def test_reserver_evenement_view_not_user(self):
        # Essaye d'accéder à la vue sans être connecté
        response = self.client.get(reverse('reserver_evenement', args=[self.evenement.id]))
        # Vérifie qu'il redirige vers la page de connexion
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('reserver_evenement', args=[self.evenement.id])}")

    def test_reserver_evenement_view_sans_billet(self):
        # Essaye d'accéder à la vue avec un utilisateur connecté sans billets valides
        self.client.login(username='testuser', password='SuperMo2pas!')
        Billet.objects.all().delete()  # Supprime le billet précédement créé dans le setup pour simuler un user sans billet
        response = self.client.get(reverse('reserver_evenement', args=[self.evenement.id]))
        # Vérifie que l'utilisateur est redirigé vers la page besoin_billet.html
        self.assertTemplateUsed(response, 'besoin_billet.html')

    def test_reserver_evenement_view_user_avec_billet_ok(self):
        # Connecte l'utilisateur
        self.client.login(username='testuser', password='SuperMo2pas!')
        # Essaye d'accéder à la vue avec un billet valide
        response = self.client.get(reverse('reserver_evenement', args=[self.evenement.id]))
        # Vérifie que la réservation est créée
        self.assertEqual(Reservation.objects.count(), 1)
        # Vérifie que le billet a été invalidé
        self.billet.refresh_from_db()
        self.assertFalse(self.billet.est_valide)
        # Vérifie que le stock de l'événement a été décrémenté
        self.evenement.refresh_from_db()
        self.assertEqual(self.evenement.stock_restant, 4)
        # Vérifie que l'utilisateur est redirigé vers la page de confirmation
        self.assertRedirects(response, reverse('confirmation_reservation'))

    def test_reserver_evenement_view_plus_de_stock(self):
        # Connecte l'utilisateur
        self.client.login(username='testuser', password='SuperMo2pas!')
        # Mise à 0 du stock de l'événement
        self.evenement.stock_restant = 0
        self.evenement.save()
        # Essaye d'accéder à la vue avec un billet valide
        response = self.client.get(reverse('reserver_evenement', args=[self.evenement.id]))
        # Vérifie que l'utilisateur est redirigé vers plus_de_stock.html
        self.assertTemplateUsed(response, 'plus_de_stock.html')

class AnnulerReservationViewTest(TestCase): #Test de l'annulation d'une résa

    def setUp(self):
        # Création d'un utilisateur pour faire les résa
        self.user = User.objects.create_user(username='testuser', password='SuperMo2pas!')

        # Crée un profil pour l'utilisateur sinon n'arrive pas à charger la page profil
        self.profile = Profile.objects.create(user=self.user, adresse='adresse', telephone='0123456789')

        # Création d'un événement
        self.evenement = Evenement.objects.create(
            nom="Événement Test",
            date=timezone.now() + timezone.timedelta(days=10),
            description="Description de l'événement test",
            stock_initial=5
        )

        # Création d'offres pour les utiliser dans les tests
        self.type_billet_1 = TypeBillet.objects.create(nom='SOLO', description='1 billet', prix=50, quantité_billet = 1)
        self.type_billet_2 = TypeBillet.objects.create(nom='DUO', description='2 billets', prix=90, quantité_billet = 2)


        # Création d'un billet valide pour l'utilisateur
        self.billet = Billet.objects.create(
            utilisateur=self.user,
            est_valide=True,
            type_billet = self.type_billet_1
        )
        # Création d'une réservation
        self.reservation = Reservation.objects.create(
            utilisateur=self.user,
            billet=self.billet,
            evenement=self.evenement,
        )

    def test_annuler_reservation_view_bad_token(self):
        # Connecte l'utilisateur
        self.client.login(username='testuser', password='SuperMo2pas!')
        # Essaye d'accéder à la vue avec un token invalide
        invalid_token = str(uuid.uuid4()) #token random pour simuler un mauvais token dans l'url
        response = self.client.post(reverse('annuler_reservation', args=[invalid_token]))
        # Vérifie qu'une erreur 404 est retournée
        self.assertEqual(response.status_code, 404)

    def test_annuler_reservation_view_valid_token(self):
        # Connecte l'utilisateur
        self.client.login(username='testuser', password='SuperMo2pas!')
        # Essaye d'annuler la réservation avec un token valide
        response = self.client.post(reverse('annuler_reservation', args=[self.reservation.token]))
        # Vérifie que la réservation est supprimée
        self.assertEqual(Reservation.objects.count(), 0)
        # Vérifie que le billet est recrédité
        self.billet.refresh_from_db()
        self.assertTrue(self.billet.est_valide)
        # Vérifie que le stock de l'événement a été incrémenté
        self.evenement.refresh_from_db()
        self.assertEqual(self.evenement.stock_restant, 6)
        # Vérifie que l'utilisateur est redirigé vers la page de profil
        self.assertRedirects(response, reverse('profil'))
        # Vérifie que le message de succès est affiché
        messages = list(response.wsgi_request._messages)
        self.assertEqual(str(messages[0]), "Votre réservation a bien été annulée et le billet est de nouveau disponible.")

    def test_annuler_reservation_view_get(self):
        # Connecte l'utilisateur
        self.client.login(username='testuser', password='SuperMo2pas!')
        # Essaye d'accéder à la vue avec un token valide en GET
        response = self.client.get(reverse('annuler_reservation', args=[self.reservation.token]))
        # Vérifie que la page de confirmation d'annulation est rendue
        self.assertTemplateUsed(response, 'confirmation_annulation.html')

class TicketViewTest(TestCase): #test l'affichage des tickets
    def setUp(self):
        # Création d'un utilisateur pour faire les résa
        self.user = User.objects.create_user(username='testuser', password='SuperMo2pas!')

        # Crée un profil pour l'utilisateur sinon n'arrive pas à charger la page profil
        self.profile = Profile.objects.create(user=self.user, adresse='adresse', telephone='0123456789')

        # Création d'un autre utilisateur pour faire les test
        self.user2 = User.objects.create_user(username='testuser2', password='SuperMo2pas!2')

        # Crée un profil pour l'autre utilisateur
        self.profile2 = Profile.objects.create(user=self.user2, adresse='adresse2', telephone='01234567892')


        # Création d'un événement
        self.evenement = Evenement.objects.create(
            nom="Événement Test",
            date=timezone.now() + timezone.timedelta(days=10),
            description="Description de l'événement test",
            stock_initial=5
        )

        # Création d'offres pour les utiliser dans les tests
        self.type_billet_1 = TypeBillet.objects.create(nom='SOLO', description='1 billet', prix=50, quantité_billet = 1)
        self.type_billet_2 = TypeBillet.objects.create(nom='DUO', description='2 billets', prix=90, quantité_billet = 2)


        # Création d'un billet valide pour l'utilisateur
        self.billet = Billet.objects.create(
            utilisateur=self.user,
            est_valide=True,
            type_billet = self.type_billet_1
        )
        # Création d'une réservation
        self.reservation = Reservation.objects.create(
            utilisateur=self.user,
            billet=self.billet,
            evenement=self.evenement,
        )

    def test_ticket_view_for_good_user(self):
        # Connecte l'utilisateur qui a bien une résa valide
        self.client.login(username='testuser', password='SuperMo2pas!')

        # Effectue la requête pour accéder au ticket
        response = self.client.get(reverse('ticket_view', args=[self.reservation.token]))


        # Vérifie que la réponse est un succès (200 OK)
        self.assertEqual(response.status_code, 200)

        # Vérifie que le bon template est utilisé
        self.assertTemplateUsed(response, 'ticket.html')

        # Vérifie que les informations de réservation sont dans le contexte
        self.assertIn('reservation', response.context)
        self.assertEqual(response.context['reservation'], self.reservation)

    def test_ticket_view_access_bad_user(self): #test d'acceder a un ticket en étant le mauvais user qui n'a pas de ticket
        # Connecte l'autre utilisateur
        self.client.login(username='testuser2', password='SuperMo2pas!2')

        # Effectue la requête pour accéder au ticket de la première réservation
        response = self.client.get(reverse('ticket_view', args=[self.reservation.token]))

        # Vérifie que l'accès est interdit
        self.assertEqual(response.status_code, 403)

    def test_ticket_view_with_invalid_token(self):
        # Connecte l'utilisateur
        self.client.login(username='testuser', password='SuperMo2pas!')

        # Effectue la requête avec un token invalide
        invalid_token = str(uuid.uuid4())
        response = self.client.get(reverse('ticket_view', args=[invalid_token]))

        # Vérifie que l'utilisateur est redirigé vers la page 404
        self.assertEqual(response.status_code, 404)

class VerificationBilletViewTest(TestCase): # TEst la page de verification des tickets (pour les admin)

    def setUp(self):
        # Créer un utilisateur administrateur
        self.superuser = User.objects.create_superuser(
            username='admin',
            password='admin_password',
            email='admin@admin.com'
        )
        self.profile = Profile.objects.create(
            user=self.superuser,
            security_key=str(uuid.uuid4())
            )

        # Création d'un utilisateur pour faire les résa
        self.user = User.objects.create_user(username='testuser', password='SuperMo2pas!')

        # Crée un profil pour l'utilisateur sinon n'arrive pas à charger la page profil
        self.profile = Profile.objects.create(user=self.user, adresse='adresse', telephone='0123456789')

        # Création d'un événement
        self.evenement = Evenement.objects.create(
            nom="Événement Test",
            date=timezone.now() + timezone.timedelta(days=10),
            description="Description de l'événement test",
            stock_initial=5
        )

        # Création d'offres pour les utiliser dans les tests
        self.type_billet_1 = TypeBillet.objects.create(nom='SOLO', description='1 billet', prix=50, quantité_billet = 1)
        self.type_billet_2 = TypeBillet.objects.create(nom='DUO', description='2 billets', prix=90, quantité_billet = 2)


        # Création d'un billet valide pour l'utilisateur
        self.billet = Billet.objects.create(
            utilisateur=self.user,
            est_valide=True,
            type_billet = self.type_billet_1
        )
        # Création d'une réservation
        self.reservation = Reservation.objects.create(
            utilisateur=self.user,
            billet=self.billet,
            evenement=self.evenement,
        )

    def test_access_verification_billet_view_admin(self):
        self.client.login(username='admin', password='admin_password')
        response = self.client.get(reverse('verification_billet'))
        self.assertEqual(response.status_code, 200)
    
    def test_access_verification_billet_view_non_admin(self):
        self.client.login(username='testuser', password='SuperMo2pas!')
        response = self.client.get(reverse('verification_billet'))
        self.assertNotEqual(response.status_code, 200)

    def test_verification_billet_valid_ticket(self):
        self.client.login(username='admin', password='admin_password')
        numero_ticket = f"{self.profile.security_key}g{self.billet.security_key_billet}" #ce qui est attendu

        response = self.client.post(reverse('verification_billet'), {'numero_ticket': numero_ticket})
        self.assertContains(response, "Ticket valide !")  # Vérifie que le message de ticket valide est présent dans le retour

    def test_verification_billet_invalid_ticket(self):
        self.client.login(username='admin', password='admin_password')
        numero_ticket = f"{self.profile.security_key}g{uuid.uuid4()}"  # Clé de billet ko

        response = self.client.post(reverse('verification_billet'), {'numero_ticket': numero_ticket})
        self.assertContains(response, "Ticket invalide. Veuillez vérifier le numéro.")  # Vérifie que le message d'erreur est présent

    def test_verification_billet_ticket_vide(self):
        self.client.login(username='admin', password='admin_password')
        response = self.client.post(reverse('verification_billet'), {'numero_ticket': ''})
        self.assertContains(response, "Veuillez entrer un numéro de ticket.")  # Vérifie que le message d'erreur est présent

    def test_verification_billet_with_invalid_format(self):
        self.client.login(username='admin', password='admin_password')
        numero_ticket = "invalid_format"  # Format invalide

        response = self.client.post(reverse('verification_billet'), {'numero_ticket': numero_ticket})
        self.assertContains(response, "Numéro de ticket incorrect ou non valide.")  # Vérifie que le message d'erreur est présent

class AchatBilletViewTest(TestCase): #test le processus d'achat jusqu'à la confirmation (vérication ajoutée ici : le mock et la confirmation)
    def setUp(self):
        # Création d'un utilisateur pour faire les réservations et connexion
        self.user = User.objects.create_user(username='testuser', password='SuperMo2pas!')
        self.client.login(username='testuser', password='SuperMo2pas!')

        # Création d'un type de billet pour les tests
        self.type_billet = TypeBillet.objects.create(nom='SOLO', description='1 billet', prix=50, quantité_billet=1)

    def test_achat_billet_view_post(self):
        response = self.client.post(reverse('achat_billet'), {
            f'quantities[{self.type_billet.id}]': 1,  # Sélectionne ici 1 billet via l'offre précédement créee
        })
        
        self.assertEqual(response.status_code, 302)  # Vérifie redirection vers recap_achat
        self.assertEqual(self.client.session['montant_total'], 50)  # Vérifie le montant total
        self.assertEqual(self.client.session['nombre_billet'], 1)  # Vérifie le nombre de billets
        self.assertTrue('panier' in self.client.session)  # Vérifie que le panier est rempli

    def test_recap_achat_view(self): #passage au recap

        self.client.post(reverse('achat_billet'), {
            f'quantities[{self.type_billet.id}]': 1,
        })

        response = self.client.get(reverse('recap_achat'))
        self.assertEqual(response.status_code, 200)  # Vérifie que la page est accessible
        self.assertContains(response, 'SOLO')  # Vérifie que le type de billet est présent
        self.assertContains(response, '50')  # Vérifie que le prix est affiché

    def test_mock_paiement_view(self): #passage au mock :
        self.client.post(reverse('achat_billet'), {
            f'quantities[{self.type_billet.id}]': 1,
        })

        # recap_achat pour générer le token_url
        self.client.get(reverse('recap_achat'))

        response = self.client.get(reverse('mock_paiement', args=[self.client.session['token_url']]))
        self.assertEqual(response.status_code, 200)  # Vérifie que la page est accessible
        self.assertContains(response, '50')  # Vérifie que le montant est affiché

    def test_confirmation_achat_view(self): #test ici la confirmation, si toute la session a bien suivie
        self.client.post(reverse('achat_billet'), {
            f'quantities[{self.type_billet.id}]': 1,
        })

        # Appeler la vue recap_achat pour générer le token de paiement
        self.client.get(reverse('recap_achat'))

        # Appeler la vue mock_paiement pour passer au paiement
        response = self.client.post(reverse('mock_paiement', args=[self.client.session['token_url']]))
        self.assertEqual(response.status_code, 200)  # Vérifie que la page est accessible

        # Appeler la vue de confirmation d'achat
        response = self.client.post(reverse('confirmation_achat'), {
            'token_paiement': self.client.session['token_paiement'],  # token de paiement
        })
        
        self.assertEqual(response.status_code, 200)  # Vérifie que la page est accessible
        self.assertContains(response, '50')  # Vérifie que le montant est affiché
        
        # Vérifiez que les billets ont été créés
        billets = Billet.objects.filter(utilisateur=self.user)
        self.assertEqual(billets.count(), 1)  # Vérifie qu'un billet a été créé
        self.assertTrue(billets[0].est_valide)  # Vérifie que le billet est valide

        # Vérifiez que la session a été réinitialisée
        self.assertNotIn('panier', self.client.session)
        self.assertNotIn('montant_total', self.client.session)
        self.assertNotIn('nombre_billet', self.client.session)
        self.assertNotIn('token_paiement', self.client.session)
