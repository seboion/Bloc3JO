# Generated by Django 5.1.1 on 2024-09-19 13:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_alter_billet_evenement'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='billet',
            name='evenement',
        ),
    ]
