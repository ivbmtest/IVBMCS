# Generated by Django 5.0.1 on 2024-03-19 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_portal', '0017_user_service_details'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_service_details',
            name='taken_by',
            field=models.CharField(blank=True, max_length=255, verbose_name='Taken'),
        ),
    ]
