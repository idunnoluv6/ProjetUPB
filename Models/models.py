from django.db import models
from django.db.models import Sum
import uuid
from datetime import date
import random
from datetime import datetime, timedelta
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import os
from PIL import Image, ImageOps
from django.core.validators import MinValueValidator, MaxValueValidator


def resize_image(image, size):
    img = Image.open(image)
    img = ImageOps.fit(img, size, Image.LANCZOS)
    img.save(image.path)

def get_upload_path(instance, filename):
    pseudo = instance.pseudo
    _, ext = os.path.splitext(filename)
    return os.path.join('Profile', f'{pseudo}{ext}')

class compagnie_aerienne(models.Model):
    compagnie = models.CharField(max_length = 20, default = None)
    def __str__(self) -> str:
        return self.compagnie
    class Meta:
        ordering = ['compagnie']
    

class Destination(models.Model):
    ville = models.CharField(max_length = 50, default = None)
    def __str__(self) -> str:
        return self.ville
    class Meta:
        ordering = ['ville']
    


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_prenom = models.CharField(max_length=50, blank=True)
    registration_date = models.DateField(auto_now_add=True)
    email = models.EmailField(blank=True)
    numero = models.CharField(max_length=10, blank=True)
    image = models.ImageField(upload_to= get_upload_path, height_field=None, width_field=None, max_length=None)
    sex = models.CharField(max_length=10, blank=True)
    birthday = models.DateField(blank=True, null=True)
    pseudo = models.CharField(max_length=50, blank=True) 

    def __str__(self):
        return self.user.username

    def get_expiry_date(self):
        return self.registration_date + timedelta(days=30)

    def is_license_valid(self):
        current_date = timezone.now().date()
        expiry_date = self.get_expiry_date()
        return current_date <= expiry_date
    
    def generate_pseudo(self):
        username = self.user.username        
        first_letter = username[0].upper() if username else ''
        prenom = self.user_prenom
        random_number = ''.join([str(random.randint(0, 9)) for _ in range(3)])
        pseudo = f"{first_letter}{prenom}{random_number}"
        self.pseudo = pseudo
        self.save()
        
        return pseudo  

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            resize_image(self.image, (280, 280))


class annonces (models.Model) :
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default = None)
    vendeur = models.CharField(max_length = 20, default = None)
    compagnie = models.ForeignKey(compagnie_aerienne, on_delete=models.CASCADE, default = None)
    numero_vendeur = models.CharField(max_length = 20, default = None)
    email = models.CharField(max_length = 100, default = None)
    localisation = models.CharField(max_length = 20, default = None)
    KG = models.IntegerField(default = None)
    Prix = models.BigIntegerField(default = None)
    date_pub = models.DateTimeField(auto_now_add = True)
    Destination = models.ForeignKey(Destination, on_delete=models.CASCADE, default = None)
    date_voyage = models.DateField(default = None)

    def __str__(self) -> str:
        return self.numero_vendeur
    
    def total_kilo(self):
        total = annonces.objects.filter(user=self.user).aggregate(total_kilo=models.Sum('KG'))['total_kilo']
        return total or 0
    
    def total_somme(self):
        total_somme = annonces.objects.filter(user=self.user).aggregate(total_somme=models.Sum('Prix'))['total_somme']
        return total_somme or 0
    
    def est_perimee(self):
        return self.date_voyage < timezone.now().date()

    @classmethod
    def supprimer_perimees(cls):
        annonces_perimees = cls.objects.filter(date_voyage__lt=timezone.now().date())
        count_deleted = annonces_perimees.delete()[0]  # Supprime les annonces périmées et récupère le nombre d'enregistrements supprimés
        return count_deleted


class annonces_vu(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    client = models.CharField(max_length = 20, default = None)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default = None)
    pseudo_vendeur = models.CharField(max_length = 20, default = None)
    compagnie = models.CharField(max_length = 20, default = None)
    numero_vendeur = models.CharField(max_length = 20, default = None)
    email = models.CharField(max_length = 100, default = None)
    localisation = models.CharField(max_length = 20)
    KG = models.IntegerField(default = None)
    Prix = models.BigIntegerField(default = None)
    date_achat = models.DateTimeField(auto_now_add = True)
    Destination = models.CharField(max_length = 20, default = None)
    date_voyage = models.DateField(default = None)

    def __str__(self) -> str:
        return self.numero_vendeur
    

class annonces_annuler(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    client = models.CharField(max_length = 20, default = None)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default = None)
    pseudo_vendeur = models.CharField(max_length = 20, default = None)
    compagnie = models.CharField(max_length = 20, default = None)
    numero_vendeur = models.CharField(max_length = 20, default = None)
    email = models.CharField(max_length = 100, default = None)
    localisation = models.CharField(max_length = 20)
    KG = models.IntegerField(default = None)
    Prix = models.BigIntegerField(default = None)
    date_achat = models.DateTimeField(auto_now_add = True)
    Destination = models.CharField(max_length = 20, default = None)
    date_voyage = models.DateField(default = None)

    def __str__(self) -> str:
        return self.numero_vendeur
        

#class question_verification(models.Model):
#    question = models.TextField()


#class question_verification(models.Model):
#    user = models.ForeignKey(User, on_delete=models.CASCADE, default = None)
#    question = models.ForeignKey(question_verification, on_delete=models.CASCADE, default = None)
#    reponse = models.TextField()

    
class verification_robot (models.Model):
    image = models.ImageField(upload_to= get_upload_path, height_field=None, width_field=None, max_length=None)

class reponse_verification (models.Model):
    image = models.ForeignKey(verification_robot, on_delete = models.CASCADE)
    reponse_1 = models.CharField(max_length = 20, default = None)
    reponse_2 = models.CharField(max_length = 20, default = None)
    reponse_3 = models.CharField(max_length = 20, default = None)

#class annonces (models.Model):
#    vendeur = models.ForeignKey(annonces_vu, on_delete = models.CASCADE)
#    evaluation = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])
