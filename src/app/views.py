from django.shortcuts import redirect, render, get_object_or_404 #SEB : get_object_or_404 permettra de lever une erreur 404 si un objet n'est pas trouvé ; redirect pour rediriger les utilisiateurs de vue en vues
from .models import TypeBillet, Evenement, Reservation, Billet, User, Profile #SEB : imports des models
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required #SEB : pour utiliser le décorateur @login_required
import uuid #SEB : pour la génération des clés

# Create your views here.

def billets_view(request):
    billets = TypeBillet.objects.all()  #SEB : récupères tous les types de billets
    return render(request, 'billets.html', {'billets': billets})

def evenements_view(request):
    evenements = Evenement.objects.all()  #SEB : récupères tous les événements
    return render(request, 'evenements.html', {'evenements': evenements})

def reservations_view(request):
    reservations = Reservation.objects.filter(utilisateur=request.user)  #SEB : Réservations de l'utilisateur connecté
    return render(request, 'reservations.html', {'reservations': reservations})

def profil_view(request):
    utilisateur = request.user  #SEB : Utilisateur connecté
    
    if not utilisateur.is_authenticated:
        return redirect('inscription')  # Redirige vers la page de login si non connecté

    return render(request, 'profil.html', {'utilisateur': utilisateur})

def home_view(request): #SEB : page d'accueil
    utilisateur = request.user  
    return render(request, 'home.html')

def inscription_view(request): #SEB : page d'inscription
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(
                user=user,
                adresse=request.POST.get('adresse'),
                telephone=request.POST.get('telephone')
            )
            return redirect('login')  # Redirige vers la page de login après inscription
    else:
        form = UserCreationForm()
        print("il y a un probleme avec les saisies")

    return render(request, 'inscription.html', {'form': form})


def reserver_evenement_view(request, evenement_id): #SEB : vérifie si l'utilisateur dispose bien d'un billet avant de reserver
    utilisateur = request.user #SEB : récupération de l'user
    evenement = get_object_or_404(Evenement, id=evenement_id) #SEB : Tente de récupérer l'évènement correspondant à evenement_id ; si n'existe pas ==> 404

    #SEB : Vérification de l'user :
    if not utilisateur.is_authenticated: #SEB : méthode is_authenticated de Django
        return redirect('login')  #SEB : Redirige vers la page de connexion si non authentifié (la vue login est celle de Django)
    

    #SEB : Vérifie si l'utilisateur possède au moins un billet
    billets_utilisateur = Billet.objects.filter(utilisateur=utilisateur, est_valide=True) #SEB : requete sur le modèle Billet pour récupérer tous les billets de l'user connecté et qui ont la propriété Valide sur True
    
    if  not billets_utilisateur.exists(): #SEB : Si au moins 1 billet exist ==> True
        return render(request, 'besoin_billet.html') #SEB : redirige vers une page indiquant il est nécessaire d'avoir un billet

    if evenement.stock_restant > 0: #SEB : Vérifie que l'evenement solicité soit encore en stock
        Reservation.objects.create(utilisateur=utilisateur, billet=billets_utilisateur.first(), evenement=evenement) #SEB : créé l'objet réservation
        evenement.stock_restant -= 1 #SEB : MAJ du stock
        evenement.save()
        
        return redirect('confirmation_reservation') #SEB : renvoi vers une page de confirmation de resa
    else:
        return render(request, 'plus_de_stock.html')
    

def confirmation_reservation_view(request): #Page de confirmation après utilisation d'un billet pour une reservaiton
    return render(request, 'confirmation_reservation.html')

@login_required #SEB : pour que la page ne soit pas accessible sans login
def achat_billet_view(request): #Page d'achat de billet après sélection

    if request.method == 'POST':
        type_billet_id = request.POST.get('type_billet')
        type_billet = get_object_or_404(TypeBillet, id=type_billet_id)
        
        # Création d'un billet pour l'utilisateur connecté
        billet = Billet.objects.create(
            utilisateur=request.user,
            type_billet=type_billet,
            #evenement=None,  # Aucun événement associé lors de l'achat ******************************************************************************* a suppr
            qr_code=str(uuid.uuid4()),  # Génère un code unique pour le billet
            est_valide=True
        )
        
        return redirect('confirmation_achat')  # Redirige vers une page de confirmation

    # Récupère tous les types de billets disponibles pour les afficher
    types_billet = TypeBillet.objects.all()
    return render(request, 'achat_billet.html', {'types_billet': types_billet})


def confirmation_achat_view(request):
    return render(request, 'confirmation_achat.html')

