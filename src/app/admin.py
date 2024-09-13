from django.contrib import admin
from .models import TypeBillet, Evenement, Billet, Reservation #SEB : import des models à gérer par l'administrateur (à créer aver python manage.py createsuperuser)

# Register your models here.

#SEB : ajout des models à gérer
admin.site.register(TypeBillet)
admin.site.register(Evenement)
admin.site.register(Billet)
admin.site.register(Reservation)
