# Generated by Django 5.1 on 2024-09-17 12:55

import django.db.models.deletion
import django.utils.crypto
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CreditCard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('card_number', models.CharField(max_length=16)),
                ('cardholder_name', models.CharField(max_length=100)),
                ('expiration_date', models.DateField()),
                ('cvv', models.CharField(max_length=3)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cartao_credito', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DebitCard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('card_number', models.CharField(max_length=16)),
                ('cardholder_name', models.CharField(max_length=100)),
                ('expiration_date', models.DateField()),
                ('cvv', models.CharField(max_length=3)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cartao_debito', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('method', models.CharField(choices=[('CREDIT_CARD', 'Cartão de Crédito'), ('DEBIT_CARD', 'Cartão de Débito'), ('PIX', 'PIX')], max_length=20)),
                ('status', models.CharField(choices=[('PENDING', 'Pendente'), ('COMPLETED', 'Concluído'), ('FAILED', 'Falhou')], default='PENDING', max_length=10)),
                ('transaction_id', models.CharField(default=django.utils.crypto.get_random_string, max_length=100, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('pix_key', models.CharField(blank=True, max_length=100, null=True)),
                ('credit_card', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='pagamento.creditcard')),
                ('debit_card', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='pagamento.debitcard')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
