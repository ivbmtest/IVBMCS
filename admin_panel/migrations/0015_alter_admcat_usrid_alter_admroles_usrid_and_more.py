# Generated by Django 5.0.1 on 2024-02-20 04:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0014_customuser_agent_admin_staff_users'),
    ]

    operations = [
        migrations.AlterField(
            model_name='admcat',
            name='usrid',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, to='admin_panel.customuser', verbose_name='Created By'),
        ),
        migrations.AlterField(
            model_name='admroles',
            name='usrid',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, to='admin_panel.customuser', verbose_name='Created By'),
        ),
        migrations.AlterField(
            model_name='agent',
            name='admin',
            field=models.OneToOneField(default=' ', on_delete=django.db.models.deletion.CASCADE, to='admin_panel.customuser'),
        ),
        migrations.AlterField(
            model_name='clnt',
            name='usrid',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, to='admin_panel.customuser', verbose_name='Created By'),
        ),
        migrations.AlterField(
            model_name='clsubsdet',
            name='usrid',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, to='admin_panel.customuser', verbose_name='Created By'),
        ),
        migrations.AlterField(
            model_name='cntry',
            name='usrid',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, to='admin_panel.customuser', verbose_name='Created By'),
        ),
        migrations.AlterField(
            model_name='crnc',
            name='usrid',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, to='admin_panel.customuser', verbose_name='Created By'),
        ),
        migrations.AlterField(
            model_name='ctgry',
            name='usrid',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, to='admin_panel.customuser', verbose_name='Created By'),
        ),
        migrations.AlterField(
            model_name='documentsrequired',
            name='CreatedBy',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, to='admin_panel.customuser', verbose_name='Created By'),
        ),
        migrations.AlterField(
            model_name='formt',
            name='usrid',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, to='admin_panel.customuser', verbose_name='Created By'),
        ),
        migrations.AlterField(
            model_name='srvc',
            name='usrid',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, to='admin_panel.customuser', verbose_name='Created By'),
        ),
        migrations.AlterField(
            model_name='states',
            name='usrid',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, to='admin_panel.customuser', verbose_name='Created By'),
        ),
        migrations.AlterField(
            model_name='txmst',
            name='usrid',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, to='admin_panel.customuser', verbose_name='Created By'),
        ),
    ]
