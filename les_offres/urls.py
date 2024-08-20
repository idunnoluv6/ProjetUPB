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
    path('', views.affichage_vente, name='affichage_vente'),
    path('facture/<uuid:carte_id>/', views.generate_qr, name='generate_qr'),
    path('valider/<uuid:carte_id>/', views.valider, name='valider'),
    path('supprimer_annonce/<uuid:carte_id>/', views.supprimer_annonce, name='supprimer_annonce'),
    path('account_vendeur/', views.account_vendeur, name='account_vendeur'),
    #path('account_vendeur/evaleur/', views.edit_evaluation, name='edit_evaluation'),
]