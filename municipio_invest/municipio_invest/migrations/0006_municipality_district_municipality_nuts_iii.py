# Generated by Django 5.1.3 on 2024-11-24 14:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('municipio_invest', '0005_adicionar_distritos'),
    ]

    operations = [
        migrations.AddField(
            model_name='municipality',
            name='district',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='municipio_invest.district'),
        ),
        migrations.AddField(
            model_name='municipality',
            name='nuts_III',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='municipio_invest.nutsiii'),
        ),
    ]
