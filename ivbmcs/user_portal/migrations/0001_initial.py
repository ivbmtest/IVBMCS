# Generated by Django 5.0.1 on 2024-02-23 06:28

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('admin_panel', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Free_consult_detail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(max_length=15, verbose_name='Phone number')),
                ('service', models.CharField(blank=True, max_length=15, verbose_name='Service')),
            ],
        ),
        migrations.CreateModel(
            name='userdata',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, verbose_name='Name')),
                ('phone_number', models.CharField(blank=True, max_length=15, unique=True, verbose_name='Phone number')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='Email')),
                ('status', models.CharField(blank=True, max_length=255, verbose_name='Status')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='user_service_details',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment', models.BooleanField(blank=True, default=False, verbose_name='Payment')),
                ('msg', models.TextField(blank=True, verbose_name='user Query')),
                ('documents', models.JSONField(blank=True, default='', verbose_name='Documents')),
                ('taken_by', models.CharField(blank=True, max_length=255, verbose_name='Taken')),
                ('status', models.CharField(blank=True, max_length=255, verbose_name='Status')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin_panel.srvc', verbose_name='Service')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='user_id')),
            ],
        ),
        migrations.CreateModel(
            name='user_notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('recepient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('service', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='user_portal.user_service_details')),
            ],
        ),
    ]
