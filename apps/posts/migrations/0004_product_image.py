# Generated by Django 4.2.7 on 2023-12-15 20:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_alter_product_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, upload_to='', verbose_name='Фотография'),
        ),
    ]
