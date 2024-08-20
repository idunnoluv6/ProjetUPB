# Generated by Django 4.2.6 on 2024-07-22 00:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Models', '0026_annonces_vendeur_alter_annonces_destination_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='compagnie_aerienne',
            options={'ordering': ['compagnie']},
        ),
        migrations.AlterModelOptions(
            name='destination',
            options={'ordering': ['ville']},
        ),
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(upload_to='Profile/'),
        ),
    ]