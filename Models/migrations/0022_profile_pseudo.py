# Generated by Django 4.2.6 on 2024-07-17 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Models', '0021_profile_birthday_profile_email_profile_image_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='pseudo',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
