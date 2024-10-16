from django.urls import path
from django.contrib.auth import views as auth_views #SEB : pour utiliser les login et logout de Django
from . import views #SEB : import de toutes les views
from .views import CustomLoginView, annuler_reservation_view, ticket_view, password_change_done_view
#SEB : pour utiliser les fichiers media :
from django.conf import settings
from django.conf.urls.static import static
from .views import CustomPasswordChangeView
from .views import achat_billet_view, recap_achat_view, mock_paiement_view, confirmation_achat_view

urlpatterns = [ #SEB : liaisons de chaques vues aux urls
    path('login/', CustomLoginView.as_view(), name='login'), #SEB : login et logout de Django
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
    path('recap_achat/', views.recap_achat_view, name='recap_achat'),
    path('mock_paiement/<str:token_url>/', views.mock_paiement_view, name='mock_paiement'),
    path('confirmation_achat/', views.confirmation_achat_view, name='confirmation_achat'),
    path('annuler_reservation/<uuid:token>/', annuler_reservation_view, name='annuler_reservation'),
    path('ticket/<uuid:token>/', ticket_view, name='ticket_view'),
    path('verification_billet/', views.verification_billet_view, name='verification_billet'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) #SEB : pour la gestion des images

