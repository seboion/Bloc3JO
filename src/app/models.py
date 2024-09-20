from django.db import models
from django.contrib.auth.models import User #SEB: Pour laisser à Django l'utilisation sécurisé des Users
import uuid #SEB : Pour la génération de clés

# Create your models here.
#SEB: les 5 modèles décrits ici servent à communiquer avec la BDD


#SEB : MODELE 0 : Profiles des utilisateurs : ajout de clé au modèle utilisateur de Django (il s'agit ici d'un modèle étendu)
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) #SEB: Utilisation du User de Django
    adresse = models.CharField(max_length=255) #SEB : Ajout d'autres champs non prévu dans User de Django
    telephone = models.CharField(max_length=20)
    security_key = models.UUIDField(default=uuid.uuid4, unique=True) #SEB : clé de sécurité

    def __str__(self):
        return f'{self.user.username} - Profile'


#SEB : MODELE 1 : Type de billet : Il s'agira des billets demandés : SOLO, DUO ou FAMILLE
class TypeBillet(models.Model):
    nom = models.CharField(max_length=20) #SEB: SOLO, DUO, FAMILLE
    description = models.TextField()
    quantité_billet = models.IntegerField(default=1) #SEB : 1 , 2, ou 4
    prix = models.DecimalField(max_digits=5, decimal_places=2) #SEB: en supossant un prix max de 999,99€ max_digits réglé sur 5

    def __str__(self):
        return self.nom
    

#SEB : MODELE 2 : Evèvements proposés et places restantes sur chaque évènement
class Evenement(models.Model):
    nom = models.CharField(max_length=100)
    date = models.DateTimeField()
    stock_initial = models.IntegerField()
    stock_restant = models.IntegerField()
    description = models.TextField()
    photo = models.ImageField(upload_to='evenements/', blank=True, null=True)

    def __str__(self):
        return self.nom


#SEB : MODELE 3 : Billets achetés, avec génération d'une deuxième clé et du qrcode
class Billet(models.Model):
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True) #SEB : associe un billet à un user (on_delete=models.CASCADE : pour supprimer le billet si l'user est supprimé)
    type_billet = models.ForeignKey(TypeBillet, on_delete=models.CASCADE)
    date_achat = models.DateTimeField(auto_now_add=True)  #SEB : Date d'achat générée automatiquement
    qr_code = models.CharField(max_length=255, unique=True)
    est_valide = models.BooleanField(default=True)
    security_key_billet = models.UUIDField(default=uuid.uuid4, unique=True)  # SEB : Clé dédiée au billet

    def __str__(self):
        return f'{self.type_billet.nom}'


#SEB : MODELE 4 : Réservation, rendu possible avec un billet et si l'évènement en question est toujours dispo (vérif à faire)
class Reservation(models.Model):
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    billet = models.ForeignKey(Billet, on_delete=models.CASCADE)
    evenement = models.ForeignKey(Evenement, on_delete=models.CASCADE)
    date_reservation = models.DateTimeField(auto_now_add=True)
    #total = models.DecimalField(max_digits=10, decimal_places=2) **************************************************************************

    def __str__(self):
        return f'Reservation pour {self.evenement.nom} - Billet ID: {self.billet.id}'


