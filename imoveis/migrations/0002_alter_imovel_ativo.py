# Generated by Django 4.2.5 on 2023-09-18 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imoveis', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imovel',
            name='ativo',
            field=models.BooleanField(default=True, editable=False),
        ),
    ]
