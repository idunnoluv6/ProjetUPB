# vim: set fileencoding=utf-8 :
from django.contrib import admin

import Models.models as models


class compagnie_aerienneAdmin(admin.ModelAdmin):

    list_display = ('id', 'compagnie')
    list_filter = ('id', 'compagnie')


class DestinationAdmin(admin.ModelAdmin):

    list_display = ('id', 'ville')
    list_filter = ('id', 'ville')


class ProfileAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'user',
        'user_prenom',
        'registration_date',
        'email',
        'numero',
        'image',
        'sex',
        'birthday',
        'pseudo',
    )
    list_filter = (
        'user',
        'registration_date',
        'birthday',
        'id',
        'user_prenom',
        'email',
        'numero',
        'image',
        'sex',
        'pseudo',
    )


class annoncesAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'user',
        'vendeur',
        'compagnie',
        'numero_vendeur',
        'email',
        'localisation',
        'KG',
        'Prix',
        'date_pub',
        'Destination',
        'date_voyage',
    )
    list_filter = (
        'user',
        'compagnie',
        'date_pub',
        'Destination',
        'date_voyage',
        'id',
        'vendeur',
        'numero_vendeur',
        'email',
        'localisation',
        'KG',
        'Prix',
    )


class annonces_vuAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'client',
        'user',
        'pseudo_vendeur',
        'compagnie',
        'numero_vendeur',
        'email',
        'localisation',
        'KG',
        'Prix',
        'date_achat',
        'Destination',
        'date_voyage',
    )
    list_filter = (
        'user',
        'date_achat',
        'date_voyage',
        'id',
        'client',
        'pseudo_vendeur',
        'compagnie',
        'numero_vendeur',
        'email',
        'localisation',
        'KG',
        'Prix',
        'Destination',
    )


class annonces_annulerAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'client',
        'user',
        'pseudo_vendeur',
        'compagnie',
        'numero_vendeur',
        'email',
        'localisation',
        'KG',
        'Prix',
        'date_achat',
        'Destination',
        'date_voyage',
    )
    list_filter = (
        'user',
        'date_achat',
        'date_voyage',
        'id',
        'client',
        'pseudo_vendeur',
        'compagnie',
        'numero_vendeur',
        'email',
        'localisation',
        'KG',
        'Prix',
        'Destination',
    )


class verification_robotAdmin(admin.ModelAdmin):

    list_display = ('id', 'image')
    list_filter = ('id', 'image')


class reponse_verificationAdmin(admin.ModelAdmin):

    list_display = ('id', 'image', 'reponse_1', 'reponse_2', 'reponse_3')
    list_filter = ('image', 'id', 'reponse_1', 'reponse_2', 'reponse_3')


def _register(model, admin_class):
    admin.site.register(model, admin_class)


_register(models.compagnie_aerienne, compagnie_aerienneAdmin)
_register(models.Destination, DestinationAdmin)
_register(models.Profile, ProfileAdmin)
_register(models.annonces, annoncesAdmin)
_register(models.annonces_vu, annonces_vuAdmin)
_register(models.annonces_annuler, annonces_annulerAdmin)
_register(models.verification_robot, verification_robotAdmin)
_register(models.reponse_verification, reponse_verificationAdmin)
