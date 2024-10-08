# Generated by Django 4.2.6 on 2024-08-03 08:06

import Models.models
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Models', '0035_annonces_vu_pseudo_vendeur'),
    ]

    operations = [
        migrations.CreateModel(
            name='verification_robot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=Models.models.get_upload_path)),
            ],
        ),
        migrations.RemoveField(
            model_name='annonces',
            name='Destination',
        ),
        migrations.RemoveField(
            model_name='annonces',
            name='KG',
        ),
        migrations.RemoveField(
            model_name='annonces',
            name='Prix',
        ),
        migrations.RemoveField(
            model_name='annonces',
            name='compagnie',
        ),
        migrations.RemoveField(
            model_name='annonces',
            name='date_pub',
        ),
        migrations.RemoveField(
            model_name='annonces',
            name='date_voyage',
        ),
        migrations.RemoveField(
            model_name='annonces',
            name='email',
        ),
        migrations.RemoveField(
            model_name='annonces',
            name='localisation',
        ),
        migrations.RemoveField(
            model_name='annonces',
            name='numero_vendeur',
        ),
        migrations.RemoveField(
            model_name='annonces',
            name='user',
        ),
        migrations.AddField(
            model_name='annonces',
            name='evaluation',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)]),
        ),
        migrations.AlterField(
            model_name='annonces',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='annonces',
            name='vendeur',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Models.annonces_vu'),
        ),
        migrations.CreateModel(
            name='reponse_verification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reponse_1', models.CharField(default=None, max_length=20)),
                ('reponse_2', models.CharField(default=None, max_length=20)),
                ('reponse_3', models.CharField(default=None, max_length=20)),
                ('image', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Models.verification_robot')),
            ],
        ),
    ]
