import uuid #SEB : pour la génération des clés et token
from .models import TypeBillet, Evenement, Reservation, Billet, User, Profile #SEB : imports des models
from .forms import CustomUserCreationForm, UpdateUserForm, UpdateProfileForm, CustomAuthenticationForm, CustomPasswordChangeForm #SEB : import des class de .forms pour l'extension des données perso + les modifications des informations
from django.shortcuts import redirect, render, get_object_or_404 #SEB : get_object_or_404 permettra de lever une erreur 404 si un objet n'est pas trouvé ; redirect pour rediriger les utilisiateurs de vue en vues
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required #SEB : pour utiliser le décorateur @login_required
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from django.utils import timezone
from datetime import date, timedelta
from django.contrib import messages
from django.http import HttpResponse, HttpResponseForbidden
#SEB : pour recup le chemin des media pour la generation des qrcode
import os
from django.conf import settings
from django.http import HttpResponseForbidden
from django.contrib.auth import update_session_auth_hash #pour ne pas déconnecter l'user après changement de mot de passe
#SEB : pour la personnalisation de la vue de changement de mot de passe :
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import user_passes_test #pour la page de vérification des tickets, permet d'utiliser le décorateur django
from django.core.exceptions import ValidationError, ObjectDoesNotExist

# Create your views here.

class CustomLoginView(LoginView): #SEB : pour personnaliser la vue login de Django
    template_name = 'login.html'
    authentication_form = CustomAuthenticationForm 

    def form_invalid(self, form):
        # SEB : pour personaliser le message d'erreur
        for field in form.errors:
            if field != '__all__':
                form[field].field.widget.attrs['class'] = 'is-invalid'
        return super().form_invalid(form)

class CustomPasswordChangeView(PasswordChangeView): #SEB : pour personnaliser la vue de changement de mot de passe
    template_name = 'registration/password_change.html'  #template pour le changement de mot de passe
    success_url = reverse_lazy('password_change_done')  # redirige vers la page de confirmation

def home_view(request): #SEB : page d'accueil
    utilisateur = request.user if request.user.is_authenticated else None
    
    evenements_une = Evenement.objects.filter(date__gt=timezone.now(), a_la_une=True)  #SEB : récupères tous les événements filtré sur "à la une" et dont la date n'est pas dépassée
    return render(request, 'home.html', {'evenements_une': evenements_une , 'utilisateur': utilisateur})#, 'utilisateur' : utilisateur.first_name})

def billets_view(request): #SEB : présentation des offres d'achats de billets
    billets = TypeBillet.objects.all()  #SEB : récupères tous les types de billets
    return render(request, 'billets.html', {'billets': billets})

def evenements_view(request): #SEB : présentation des évèvements
    evenements = Evenement.objects.all()  #SEB : récupères tous les événements
    
    for evenement in evenements:

        evenement.reservation_possible = date.today() < evenement.date_limite_reservation.date()
    
    return render(request, 'evenements.html', {'evenements': evenements})

def inscription_view(request): #SEB : page de création de compte utilisateur
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirige vers la page de login après inscription
    else:
        form = CustomUserCreationForm()

    return render(request, 'inscription.html', {'form': form})

@login_required
def profil_view(request): #SEB : page d'affichage du profil de l'utilisateur
    utilisateur = request.user #SEB : Utilisateur connecté
    profil = Profile.objects.get(user=utilisateur) #SEB : Récupère le profil de l'utilisateur

    #SEB : Initialise les formulaires
    user_form = UpdateUserForm(instance=utilisateur)
    profile_form = UpdateProfileForm(instance=profil)
    password_change_form = CustomPasswordChangeForm(request.user)

    # Gérer la mise à jour des informations de l'utilisateur que si 'update_info' a été POST
    if 'update_info' in request.POST:
        user_form = UpdateUserForm(request.POST, instance=utilisateur)
        profile_form = UpdateProfileForm(request.POST, instance=profil)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Vos informations personnelles ont été mises à jour avec succès.")
        else:
            messages.error(request, "Il y a des erreurs dans les informations fournies.")

    # Gérer le changement de mot de passe
    elif 'change_password' in request.POST:
        password_change_form = CustomPasswordChangeForm(request.user, request.POST)
        
        if password_change_form.is_valid():
            user = password_change_form.save()
            update_session_auth_hash(request, user)  # Pour éviter de déconnecter l'utilisateur
            messages.success(request, "Votre mot de passe a été mis à jour avec succès.")
        else:
            messages.error(request, "Il y a eu une erreur dans la saisie du mot de passe. Veuillez vérifier les informations et réessayer.")

    # Compter le nombre de billets associés à l'utilisateur
    nombre_billets = Billet.objects.filter(utilisateur=utilisateur, est_valide=True).count()
    reservations = Reservation.objects.filter(utilisateur=utilisateur)

    for reservation in reservations:
        reservation.annulation_possible = date.today() < reservation.evenement.date_limite_reservation.date()

    return render(request, 'profil.html', {
        'utilisateur': utilisateur,
        'profil': profil,
        'user_form': user_form,
        'profile_form': profile_form,
        'password_change_form': password_change_form,
        'quantite_totale_billets': nombre_billets,
        'reservations': reservations,
    })

def password_change_done_view(request):
    return render(request, 'password_change_done.html')

@login_required
def achat_billet_view(request):
    types_billet = TypeBillet.objects.all()

    if request.method == 'POST':
        montant_total = 0
        nombre_billet = 0
        panier = []

        # SEB : Parcourir les types de billets pour stocker les billets sélectionnés
        for billet in types_billet:
            quantity = int(request.POST.get(f'quantities[{billet.id}]', 0))
            if quantity > 0:
                billet_total = float(billet.prix) * quantity #conversion en float car django utilise par defaut des decimal (non serialisable en JSON)
                montant_total += billet_total
                nombre_billet += billet.quantité_billet * quantity
                panier.append({
                    'type_billet_id': billet.id,
                    'billet_nom': billet.nom,
                    'billet_prix': float(billet.prix), 
                    'quantity': quantity,
                    'billet_total': billet_total,
                })

        # Si aucun billet n'a été sélectionné
        if montant_total == 0:
            messages.error(request, "Veuillez sélectionner au moins un billet.")
            return redirect('achat_billet')

        # Stocker les détails de l'achat dans la session (pour le récapitulatif et le paiement)
        request.session['panier'] = panier
        request.session['montant_total'] = float(montant_total)
        request.session['nombre_billet'] = nombre_billet

        return redirect('recap_achat')

    # Récupère tous les types de billets disponibles pour les afficher
    return render(request, 'achat_billet.html', {'types_billet': types_billet})

@login_required
def recap_achat_view(request):
    # Récupérer les informations du panier depuis la session
    panier = request.session.get('panier', [])
    montant_total = request.session.get('montant_total', 0)
    nombre_billet = request.session.get('nombre_billet', 0)

    # Généreration d'un token unique pour la transaction
    token_paiement = str(uuid.uuid4())
    request.session['token_paiement'] = token_paiement

    # Générer un token spécifique pour masquer l'URL
    token_url = uuid.uuid4().hex #la conversion .hex permet de supprimer les tirets pour ne pas les avoir dans l'url
    request.session['token_url'] = token_url

    # Si le panier est vide, rediriger vers la page d'achat
    if not panier:
        messages.error(request, "Votre panier est vide. Veuillez sélectionner des billets.")
        return redirect('achat_billet')
    
    # Calculer le nombre total de billets individuels
    total_billets = 0
    for item in panier:
        # Récupérer l'objet TypeBillet correspondant
        type_billet = TypeBillet.objects.get(id=item['type_billet_id'])
        total_billets += item['quantity'] * type_billet.quantité_billet
    
    return render(request, 'recap_achat.html', {
        'panier': panier,
        'montant_total': montant_total,
        'nombre_billet': nombre_billet,
        'total_billets': total_billets,
        'token_paiement': token_paiement,
        'token_url': token_url,
    })

@login_required
def mock_paiement_view(request, token_url):
    token_url_session = request.session.get('token_url') #recup le token_url de la session
    if token_url_session and token_url != token_url_session:
        return HttpResponseForbidden("Accès refusé. URL invalide ou expirée.")

    montant_total = request.session.get('montant_total', 0)
    token_paiement = request.session.get('token_paiement')

    # Si le montant total est zéro, rediriger vers l'achat
    if montant_total == 0:
        messages.error(request, "Le montant est nul. Veuillez sélectionner des billets.")
        return redirect('achat_billet')

    return render(request, 'mock_paiement.html', {
        'montant_total': montant_total,
        'token_paiement': token_paiement  # Passe le token au template

    
    })

@login_required
def confirmation_achat_view(request): #page de confirmation après achat via mock_paiement, génère les billets
    token_paiement = request.POST.get('token_paiement')
    token_session = request.session.get('token_paiement')

    # Vérifie que le token correspond à celui stocké dans la session
    if token_paiement != request.session.get('token_paiement'):
        messages.error(request, "Paiement non valide.")
        return redirect('achat_billet')

    # Si le token est valide, procéder à la création des billets :

    panier = request.session.get('panier', [])
    montant_total = request.session.get('montant_total', 0)

    # Génération des billets selon la quantité acheté
    utilisateur = request.user

    if panier:
        for item in panier:
            type_billet = TypeBillet.objects.get(id=item['type_billet_id'])

            quantity = item['quantity']  # Quantité d'offres achetées
            for _ in range(quantity):
                # Création des billets individuels pour chaque billet dans l'offre
                for _ in range(type_billet.quantité_billet):
                    Billet.objects.create(
                        utilisateur=utilisateur,
                        type_billet=type_billet,
                        est_valide=True,
                        security_key_billet=uuid.uuid4()  # Génère une clé unique pour chaque billet
                    )

    # Réinitialiser le panier après le paiement ainsi que le token
    request.session.pop('panier', None)
    request.session.pop('montant_total', None)
    request.session.pop('nombre_billet', None)
    request.session.pop('token_paiement', None)

    return render(request, 'confirmation_achat.html', {
        'montant_total': montant_total,
    })

@login_required
def reserver_evenement_view(request, evenement_id): #SEB : vérifie si l'utilisateur dispose bien d'un billet avant de reserver
    utilisateur = request.user #SEB : récupération de l'user
    evenement = get_object_or_404(Evenement, id=evenement_id) #SEB : Tente de récupérer l'évènement correspondant à evenement_id ; si n'existe pas ==> 404

    billets_utilisateur = Billet.objects.filter(utilisateur=utilisateur, est_valide=True) #SEB : requete sur le modèle Billet pour récupérer tous les billets de l'user connecté et qui ont la propriété Valide sur True
    
    if  not billets_utilisateur.exists(): #SEB : Si au moins 1 billet exist ==> True
        return render(request, 'besoin_billet.html') #SEB : redirige vers une page indiquant il est nécessaire d'avoir un billet

    if evenement.stock_restant > 0: #SEB : Vérifie que l'evenement solicité soit encore en stock

        # Créer la réservation
        Reservation.objects.create(utilisateur=utilisateur, billet=billets_utilisateur.first(), evenement=evenement)
        
        # Invalider le billet utilisé
        billet = billets_utilisateur.first()
        billet.est_valide = False
        billet.save()

        # Décrémenter le stock de l'événement
        evenement.stock_restant -= 1
        evenement.save()
        
        return redirect('confirmation_reservation') #SEB : renvoi vers une page de confirmation de resa
    else:
        return render(request, 'plus_de_stock.html')

@login_required
def confirmation_reservation_view(request): #Page de confirmation après utilisation d'un billet pour une reservaiton
    return render(request, 'confirmation_reservation.html')

@login_required
def annuler_reservation_view(request, token):

    reservation = get_object_or_404(Reservation, token = token, utilisateur=request.user)

    if request.method == 'POST':
        # le billet associé à la réservation
        billet = reservation.billet
        
        # l'événement associé à la réservation
        evenement = reservation.evenement
        

        # Supprimer la réservation
        reservation.delete()


        # Recréditer le billet à l'utilisateur de la reservation
        billet.utilisateur = request.user
        billet.est_valide = True
        billet.save()

        # Recréditer le stock de l'événement
        evenement.stock_restant += 1
        evenement.save()

        # Ajouter un message de confirmation
        messages.success(request, "Votre réservation a bien été annulée et le billet est de nouveau disponible.")

        # Rediriger vers la page profil
        return redirect('profil')

    return render(request, 'confirmation_annulation.html', {'reservation': reservation})

@login_required
def reservations_view(request):
    reservations = Reservation.objects.filter(utilisateur=request.user)  #SEB : Réservations de l'utilisateur connecté
    return render(request, 'reservations.html', {'reservations': reservations})

@login_required
def ticket_view(request, token):
    reservation = get_object_or_404(Reservation, token=token)

    if reservation.utilisateur != request.user:
        return HttpResponseForbidden("Vous n'êtes pas autorisé à accéder à cette page.")
    
    # Récupéreration des clé de sécurité
    security_key_user = reservation.utilisateur.profile.security_key
    security_key_billet = reservation.billet.security_key_billet

 

    context = {
        'reservation': reservation,
    }

    return render(request, 'ticket.html', context)

@user_passes_test(lambda u: u.is_superuser)  # SEB: Restriction à l'administrateur
def verification_billet_view(request):
    if request.method == 'POST':
        numero_ticket = request.POST.get('numero_ticket')
        if numero_ticket:  # Vérifie si numero_ticket n'est pas vide
            try:
                # Séparer la clé utilisateur et la clé billet à partir du séparateur "g" mis dans le template html (si besoin de le changer ne pas l'oublier dans le template)
                security_key_user, security_key_billet = numero_ticket.split('g')
                
                # Valide que chaque partie est un UUID valide
                uuid.UUID(security_key_user)
                uuid.UUID(security_key_billet)
                
                # Recherche le profil utilisateur par security_key :
                profile = Profile.objects.get(security_key=security_key_user)
                
                # Recherche le billet par security_key_billet :
                billet = Billet.objects.get(security_key_billet=security_key_billet, utilisateur=profile.user)

                # Recherche la reservation par l'utilisateur :
                reservation =  Reservation.objects.get(utilisateur=profile.user)

                # Chercher les info de l'evenement pour précision :
                evenement = Evenement.objects.get(nom=reservation.evenement)

                # Formatage des dates pour affichage des messages : 
                formatted_date_achat = billet.date_achat.strftime('%d/%m/%Y à %H:%M')
                formatted_date_evenement = evenement.date.strftime('%d/%m/%Y à %H:%M')
                
                # Si billet trouvé, afficher les messages serveur :
                message = (
                    f"Ticket valide ! <br>Ce ticket a été généré lors de la reservation effectué le {formatted_date_achat} avec un billet acheté avec une offre \" {billet.type_billet.nom} \" par l'utilisateur suivant (Nom, Prénom) : {profile.user.first_name}, {profile.user.last_name}. <br>" # la balise ne fonctionne que si |safe est ajouté dans le template
                    
                    f"<br>Il est affilié à la reservation de l'évenement \" {reservation.evenement} \" qui à lieu le {formatted_date_evenement}."
                )
                return render(request, 'verification_billet.html', {'message': message})
            
            except (Profile.DoesNotExist, Billet.DoesNotExist):
                message = "Ticket invalide. Veuillez vérifier le numéro."
            except (ValueError, ValidationError):
                message = "Numéro de ticket incorrect ou non valide."
            except (ObjectDoesNotExist): # Pour palier au problème de présentation d'un ticket qui a été annulé
                message = "Le ticket n'est plus valide. La reservation a été réalisée puis annulée"
        
        else:
            message = "Veuillez entrer un numéro de ticket."


        
        return render(request, 'verification_billet.html', {'message': message})
    
    return render(request, 'verification_billet.html')
