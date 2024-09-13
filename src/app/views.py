from django.shortcuts import redirect, render
from .models import TypeBillet, Evenement, Reservation, Billet, User #SEB : imports des models

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

def home_view(request):
    utilisateur = request.user  #SEB : page d'accueil
    return render(request, 'home.html')

def inscription_view(request):
    utilisateur = request.user  #SEB : page d'inscription
    return render(request, 'inscription.html')
