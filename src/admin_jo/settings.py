"""
Django settings for admin_jo project.

Generated by 'django-admin startproject' using Django 5.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

import os
from pathlib import Path
#SEB : import des variables d'environnement pour ne pas afficher de mot de passe en clair dans le code
from dotenv import load_dotenv
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
#SEB : sortie du code et mis en .env pour la re-generer : python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!

#SEB : lors du passage à DEBUG = False : modifier ALLOWED_HOSTS ; rassembler tous les fichiers static avec python manage.py collectstatic et avoir défini un dossier STATIC_ROOT

DEBUG = True
#DEBUG = False

#SEB: Si DEBUG = False et pour mise en production, indiquer ici les adresses pour le local : localhost et 127.0.0.1
#ALLOWED_HOSTS = []
ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'sebastien.alavigne.eu']

#SEB : utilisation de nginx il faut donc autoriser les requetes venant du nom de domaine public :
CSRF_TRUSTED_ORIGINS = ['https://sebastien.alavigne.eu']

#SEB : pour que la commande python manage.py collectstatic copie les fichiers statics dans ce dossier
STATIC_ROOT = os.path.join(BASE_DIR, 'static')


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app', #SEB: Ajout de mon application Django ici, sinon non reconnue
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'admin_jo.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,"admin_jo","templates")], #SEB: modification afin de trouver le dossier "templates" peut importe l'emplacement du dossier
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'admin_jo.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql', #SEB: modification des paramètres par defaut pour l'utilisation de postgresql (les nom d'utilisateur, password et nom de la bdd ont été créés au préalable et également avoir installé dans l'env psycopg)
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'fr-FR'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = False #SEB : réglé sur False (par défaut sur True) pour désactiver la gestion des fuseaux horraires et des problèmes qui peuvent être liés (pas d'utilité dans ce projet)


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'app/static')] #SEB : pour les fichiers static de l'app

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

#SEB : pour renvoyer vers la page d'accueil une fois logué ou dé-logué
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

#SEB : pour utiliser les fichiers multimedia (jpg pour cette app)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

#SEB : gestion des sessions à fermer :
SESSION_COOKIE_AGE = 900 #durée max 15min (900 secondes)
SESSION_ENGINE = 'django.contrib.sessions.backends.db'  # Utilise la session par base de données
SESSION_EXPIRE_AT_BROWSER_CLOSE = True # Session expire lorsque l'utilisateur ferme son navigateur

#SEB : Important à définir car changement par rapport aux valuurs par defaut de Django qui utilise le dossier templates/registration/
LOGIN_URL = 'login' 

