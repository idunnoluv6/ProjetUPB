from django.shortcuts import render, redirect, get_object_or_404
from Models import models
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest
import io
import qrcode
import base64
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

@csrf_exempt
def supprimer_annonce(request, carte_id):
    if request.method == 'GET':
        # Récupérer l'annonce à partir de l'ID, ou renvoyer une erreur 404 si non trouvée
        annonce = get_object_or_404(models.annonces, id=carte_id)

        # Créer une nouvelle instance de annonces_vu et sauvegarder
        nouvelle_annonce_sup = models.annonces_annuler.objects.create(
            client=request.user,
            user=annonce.user,
            id=annonce.id,
            pseudo_vendeur = annonce.vendeur,
            email = annonce.email,
            numero_vendeur = annonce.numero_vendeur,
            localisation = annonce.localisation,
            compagnie=annonce.compagnie,
            KG=annonce.KG,
            Prix=annonce.Prix,
            Destination=annonce.Destination,
            date_voyage=annonce.date_voyage,
        )
        
        # Supprimer l'annonce d'origine
        annonce.delete()

        return redirect('affichage_mes_annonces')
    else:
        return HttpResponse(status=400)


def affichage_vente (request) :
    user = request.user
    annonces = models.annonces.objects.exclude(user=user).order_by('-date_pub')  # Exclure les annonces de l'utilisateur actif
    context = {
        'user': user,
        'annonce': annonces,
    }
    return render (request, 'docs.html', context)


def generate_qr(request, carte_id) :
    # Récupérer l'annonce à partir de l'ID, ou renvoyer une erreur 404 si non trouvée
    annonce = get_object_or_404(models.annonces, id=carte_id)

    # Construire la chaîne de données à encoder dans le code QR
    data_to_encode = (
        f"code annonce: {annonce.id}, "
        f"Annoceur: {annonce.vendeur}, "
        f"Localisation: {annonce.localisation}, "
        f"Numéro vendeur: {annonce.numero_vendeur}, "
        f"Email: {annonce.email}, "
        f"Compagnie: {annonce.compagnie}, "
        f"KG: {annonce.KG} KG, "
        f"Prix: {annonce.Prix} FCFA, "
        f"Destination: {annonce.Destination}, "
        f"Date voyage: {annonce.date_voyage}"
    )
    # Créer un objet QRCode
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    # Ajouter les données à l'objet QRCode
    qr.add_data(data_to_encode)
    qr.make(fit=True)

    # Créer une image PIL (Python Imaging Library) à partir de l'objet QRCode
    img = qr.make_image(fill_color="black", back_color="white")

    # Enregistrer l'image dans un buffer BytesIO
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")  # Sauvegarder l'image en format PNG

    # Convertir l'image en base64
    image_data = buffer.getvalue()
    img_base64 = base64.b64encode(image_data).decode('utf-8')  # Encodage en base64

    # Rendre l'image dans un template
    return render(request, 'facture.html', {'qr_code': img_base64, 'annonce': annonce})


def valider(request, carte_id):
    if request.method == 'GET':
        # Récupérer l'annonce à partir de l'ID, ou renvoyer une erreur 404 si non trouvée
        annonce = get_object_or_404(models.annonces, id=carte_id)
        profile = request.user.profile

        # Créer une nouvelle instance de annonces_vu et sauvegarder
        nouvelle_annonce_vu = models.annonces_vu.objects.create(
            client=request.user,
            user=annonce.user,
            id=annonce.id,
            pseudo_vendeur = annonce.vendeur,
            email = annonce.email,
            numero_vendeur = annonce.numero_vendeur,
            localisation = annonce.localisation,
            compagnie=annonce.compagnie,
            KG=annonce.KG,
            Prix=annonce.Prix,
            Destination=annonce.Destination,
            date_voyage=annonce.date_voyage,
        )
        
        # Supprimer l'annonce d'origine
        annonce.delete()

        # Récupérer les informations nécessaires pour l'email
        username = request.session.get('username', 'Utilisateur inconnu')
        user_prenom = profile.user_prenom


        # Envoi de l'email de confirmation
        subject = 'Confirmation d\'achat sur notre plateforme'
        message = f'Bonjour {annonce.user} ,\n\nVotre annonce du {annonce.date_pub} de {annonce.KG}KG au prix de {annonce.Prix}FCFA en direction de {annonce.Destination} pour le {annonce.date_voyage} vient d\'etre confirmer par {username}:\n\n' \
                  f'Il vous contactera dans les jours a venir !\n'\
                  f'Vous pouvez aussi le contacter au {annonce.numero_vendeur} !\n'\
                  f'Merci d\'etre LOKI !'

        from_email = settings.EMAIL_HOST_USER

        try:
            server = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
            server.ehlo()
            server.starttls()
            server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)

            msg = MIMEMultipart()
            msg['From'] = from_email
            msg['To'] = ', '.join(annonce.email)
            msg['Subject'] = subject

            msg.attach(MIMEText(message, 'plain'))

            server.sendmail(from_email, annonce.email, msg.as_string())
            server.quit()

            print("Email sent successfully!")
        except Exception as e:
            print(f"Error sending email: {e}")
            # Gérer l'échec de l'envoi d'email ici, par exemple afficher un message d'erreur à l'utilisateur

        # Redirection vers la page de succès après validation
        return redirect('succes')
    else:
        return HttpResponse(status=400)
    

def account_vendeur (request) :    
    return render (request, 'account_vendeur.html')


def evaluer_annonce(request, annonce_id):
    annonce = get_object_or_404(models.annonces, pk=annonce_id)
    
    if request.method == 'POST':
        evaluation = int(request.POST.get('rating'))
        if 1 <= evaluation <= 5:
            annonce.evaluation = evaluation
            annonce.save()
            # Redirection vers une autre vue ou retourner une réponse appropriée
            return redirect('detail_annonce', annonce_id=annonce.id)
        else:
            # Gérer l'erreur si l'utilisateur tente de soumettre une valeur non valide
            return HttpResponseBadRequest("Évaluation invalide")
    
    # Afficher le formulaire pour l'évaluation si la méthode n'est pas POST
    return render(request, 'evaluer_annonce.html', {'annonce': annonce})