# Generated by Django 5.1.3 on 2024-11-24 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('municipio_invest', '0002_concelhos_tamega_e_sousa'),
    ]

    operations = [
        migrations.CreateModel(
            name='District',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
            options={
                'verbose_name': 'District',
                'verbose_name_plural': 'Districts',
            },
        ),
        migrations.CreateModel(
            name='NUTSIII',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
            options={
                'verbose_name': 'NUTS III',
                'verbose_name_plural': 'NUTS III',
            },
        ),
    ]