# views.py

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login, authenticate, logout
from django.views.decorators.csrf import csrf_protect
from Models import models
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.core.files.storage import FileSystemStorage
from django.db.models.signals import post_save
from django.dispatch import receiver




def signup(request):
    if request.method == 'POST':
        # Récupération des données du formulaire
        username = request.POST.get('signup-name', '')
        user_prenom = request.POST.get('signup-Prename', '')
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')
        email = request.POST.get('email', '')
        numero = request.POST.get('numero', '')
        sex = request.POST.get('sex', '')
        birthday = request.POST.get('birthday', '')
        image = request.FILES.get('image', '')

        # Validation des champs obligatoires
        if not username or not user_prenom or not password1 or not password2 or not email or not numero or not sex or not birthday:
            return render(request, 'signup.html', {'error_message': "Veuillez remplir tous les champs."})

        # Vérification si les mots de passe correspondent
        if password1 != password2:
            return render(request, 'signup.html', {'error_message': "Les mots de passe ne correspondent pas."})

        # Vérification si l'utilisateur existe déjà
        if User.objects.filter(email=email).exists():
            return render(request, 'signup.html', {'error_message': "Cet email est déjà pris."})

        # Création de l'utilisateur
        user = User.objects.create_user(username=username, password=password1, email=email)

        # Création du profil associé
        profile = models.Profile(user=user, user_prenom=user_prenom, email=email, sex=sex, birthday=birthday, numero=numero)
        if image:
            profile.image = image  # Associer l'image au champ 'image' du profil

        try:
            # Générer le pseudo et enregistrer dans le profil
            pseudo = profile.generate_pseudo()
            profile.save()
        except Exception as e:
            print(f"Error generating pseudo: {e}")
            return render(request, 'signup.html', {'error_message': "Erreur lors de la création du profil."})

        # Envoi d'un email avec le pseudo généré
        subject = 'Bienvenue sur LOKI !'
        message = f'Bonjour {username} {user_prenom}, votre pseudo est : {pseudo}. Utilisez-le pour vous connecter à votre compte LOKI !'
        from_email = settings.EMAIL_HOST_USER
        to_email = [email]

        try:
            server = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
            server.ehlo()
            server.starttls()
            server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)

            msg = MIMEMultipart()
            msg['From'] = from_email
            msg['To'] = ', '.join(to_email)
            msg['Subject'] = subject

            msg.attach(MIMEText(message, 'plain'))

            server.sendmail(from_email, to_email, msg.as_string())
            server.quit()

            print("Email sent successfully!")
        except Exception as e:
            print(f"Error sending email: {e}")
            return render(request, 'signup.html', {'error_message': "Erreur lors de l'envoi de l'email."})

        # Authentification et connexion de l'utilisateur
        user = authenticate(username=username, password=password1)
        login(request, user)

        # Redirection après l'inscription
        return redirect('signin')  # Assurez-vous d'avoir une vue nommée 'signin' dans vos URLs

    else:
        return render(request, 'signup.html')

def signin(request):
    if request.method == 'POST':
        pseudo = request.POST.get('login-name', '')  # Récupération du pseudo depuis le formulaire
        password = request.POST.get('signin-password', '')  # Récupération du mot de passe

        # Recherche de l'utilisateur par pseudo dans le profil associé
        try:
            user_profile = models.Profile.objects.get(pseudo=pseudo)
            user = user_profile.user  # Récupération de l'utilisateur associé au profil
        except models.Profile.DoesNotExist:
            user = None

        # Authentification de l'utilisateur
        if user is not None:
            # Vérification si la licence du profil est valide
            if not user_profile.is_license_valid():
                return render(request, 'login.html', {'error_message': "Votre licence a expiré. Veuillez contacter le support."})

            user = authenticate(request, username=user.username, password=password)

            if user is not None:
                auth_login(request, user)  # Authentification de l'utilisateur
                request.session['username'] = pseudo  # Stockage du pseudo dans la session
                return redirect('affichage_index')  # Redirection vers la page principale après connexion
            else:
                return render(request, 'login.html', {'error_message': "Mot de passe incorrect."})
        else:
            return render(request, 'login.html', {'error_message': "Pseudo incorrect."})

    else:
        return render(request, 'login.html')

def affichage_reset (request) :
    data = {
    }
    return render (request, 'reset_password.html', data)


def logout_views (request) :
    logout(request)
    return redirect ('signin')




