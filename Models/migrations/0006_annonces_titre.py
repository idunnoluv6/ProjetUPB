# Generated by Django 4.2.6 on 2024-07-11 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Models', '0005_alter_annonces_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='annonces',
            name='titre',
            field=models.CharField(default=None, max_length=20),
        ),
    ]