# Generated by Django 4.2.6 on 2024-08-09 09:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Models', '0040_profile_numero'),
    ]

    operations = [
        migrations.CreateModel(
            name='annonces_annuler',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('client', models.CharField(default=None, max_length=20)),
                ('pseudo_vendeur', models.CharField(default=None, max_length=20)),
                ('compagnie', models.CharField(default=None, max_length=20)),
                ('numero_vendeur', models.CharField(default=None, max_length=20)),
                ('email', models.CharField(default=None, max_length=100)),
                ('localisation', models.CharField(max_length=20)),
                ('KG', models.IntegerField(default=None)),
                ('Prix', models.BigIntegerField(default=None)),
                ('date_achat', models.DateTimeField(auto_now_add=True)),
                ('Destination', models.CharField(default=None, max_length=20)),
                ('date_voyage', models.DateField(default=None)),
                ('user', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
