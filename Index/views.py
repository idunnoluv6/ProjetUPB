from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.db.models import Count, Sum
from Models import models
from django.http import HttpRequest, HttpResponse


def affichage_index(request):
    user = request.user
    annonces_list = models.annonces.objects.count()  # Récupère toutes les annonces
    username = request.session.get('username', 'Utilisateur inconnu')
    users_count = User.objects.count()

    ventes_stats = models.annonces_vu.objects.filter(user=user).values('Destination').annotate(total_kilos= models.Sum('KG'), total_somme=Sum('Prix'), nombre_ventes= Count('id')).order_by('Destination')[:5]
    achats_stats = models.annonces_vu.objects.filter(client = user).values('Destination').annotate(total_kilos= models.Sum('KG'), total_somme=Sum('Prix'), nombre_ventes= Count('id')).order_by('Destination')[:5]

    total_kilo = models.annonces_vu.objects.filter(user=user).aggregate(total_kilo=models.Sum('KG'))['total_kilo'] or 0
    total_somme = models.annonces_vu.objects.filter(user=user).aggregate(total_somme=Sum('Prix'))['total_somme'] or 0
    total_kilo_acheter = models.annonces_vu.objects.filter(client=user).aggregate(total_kilo=models.Sum('KG'))['total_kilo'] or 0
    total_somme_dep = models.annonces_vu.objects.filter(client=user).aggregate(total_somme=models.Sum('Prix'))['total_somme'] or 0
    context = {
        'user' : user,
        'username': username,
        'annonces_list': annonces_list,
        'users_count': users_count,
        'total_kilo': total_kilo,
        'total_somme' : total_somme,
        'total_kilo_acheter': total_kilo_acheter,
        'total_somme_dep' : total_somme_dep,
        'ventes_stats': ventes_stats,
        'achats_stats' : achats_stats,
    }
    return render(request, 'index.html', context)


def affichage_historique (request) :
    user = request.user
    annonces_vu_user = models.annonces_vu.objects.filter(user=user).order_by('-date_achat')[:10]
    annonces_vu_client = models.annonces_vu.objects.filter(client = user).order_by('-date_achat')[:10]
    annonces_annuler_client = models.annonces_annuler.objects.filter(client = user).order_by('-date_achat')[:10]
    context = {
        'user': user,
        'annonces_vu_user': annonces_vu_user,
        'annonces_vu_client': annonces_vu_client,
        'annonces_annuler_client' : annonces_annuler_client,
    }
    return render(request, 'historique.html', context)


def affichage_notif (request) :
    data = {
    }
    return render (request, 'notifications.html', data)


def affichage_account (request) :
    user = request.user
    try:
        profile = models.Profile.objects.get(user=user)
    except models.Profile.DoesNotExist:
        profile = None
    context = {
        'user' : user,
        'profile': profile,
    }
    return render (request, 'account.html', context)


def affichage_settings (request) :
    user = request.user
    profile = request.user.profile  # Obtenez le profil associé à l'utilisateur connecté
    expiry_date = profile.get_expiry_date()  # Utilisez l'instance de Profile pour appeler la méthode
    try:
        profile = models.Profile.objects.get(user=user)
    except models.Profile.DoesNotExist:
        profile = None
    context = {
        'user' : user,
        'profile': profile,
        'expiry_date' : expiry_date,
    }
    return render (request, 'settings.html', context)


def affichage_error (request) :
    data = {
    }
    return render (request, '404.html', data)


def affichage_help (request) :
    data = {
    }
    return render (request, 'help.html', data)

def succes(request):
    return render(request, 'succes.html')
