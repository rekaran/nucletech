# Generated by Django 2.2.1 on 2019-06-26 05:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('builder', '0005_auto_20190614_2122'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='bson_key',
            field=models.TextField(blank=True, verbose_name='BSON Key'),
        ),
        migrations.AlterField(
            model_name='project',
            name='retrain_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Retrain Date'),
        ),
    ]
