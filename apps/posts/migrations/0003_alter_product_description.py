# Generated by Django 4.2.7 on 2023-12-15 08:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.TextField(max_length=255, verbose_name='Описание'),
        ),
    ]