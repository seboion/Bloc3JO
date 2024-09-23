import uuid #SEB : pour la génération des clés et token
import qrcode
from .models import TypeBillet, Evenement, Reservation, Billet, User, Profile #SEB : imports des models
from .forms import CustomUserCreationForm, UpdateUserForm, UpdateProfileForm, CustomAuthenticationForm #SEB : import des class de .forms pour l'extension des données perso + les modifications des informations
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

# Create your views here.

class CustomLoginView(LoginView): #SEB : pour personnaliser la vue login de Django
    template_name = 'login.html'
    authentication_form = CustomAuthenticationForm 

    def form_invalid(self, form):
        # SEB : pour personaliser le message d'erreur
        for field in form.errors:
            form[field].field.widget.attrs['class'] = 'is-invalid'
        return super().form_invalid(form)

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
    utilisateur = request.user  #SEB : Utilisateur connecté
    profil = Profile.objects.get(user=utilisateur) #SEB : Récupère le profil de l'utilisateur

    #SEB : MAJ des info personnelles :
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=utilisateur)
        profile_form = UpdateProfileForm(request.POST, instance=profil)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profil')

    else:
        user_form = UpdateUserForm(instance=utilisateur)
        profile_form = UpdateProfileForm(instance=profil)


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
        'quantite_totale_billets': nombre_billets,
        'reservations': reservations,
    })

@login_required #SEB : pour que la page ne soit pas accessible sans login
def achat_billet_view(request): #SEB : Plateforme d'achat des billets
    types_billet = TypeBillet.objects.all()
    utilisateur = request.user

    if request.method == 'POST':

        # SEB : Initialise les variables et les montants
        montant_total = 0 #SEB : prix
        nombre_billet = 0 #SEB : pour la conversion des offres achetés en bon nombre de ticket individuels
        panier = []

        # Parcourir les types de billets pour créer les billets en fonction des quantités choisies
        for billet in types_billet:
            quantity = int(request.POST.get(f'quantities[{billet.id}]', 0))
            montant_total += billet.prix * quantity
            nombre_billet += billet.quantité_billet * quantity

            for _ in range(quantity):
                for _ in range(billet.quantité_billet):
                    Billet.objects.create(
                        utilisateur=utilisateur,
                        type_billet=billet,
                        est_valide=True,
                        security_key_billet=uuid.uuid4()  # Génère une clé unique pour chaque billet
                )
        
        # Si aucun billet n'a été sélectionné, renvoyer un message d'erreur
        if montant_total == 0:
            messages.error(request, "Veuillez sélectionner au moins un billet.")
            return redirect('achat_billet')

# SEB : Rediriger vers une page de confirmation avec le montant total

        return redirect('confirmation_achat')

    # Récupère tous les types de billets disponibles pour les afficher
    return render(request, 'achat_billet.html', {'types_billet': types_billet})

def confirmation_achat_view(request): #SEB : confirmation après achat
    return render(request, 'confirmation_achat.html')

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

def confirmation_reservation_view(request): #Page de confirmation après utilisation d'un billet pour une reservaiton
    return render(request, 'confirmation_reservation.html')

def annuler_reservation_view(request, token):

    reservation = get_object_or_404(Reservation, token = token, utilisateur=request.user)

    if request.method == 'POST':
        # Récupérer le billet associé à la réservation
        billet = reservation.billet
        
        # Récupérer l'événement associé à la réservation
        evenement = reservation.evenement
        

        # Supprimer la réservation
        reservation.delete()

        # Recréditer le billet
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

def ticket_view(request, token):
    reservation = get_object_or_404(Reservation, token=token)

    if reservation.utilisateur != request.user:
        return HttpResponseForbidden("Vous n'êtes pas autorisé à accéder à cette page.")
    
    # Récupéreration des clé de sécurité
    security_key_user = reservation.utilisateur.profile.security_key
    security_key_billet = reservation.billet.security_key_billet

    # Généreration du QR code (concaténation du user security key et du security key du billet)
    qr_data = f"{security_key_user}-{security_key_billet}"
    qr_img = qrcode.make(qr_data)

    # Enregistrer l'image QR code dans un fichier ou utiliser une réponse HttpResponse SEB : avoir créé le dossier scr/media/tickets
    qr_img_relative_path = f'tickets/ticket_{reservation.token}.png'
    qr_img_full_path = os.path.join(settings.MEDIA_ROOT, qr_img_relative_path)
    qr_img.save(qr_img_full_path)
    

    context = {
        'reservation': reservation,
        'qr_img_path': os.path.join(settings.MEDIA_URL, qr_img_relative_path),
    }

    return render(request, 'ticket.html', context)