# Generated by Django 5.1.1 on 2024-09-21 11:59

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Evenement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100)),
                ('date', models.DateTimeField()),
                ('stock_initial', models.IntegerField()),
                ('stock_restant', models.IntegerField(blank=True, null=True)),
                ('description', models.TextField()),
                ('photo', models.ImageField(blank=True, null=True, upload_to='evenements/')),
                ('a_la_une', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='TypeBillet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=20)),
                ('description', models.TextField()),
                ('quantité_billet', models.IntegerField(default=1)),
                ('prix', models.DecimalField(decimal_places=2, max_digits=5)),
            ],
        ),
        migrations.CreateModel(
            name='Billet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_achat', models.DateTimeField(auto_now_add=True)),
                ('qr_code', models.CharField(max_length=255, unique=True)),
                ('est_valide', models.BooleanField(default=True)),
                ('security_key_billet', models.UUIDField(default=uuid.uuid4, unique=True)),
                ('utilisateur', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('type_billet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.typebillet')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('adresse', models.CharField(max_length=255)),
                ('telephone', models.CharField(max_length=20)),
                ('security_key', models.UUIDField(default=uuid.uuid4, unique=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_reservation', models.DateTimeField(auto_now_add=True)),
                ('billet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.billet')),
                ('evenement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.evenement')),
                ('utilisateur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
