# Generated by Django 5.0.1 on 2024-03-19 08:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0008_alter_admin_id_alter_agent_id_alter_customuser_id_and_more'),
        ('user_portal', '0010_alter_user_service_details_call_back_request_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_service_details',
            name='taken_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='admin_panel.staff', verbose_name='Taken'),
        ),
    ]
