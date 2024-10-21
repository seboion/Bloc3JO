Fonctionnement du projet "Bloc3", exercice de réalisation d'un site de reservation de tickets pour les évènements des JO 2024 :

1.  Restauration de toutes les dépendances du projets avec la commande 
    pip install -r requirements.txt

2.  Le projet necessite la mise à disposition d'une base de donnée PostgreSQL (PostgreSQL doit donc être installé au préalable sur le système)
    Les données devront être stockées dans le fichiers .env situé à la racine du projet sous ce format :
    DB_NAME=##nom de votre base de donnée##
    DB_USER=##utilisateur de votre base de donnée##
    DB_PASSWORD=##mot de passe choisi##
    DB_HOST=##adresse , localhost si projet utilisé en local##
    DB_PORT=## port utilisé, 5432 par défaut si utilisé en local##


    Les commandes pour la création de la base de donnée :
    
    sudo -i -u postgres                             # Pour avoir acceder à PostgreSQL en tant que super utilisateur
    psql                                            # Accès à l'interface PostgreSQL 
    CREATE USER joadmin WITH PASSWORD "********";   # Création de l'utilisateur (suivant l'exemple précédemment cité)
    CREATE DATABASE jobdd OWNER "*user";            # Création de la base de donnée
    \q                                              # Quitter l'interface
    exit                                            # Revenir à l'utilisateur normal

    Les informations relatifs à la base de données sont reprise dans le fichier settings.py du projet Django dans la variable (dict) DATABASE

3.  Création du compte administrateur du site (permettant de visualiser et modifier les types de billets mise en vente et les évènements) :
    Avec les commandes suivantes (dans le dossier source du projet)
    python manage.py createsuperuser

4.  Réaliser les migrations avec les commandes suivantes (toujours dans le dossier source du projet) : 
    python manage.py makemigrations
    python manage.py migrate

5.  Lancer le serveur pour acceder au projet via le navigateur internet :
    python manage.py runserver
    puis ouvrir le liens local ainsi générer (CTRL+C pour fermer le serveur local)

5.  Une fois sur le site internet, se rendre sur /admin du site pour accéder à l'interface administrateur

6.  Commencer par créer les types d'offres (Solo, Duo, Famille) et des évènements pour les réservations (un fichier testImageEvent.jpg peut être utilisé il est situé dans le dossier src/media/Tests)

7.  Lors de la création d'évènements, cocher la case "A la une" pour que l'évènement fasse partie des évènements affichés sur la page d'accueil.
    Seuls les évènements dont la date est supérieure ou égale à la date du jour ET dont la case "A la une" aura été coché s'afficheront sur la page d'accueil.

8.  La reservation et l'annulation des évènements n'est rendu possible que jusqu'à J-2 de la date de l'évènement concernée

9. La génération des QR-Code se faisant coté client (javascript), si le jour de l'évènement le terminal client ne peut pas le générer, il est toujours possible d'acceder au numéro du ticket qui est également affiché.

10. Les sessions utilisateurs se ferment automatiquement passé 15 minutes d'inactivité

11. Il est possible de vérifier la valité d'un ticket (=une reservation) via la saisie manuelle (ou d'un lecteur de QR code qui renverra cette même saisie) à l'adresse suivante : \verification_billet . Seul un compte administrateur pourra acceder à cette page. Si un utilisateur lambda connecté ou non tente d'acceder à cette page, il sera rediriger vers la page de connexion.

12. Un compte administrateur ne doit pas être utilisé pour acceder aux fonctionnalités client : il ne peut acceder qu'à \admin et \verification_billet

13. La page \admin rend visible le stock restant des évènements en cliquant sur Evenements puis le nom de l'évènement.

14. Sur la page \admin, il est possible de supprimer des billets achetés par les utilisateurs, des réservations effectuées par les utilisateurs ; des évènements (qui supprimeront alors les reservations concernées et réalisées par les utilisateurs ainsi que leur billets achetés liés) et les Type de billets (=offres) qui aura également pour effet de supprimer les billets achetés par les utilisateurs sous ces offres. Une attention toute particulière est donc indispensable lors de la suppression d'éléments ayant déjà été utilisés par les utilisateurs. Des remboursements devront être réalisés dans le cas de tels suppression. L'administration de Django alerte sur les consequences de ces suppressions, et il est possible de les évaluer au cas par cas afin de permettre l'éventuel remboursement des utilisateurs. Ces suppressions manuelles n'entraine pas de remboursement automatique ni de remise à disposition des billets achetés. Les remboursements devront donc se faire manuellement selon les informations fournies grâce au message d'avertissement de l'administration Django fourni après demande de suppression et avant confirmation de la suppression définitive.

15. Si un utilisateur demande la suppression de son compte, elle est également rendue possible depuis \admin dans la section utilisateurs. Il perdra alors ses billets ainsi que ses reservations.

16. La réinitialisation du mot de passe n'est pas encore rendu autonome pour les utilisateurs. En cas de demande, il est possible de réinitialiser le mot de passe en leur communiquant un mot de passe temporaire qu'ils devront impérativement changer depuis leur page de profil.

17. Par mesure de sécurité, il n'est pas possible de communiquer le mot de passe oublié à un utilisateur.

18. Tests de l'application : Pour lancer les tests, depuis le dossier source du projet, exécuter la commande suivante : 
    python manage.py test
    Cette commande va chercher à executer tous les tests définis dans les classes TestCase du projet

19. Reset la secret_key Django : python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'


