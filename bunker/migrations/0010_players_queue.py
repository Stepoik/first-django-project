# Generated by Django 3.2.5 on 2021-08-16 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bunker', '0009_auto_20210815_1154'),
    ]

    operations = [
        migrations.AddField(
            model_name='players',
            name='queue',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]