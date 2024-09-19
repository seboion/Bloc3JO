from django.urls import path
from django.contrib.auth import views as auth_views #SEB : pour utiliser les login et logout de Django
from . import views #SEB : import de tout views

urlpatterns = [ #SEB : liaisons de chaques vues aux urls
    path('login/', auth_views.LoginView.as_view(), name='login'), #SEB : login et logout de Django
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('billets/', views.billets_view, name='billets'), 
    path('evenements/', views.evenements_view, name='evenements'),
    path('reservations/', views.reservations_view, name='reservations'),
    path('profil/', views.profil_view, name='profil'),
    path('', views.home_view, name='home'),
    path('inscription/', views.inscription_view, name='inscription'),
    path('reserver/<int:evenement_id>/', views.reserver_evenement_view, name='reserver_evenement'),
    path('confirmation/', views.confirmation_reservation_view, name='confirmation_reservation'),
    path('profil/', views.profil_view, name='profil'),
    path('achat_billet/', views.achat_billet_view, name='achat_billet'),
    path('confirmation-achat/', views.confirmation_achat_view, name='confirmation_achat'),
]
