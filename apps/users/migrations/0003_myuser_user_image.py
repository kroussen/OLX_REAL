# Generated by Django 4.2.7 on 2023-12-25 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_myuser_options_myuser_avatar_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='user_image',
            field=models.URLField(blank=True, default='https://ростр.рф/assets/img/no-profile.png', null=True),
        ),
    ]
