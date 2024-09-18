# Generated by Django 5.1 on 2024-08-13 12:38

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Hotel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('address', models.TextField()),
                ('description', models.TextField()),
                ('amenities', models.TextField(help_text='Lista de comodidades separadas por vírgula')),
            ],
        ),
        migrations.CreateModel(
            name='Quarto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_quarto', models.CharField(max_length=255)),
                ('preco_por_noite', models.DecimalField(decimal_places=2, max_digits=10)),
                ('foto', models.ImageField(upload_to='fotos_quartos/')),
                ('avaliacao', models.BooleanField(default=True)),
                ('hotel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quartos', to='hotels.hotel')),
            ],
        ),
        migrations.CreateModel(
            name='Reserva',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('check_in', models.DateField()),
                ('check_out', models.DateField()),
                ('criacao', models.DateTimeField(auto_now_add=True)),
                ('quarto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reservas', to='hotels.quarto')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]