# Generated by Django 5.1 on 2024-09-17 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_alter_perfil_birth_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='perfil',
            name='birth_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
