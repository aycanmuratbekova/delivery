# Generated by Django 4.1.5 on 2023-01-21 22:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='establishment',
            name='name',
            field=models.CharField(max_length=30, unique=True, verbose_name='Название Карточки'),
        ),
    ]