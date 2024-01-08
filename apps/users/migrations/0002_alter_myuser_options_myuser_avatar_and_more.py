# Generated by Django 4.2.7 on 2023-12-21 20:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='myuser',
            options={},
        ),
        migrations.AddField(
            model_name='myuser',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='avatars/'),
        ),
        migrations.DeleteModel(
            name='Transaction',
        ),
    ]
