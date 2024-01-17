# Generated by Django 5.0.1 on 2024-01-09 08:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0009_userprofile_status_userprofile_taken_by'),
    ]

    operations = [
        migrations.CreateModel(
            name='admcat',
            fields=[
                ('acid', models.AutoField(db_column='acid', primary_key=True, serialize=False, verbose_name='Admin Cat ID')),
                ('acname', models.CharField(max_length=255, unique=True, verbose_name='Admin Cat Name')),
                ('acdescription', models.CharField(max_length=255, verbose_name='Description')),
                ('acisadm', models.IntegerField(verbose_name='admin or user')),
                ('usrid', models.IntegerField(verbose_name='Id of User Created')),
                ('dtupdatd', models.DateTimeField(auto_now_add=True)),
                ('acstatus', models.BooleanField(default=True)),
            ],
        ),
        migrations.AddField(
            model_name='srvc',
            name='svdoccolltime',
            field=models.DecimalField(decimal_places=2, max_digits=5, null=True, verbose_name='Doc Collection Time(hrs)'),
        ),
        migrations.AddField(
            model_name='srvc',
            name='svproctime',
            field=models.DecimalField(decimal_places=2, max_digits=5, null=True, verbose_name='Process request Time(hrs)'),
        ),
        migrations.AddField(
            model_name='srvc',
            name='svprovtime',
            field=models.DecimalField(decimal_places=2, max_digits=5, null=True, verbose_name='Service provider Time(hrs)'),
        ),
        migrations.CreateModel(
            name='admroles',
            fields=[
                ('arid', models.AutoField(db_column='arid', primary_key=True, serialize=False, verbose_name='Admin role ID')),
                ('arsvid', models.IntegerField(verbose_name='Service Id')),
                ('usrid', models.IntegerField(verbose_name='Id of User Created')),
                ('dtupdatd', models.DateTimeField(auto_now_add=True)),
                ('arstatus', models.BooleanField(default=True)),
                ('aracid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin_panel.admcat', verbose_name='Admin Cat')),
            ],
        ),
        migrations.CreateModel(
            name='clnt',
            fields=[
                ('clid', models.AutoField(db_column='clid', primary_key=True, serialize=False, verbose_name='Client Id')),
                ('clcode', models.CharField(max_length=255, unique=True, verbose_name='Client code')),
                ('clname', models.CharField(max_length=255, verbose_name='Client Name')),
                ('clagid', models.IntegerField(verbose_name='Agent ID')),
                ('claddress', models.CharField(max_length=255, verbose_name='Client Address')),
                ('clmobno', models.CharField(max_length=255, verbose_name='Mob No: ')),
                ('clmobvrfd', models.IntegerField(verbose_name='Mobno verified')),
                ('clmobvrfcode', models.CharField(max_length=255, verbose_name='Verification Code')),
                ('clemail', models.CharField(max_length=255, verbose_name='Email')),
                ('clemailvrfd', models.IntegerField(verbose_name='Email Verified')),
                ('clemailvrfcode', models.CharField(max_length=255, verbose_name='Verification Code')),
                ('usrid', models.IntegerField(verbose_name='Id of User Created')),
                ('dtupdatd', models.DateTimeField(auto_now_add=True)),
                ('clstatus', models.BooleanField(default=True)),
                ('clcnid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin_panel.cntry', verbose_name='Country')),
            ],
        ),
        migrations.CreateModel(
            name='clsubsdet',
            fields=[
                ('csid', models.AutoField(db_column='csid', primary_key=True, serialize=False, verbose_name='Client sub ID')),
                ('csslno', models.IntegerField(verbose_name='Sl No')),
                ('cssubsdate', models.DateTimeField(verbose_name='Sub date')),
                ('csvldprd', models.IntegerField(verbose_name='Sub period')),
                ('csvldprdunt', models.IntegerField(verbose_name='Sub unit')),
                ('cssubsexpdate', models.DateTimeField(verbose_name='Sub Expiry Date')),
                ('csrate', models.DecimalField(decimal_places=3, max_digits=18, verbose_name='Govt Rate')),
                ('cssrvchg', models.DecimalField(decimal_places=3, max_digits=18, verbose_name='IVBMCS Ser Charge')),
                ('csdiscrt', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Discount Rate')),
                ('csdiscamt', models.DecimalField(decimal_places=3, max_digits=18, verbose_name='Discount Amt')),
                ('csagrt', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Agent Rate')),
                ('csagamt', models.DecimalField(decimal_places=3, max_digits=18, verbose_name='Agent Amt')),
                ('cstxrt', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Tax Rate')),
                ('cstxamt', models.DecimalField(decimal_places=3, max_digits=18, verbose_name='Tax Amt')),
                ('csnetamt', models.DecimalField(decimal_places=3, max_digits=18, verbose_name='Net Rate')),
                ('usrid', models.IntegerField(verbose_name='Id of User Created')),
                ('dtupdatd', models.DateTimeField(auto_now_add=True)),
                ('csstatus', models.BooleanField(default=True)),
                ('csclid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin_panel.clnt', verbose_name='Client')),
                ('cssvid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin_panel.srvc', verbose_name='Service')),
            ],
        ),
        migrations.CreateModel(
            name='states',
            fields=[
                ('stid', models.AutoField(db_column='stid', primary_key=True, serialize=False, verbose_name='State Id')),
                ('stname', models.CharField(max_length=255, verbose_name='Currency Name')),
                ('stdescription', models.CharField(max_length=255, verbose_name='Description')),
                ('sttxcode', models.CharField(max_length=255, verbose_name='Tax Code')),
                ('usrid', models.IntegerField(verbose_name='Id of User Created')),
                ('dtupdatd', models.DateTimeField(auto_now_add=True)),
                ('cnstatus', models.BooleanField(default=True)),
                ('stcnid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin_panel.cntry', verbose_name='Country')),
            ],
        ),
        migrations.AddField(
            model_name='clnt',
            name='clstid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin_panel.states', verbose_name='States'),
        ),
    ]
