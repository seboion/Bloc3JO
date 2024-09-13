from django.urls import path
from . import views #SEB : import de tout views

urlpatterns = [
    path('billets/', views.billets_view, name='billets'), #SEB : liaisons de chaques vues aux urls
    path('evenements/', views.evenements_view, name='evenements'),
    path('reservations/', views.reservations_view, name='reservations'),
    path('profil/', views.profil_view, name='profil'),
    path('', views.home_view, name='home'),
    path('inscription/', views.inscription_view, name='inscription'),
]
