# Generated by Django 4.2.6 on 2024-07-10 18:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Models', '0003_rename_nom_vendeur_annonces_numero_vendeur'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='annonces',
            name='code_vente',
        ),
    ]
