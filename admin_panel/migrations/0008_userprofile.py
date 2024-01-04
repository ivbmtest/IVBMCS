# Generated by Django 5.0.1 on 2024-01-04 04:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0007_documentsrequired_delete_documentsrequireds'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('phone_number', models.CharField(max_length=15, verbose_name='Phone number')),
                ('email', models.EmailField(max_length=254, verbose_name='Email')),
                ('document', models.FileField(upload_to='user_documents/', verbose_name='Upload Document(.pdf)')),
                ('image', models.ImageField(upload_to='user_images/', verbose_name='Upload Image(.jpg/.jpeg)')),
                ('payment', models.BooleanField(verbose_name='Payment')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin_panel.srvc', verbose_name='Service')),
            ],
        ),
    ]
