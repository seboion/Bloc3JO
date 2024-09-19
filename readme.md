Fonctionnement du projet "Bloc3", exercice de réalisation d'un site de reservation de tickets pour les évènements des JO 2024 :

1.  Restauration de toutes les dépendances du projets avec la commande 
    pip install -r requirements.txt

2.  Le projet necessite la mise à disposition d'une base de donnée PostgreSQL (PostgreSQL doit donc être installé au préalable sur le système)
    Pour le projet, une base de donnée nommée "jobdd" a été créée avec comme user "joadmin" et mot de passe "12369**/"
    Les commandes pour la création de la base de donnée :
    
    sudo -i -u postgres                             # Pour avoir acceder à PostgreSQL en tant que super utilisateur
    psql                                            # Accès à l'interface PostgreSQL 
    CREATE USER joadmin WITH PASSWORD "12369**/";   # Création de l'utilisateur (suivant l'exemple précédemment cité, à modifier donc)
    CREATE DATABASE jobdd OWNER jodamin;            # Création de la base de donnée
    \q                                              # Quitter l'interface
    exit                                            # Revenir à l'utilisateur normal

    Les informations relatifs à la base de données sont situées dans le fichier settings.py du projet Django dans la variable (dict) DATABASE
    Modifier ces valeurs en fonction du nouveau nom d'utilisateur et mot de passe choisi

3.  Création du compte administrateur du site (permettant de visualiser et modifier les types de billets mise en vente et les évènements) :
    Avec les commandes suivantes (dans le dossier source du projet)
    python manage.py createsuperuser

    Pour l'exemple du projet les informations suivantes peuvent être utilisées : 
    user : joadmin
    mail : joadmin@joadmin.com
    password : 12369++-

4.  Réaliser les migrations avec les commandes suivantes (toujours dans le dossier source du projet) : 
    python manage.py makemigrations
    python manage.py migrate

5.  Lancer le serveur pour acceder au projet via le navigateur internet :
    python manage.py runserver
    puis ouvrir le liens local ainsi générer (CTRL+C pour fermer le serveur local)

5.  Une fois sur le site internet, se rendre sur /admin du site pour accéder à l'interface administrateur
