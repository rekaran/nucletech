# Generated by Django 2.2.1 on 2019-06-13 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('builder', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='user_limit',
            field=models.BooleanField(default=True, verbose_name='User Limit'),
        ),
        migrations.AlterField(
            model_name='project',
            name='wss',
            field=models.BooleanField(default=False, verbose_name='WSS'),
        ),
    ]
