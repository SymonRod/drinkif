# Generated by Django 3.2.6 on 2022-01-17 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drinkif', '0008_auto_20220112_0844'),
    ]

    operations = [
        migrations.AddField(
            model_name='extendeduser',
            name='is_developer',
            field=models.BooleanField(default=False),
        ),
    ]