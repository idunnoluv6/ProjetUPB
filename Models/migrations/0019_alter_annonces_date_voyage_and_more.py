# Generated by Django 4.2.6 on 2024-07-16 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Models', '0018_alter_annonces_vu_date_achat'),
    ]

    operations = [
        migrations.AlterField(
            model_name='annonces',
            name='date_voyage',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='annonces_vu',
            name='date_voyage',
            field=models.DateField(default=None),
        ),
    ]
