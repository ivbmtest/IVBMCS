# Generated by Django 5.0.1 on 2024-02-20 04:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0018_alter_admroles_usrid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='admroles',
            name='aracid',
        ),
        migrations.RemoveField(
            model_name='admroles',
            name='usrid',
        ),
        migrations.DeleteModel(
            name='admcat',
        ),
        migrations.DeleteModel(
            name='admroles',
        ),
    ]

# Generated by Django 5.0.1 on 2024-02-21 05:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0018_alter_admcat_usrid_alter_admroles_usrid_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='admroles',
            name='aracid',
        ),
        migrations.RemoveField(
            model_name='admroles',
            name='usrid',
        ),
        migrations.DeleteModel(
            name='admcat',
        ),
        migrations.DeleteModel(
            name='admroles',
        ),
    ]
