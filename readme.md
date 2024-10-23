# Fonctionnement du projet "Bloc3" : Application de réservation de tickets pour les évènements des JO 2024

##    1. Utilisation du code source de l’application via le dépôt git :

###        a. Restauration de toutes les dépendances du projet :
Utiliser le fichier requirements.txt avec la commande :
```bash 
pip install -r requirements.txt
```
Pour toute mise à jour des dépendances, utiliser la commande suivante à la racine du projet :
```bash
pip freeze -> requirements.txt
```
###        b. Le projet nécessite la mise à disposition d'une base de données PostgreSQL(PostgreSQL doit donc être installé au préalable sur le système) :
Les données devront être stockées dans le fichier .env situé à la racine du projet sous ce format :
```makefile
DB_NAME=##nom de votre base de donnée##
DB_USER=##utilisateur de votre base de donnée##
DB_PASSWORD=##mot de passe choisi##
DB_HOST=##adresse , localhost si projet utilisé en local##
DB_PORT=## port utilisé, 5432 par défaut si utilisé en local##
```
Commandes pour la création de la base de données (les données sont ici des exemples) :

Pour avoir accéder à PostgreSQL en tant que super utilisateur :
```bash
sudo -i -u postgres 
```
Accès à l'interface PostgreSQL :
```bash
psql
```
Création de l'utilisateur « joamdin » :
```sql
CREATE USER joadmin WITH PASSWORD "********"; 
```
Création de la base de données « jobdd » :
```sql
CREATE DATABASE jobdd OWNER "*user"; 
```
Quitter l'interface exit # Revenir à l'utilisateur normal :
```bash
\q 
```
Si nécessaire, les informations relatives à la base de données sont reprises dans le fichier settings.py du projet Django (src/admin_jo/settings.py) dans la variable (dict) DATABASE (elles pointent vers le fichier .env)

###        c. Création du compte administrateur du site (permettant de visualiser et modifier les types de billets mise en vente et les évènements) :
Avec les commandes suivantes (dans le dossier source du projet) :
```bash
python manage.py createsuperuser
```

###        d. Renseigner la Secret_key Django dans le fichier .env :

Si besoin de réinitialiser la Secret Key du projet taper la commande suivante : 
```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```
La renseigner ensuite dans le fichier .env sous ce format :
```makefile
SECRET_KEY = ‘#secret_key#’
```
Le projet ne contenant plus la clé, il est nécessaire de la réinitialiser avant utilisation.
Pour la version déployée, la clé a été également réinitialisé.

###        e. En utilisation local, dans le fichiers settings.py, DEBUG peut être mis sur TRUE, la version déployée doit elle impérativement être réglée sur FALSE.

###        f. Réaliser les migrations avec les commandes suivantes (toujours dans le dossier source du projet) :
```bash
python manage.py makemigrations
python manage.py migrate
```
Cela permet d’initialiser la base de données pour le projet Django

###        g. Lancer le serveur local Django pour accéder au projet via le navigateur internet :
```bash
python manage.py runserver
```
Puis ouvrir le lien local fourni dans le terminal suite à cette commande 
(CTRL+C pour fermer le serveur local)

Cette étape ne peut être réalisée que si les précédentes ont été préalablement réalisées.

##    2. Utilisation de l’application via le navigateur internet, en local ou une fois déployée (l’ordre des étapes suivantes est important pour l’utilisation normale de l’application) :

###        a. Accès à l’administration du site :
Une fois sur le site internet, se rendre sur /admin du site pour accéder à l'interface administrateur. Utiliser les identifiants fournis pour la version déployée, ou les identifiants créés en partie 1) c) pour la version locale.

###        b. Création d’offre de billet (indispensable pour l’achat de billet pour l’utilisateur) :
Depuis l’interface administrateur : commencer par créer les types d'offres (Solo, Duo, Famille) en cliquant sur la section Type billet.
Donnez un nom, une description de l’offre, un prix ainsi que la quantité de billet correspondant à l’offre. Chaque billet ainsi émis après achat permettra à l’utilisateur d’effectuer une réservation.

###        c. Création d’évènements des JO (indispensable pour la réalisation de réservation) :
Depuis l’interface administrateur et la section Evenement créer un nouvel évènement en saisissant son nom, une date et une heure, un stock initial et une description.
Un fichier « testImageEvent.jpg » peut être utilisé pour la photo, il est situé dans le dossier src/media/Tests. 
Lors de la création d'évènements, cocher la case "A la une" pour que l'évènement fasse partie des évènements affichés sur la page d'accueil.
Seuls les évènements dont la date est supérieure ou égale à la date du jour ET dont la case "A la une" aura été coché s'afficheront sur la page d'accueil.

Il n’est pas obligatoire de compléter le champs « Stock restant » qui se complètera par défaut par la même valeur que le stock initial.

Il n’est pas utile non plus de compléter le champs « Date limite de réservation » qui se complètera par défaut à J-2.

##    3. Utilisation de l’application via le navigateur internet, en local ou une fois déployée en tant qu’utilisateur :

Une fois les offres et les évènements créés, il est possible d’utiliser l’application en tant que visiteur ou utilisateur lambda. 
Se déconnecter du compte administrateur afin de pouvoir créer un compte utilisateur depuis la page d’accueil du site.

###        a. Créer un utilisateur et simuler l’achat d’un billet pour pouvoir effectuer une réservation afin de consulter l’évolution de la base de données en tant qu’administrateur.

##    4. Gestion administrateur (en se reconnectant depuis le compte administrateur) :

###        a. Contrôle de la validité d’un ticket (via QR code) :
Il est possible de vérifier la validé d'un ticket (=une réservation fait par un utilisateur avec un billet acheté) via la saisie manuelle (ou d'un lecteur de QR code qui renverra cette même saisie) à l'adresse suivante :
\verification_billet

Si un utilisateur lambda connecté ou non tente d'accéder à cette page, il sera redirigé vers la page de connexion. Cette page n’est accessible que pour les administrateurs, en vue de contrôler la validité d’un ticket le jour J. Les informations relatives à l’utilisateur, à l’achat et à la réservation concernée par le ticket s’afficheront ici.

###        b. Consultation des stocks restant :
La page \admin rend visible le stock restant des évènements en cliquant sur Evenements puis sur le nom de l'évènement.

###        c. Suppression d’un compte utilisateur : 
Si un utilisateur demande la suppression de son compte, elle est également rendue possible depuis \admin dans la section utilisateurs.
Il perdra alors ses billets ainsi que ses réservations.

###        d. Accès aux données utilisateurs :
L’administrateur peux accéder aux données utilisateurs si besoin en cliquant sur le champ utilisateurs. Seul le mot de passe restera masqué.

###        e. Réinitialisation d’un mot de passe perdu :
La réinitialisation du mot de passe n'est pas encore rendue autonome pour les utilisateurs.
En cas de demande, il est possible de réinitialiser le mot de passe en leur communiquant un mot de passe temporaire qu'ils devront impérativement changer depuis leur page de profil.

Par mesure de sécurité, il n'est pas possible de communiquer le mot de passe oublié à un utilisateur (ce dernier n’est pas visible même par un administrateur).

##    5. Remarques générales sur l’utilisation de l’application :

###        a. Reservation et annulation :
La réservation et l'annulation des évènements n'est rendu possible que jusqu'à J-2 de la date de l'évènement concernée par défaut.

###        b. QrCode des tickets :
La génération des QR-Code se faisant coté client (javascript), si le jour de l'évènement, le terminal client ne peut pas le générer (javascript désactivé par exemple sur le terminal), il est toujours possible d'accéder au numéro du ticket qui est également affiché en clair.

###        c. Temps de sessions :
Les sessions utilisateurs se ferment automatiquement passé 15 minutes d'inactivité.

###        d. Utilisations des comptes admin et users :
Un compte administrateur ne doit pas être utilisé pour accéder aux fonctionnalités client : il ne doit accéder qu'à \admin et \verification_billet

###        e. Page suppresion depuis la page \admin
Sur la page \admin, il est possible de supprimer :

Des billets achetés par les utilisateurs ;
Des réservations effectuées par les utilisateurs ;
Des évènements créés (qui supprimeront alors les réservations concernées et réalisées par les utilisateurs ainsi que leur billets achetés liés) ;
Et des Type de billets (=offres) qui aura également pour effet de supprimer les billets achetés par les utilisateurs sous ces offres.

Une attention toute particulière est donc indispensable lors de la suppression d'éléments ayant déjà été utilisés par les utilisateurs.

Des remboursements devront être réalisés dans le cas de telles suppression.
L'administration de Django alerte sur les conséquences de ces suppressions, et il est possible de les évaluer au cas par cas afin de permettre l'éventuel remboursement des utilisateurs.

Ces suppressions manuelles n’entrainent pas de remboursement automatique ni de remise à disposition des billets achetés.
Les remboursements devront donc se faire manuellement selon les informations fournies grâce au message d'avertissement de l'administration Django fourni après demande de suppression et avant confirmation de la suppression définitive.

##    6. Informations complémentaires concernant l’utilisation du code source depuis le dépôt :

###        a. Réalisation des tests :
Pour lancer les tests, depuis le dossier source du projet, exécuter la commande suivante :
```bash
python manage.py test
```
Cette commande va chercher à exécuter tous les tests définis dans les classes TestCase du projet

###        b. Export du rapport de couverture des tests :
Il est possible d’exporter un rapport de couverture de test avec les commandes suivantes (depuis le dossier /src)  :
Exécution des tests :
```bash
coverage run --source='.' manage.py test
```
Affichage du rapport dans le terminal :
```bash
coverage report
```
Génération du rapport html :
```bash
coverage html
```
Le fichier .coveragerc permet d’exclure du comptage les parties du code qui n’ont pas lieu d’être testées (tous le code pré-fourni par Django par exemple)


