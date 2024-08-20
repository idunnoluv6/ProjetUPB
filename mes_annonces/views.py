from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from Models import models
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages

# Create your views here.

@login_required

def affichage_mes_annonces(request):
    # Récupérer toutes les annonces de l'utilisateur actuel
    annonces_utilisateur = models.annonces.objects.filter(user=request.user)
    nombre_annonces = annonces_utilisateur.count()
    
    context = {
        'annonces_utilisateur': annonces_utilisateur,
        'nombre_annonces': nombre_annonces,
    }
    return render(request, 'orders.html', context)


@login_required

def form_annonce(request):
    data = {
        'dest': models.Destination.objects.all(),
        'comp': models.compagnie_aerienne.objects.all(),
    }
    
    if request.method == 'POST':
        compagnie_id = request.POST.get('compagnie')
        numero = request.POST.get('numero')
        localisation = request.POST.get('Adresse')
        kilo = request.POST.get('kilo')
        prix = request.POST.get('prix')
        destination_id = request.POST.get('destination')
        date_voyage = request.POST.get('date_voyage')

        # Vérifier que toutes les données nécessaires sont présentes
        if not compagnie_id or not numero or not localisation or not kilo or not prix or not destination_id or not date_voyage:
            return render(request, 'faire_annonce.html', {
                'error_message': "Veuillez remplir tous les champs.",
                **data
            })
        
        try:
            compagnie = models.compagnie_aerienne.objects.get(pk=compagnie_id)
        except models.compagnie_aerienne.DoesNotExist:
            return render(request, 'faire_annonce.html', {
                'error_message': "La compagnie aérienne sélectionnée n'est pas valide.",
                **data
            })

        try:
            destination = models.Destination.objects.get(pk=destination_id)
        except models.Destination.DoesNotExist:
            return render(request, 'faire_annonce.html', {
                'error_message': "La destination sélectionnée n'est pas valide.",
                **data
            })
        
        # Validate date_voyage
        try:
            date_voyage = timezone.datetime.strptime(date_voyage, '%Y-%m-%d').date()
            if date_voyage <= timezone.now().date():
                raise ValueError("La date de voyage doit être ultérieure à la date actuelle.")
        except ValueError as e:
            return render(request, 'faire_annonce.html', {
                'error_message': str(e),
                **data
            })
        
        profile = request.user.profile
        pseudo_vendeur = profile.pseudo
        # Création d'une nouvelle instance d'annonce avec les données reçues
        nouvelle_annonce = models.annonces(
            user=request.user,
            vendeur = pseudo_vendeur,
            compagnie=compagnie,
            email = request.user.email,
            numero_vendeur = profile.numero,
            localisation=localisation,
            KG=kilo,
            Prix=prix,
            Destination=destination,
            date_voyage=date_voyage,
        )
        nouvelle_annonce.save()  # Enregistrement de l'annonce dans la base de données

        # Redirection vers une vue d'affichage des annonces après l'enregistrement
        return redirect('affichage_mes_annonces')
    
    return render(request, 'faire_annonce.html', data)

