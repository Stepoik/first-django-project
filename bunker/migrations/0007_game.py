# Generated by Django 3.2.5 on 2021-08-14 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bunker', '0006_alter_players_session'),
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start', models.BooleanField()),
                ('lobby', models.CharField(max_length=255)),
            ],
        ),
    ]
