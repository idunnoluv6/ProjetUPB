from django.shortcuts import render
from paypalrestsdk import Payment
from django.conf import settings
from django.urls import reverse
from paypal.standard.forms import PayPalPaymentsForm
from Models import models

def payment_process(request):
    # Définir le montant en francs CFA (5000 francs CFA = environ 9,50 USD)
    amount_cfa = '5000.00'
    import time
    invoice_id = str(int(time.time()))
    
    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': amount_cfa,
        'currency_code': 'XAF',  # Code de devise pour les francs CFA
        'item_name': 'Reabonnement',
        'invoice': invoice_id,
        'notify_url': request.build_absolute_uri(reverse('paypal-ipn')),
        'return_url': request.build_absolute_uri(reverse('payment_done')),
        'cancel_return': request.build_absolute_uri(reverse('payment_cancelled')),
    }

    form = PayPalPaymentsForm(initial=paypal_dict)
    context = {'form': form}
    return render(request, 'invoice.html', context)


# Create your views here.

def affichage_licence(request):
    try:
        profile = request.user.profile  # Obtenez le profil associé à l'utilisateur connecté
        expiry_date = profile.get_expiry_date()  # Utilisez l'instance de Profile pour appeler la méthode
        return render(request, 'licence.html', {'expiry_date': expiry_date})
    except models.Profile.DoesNotExist:
        # Gérer le cas où le profil n'existe pas pour cet utilisateur
        return render(request, '404.html')


def paypal_button_view(request):
    return render(request, 'paypal_button.html')