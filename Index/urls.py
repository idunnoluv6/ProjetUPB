"""
URL configuration for ProjetUPB project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.affichage_index, name='affichage_index'),
    path('historique/', views.affichage_historique, name='affichage_historique'),
    path('notification/', views.affichage_notif, name='affichage_notif'),
    path('account/', views.affichage_account, name='affichage_account'),
    path('settings/', views.affichage_settings, name='affichage_settings'),
    path('404/', views.affichage_error, name='affichage_error'),
    path('help/', views.affichage_help, name='affichage_help'),
    path('Achat_valider/', views.succes, name='succes'),
]