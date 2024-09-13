"""
URL configuration for admin_jo project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include #SEB : ajout de include pour permettre l'inclusion du fichier urls.py de l'app dans le projet

urlpatterns = [
    path('admin/', admin.site.urls), #SEB : déjà dans le projet DJANGO par défaut, c'est l'url de l'admin DJANGO , à garder pour plus tard pour la gestion de l'administrateur
    path('', include('app.urls')), #SEB : permet ici d'inclure les urls de l'app
]
