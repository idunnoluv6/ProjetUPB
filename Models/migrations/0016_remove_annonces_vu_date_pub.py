# Generated by Django 4.2.6 on 2024-07-16 15:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Models', '0015_annonces_vu_me'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='annonces_vu',
            name='date_pub',
        ),
    ]
