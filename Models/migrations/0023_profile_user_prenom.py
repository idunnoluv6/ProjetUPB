# Generated by Django 4.2.6 on 2024-07-18 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Models', '0022_profile_pseudo'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='user_prenom',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
