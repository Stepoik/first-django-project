# Generated by Django 3.2.5 on 2021-07-19 15:29

import django.contrib.sessions.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Alias',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('root', models.CharField(max_length=5)),
                ('lobby', models.CharField(max_length=7)),
                ('team', models.CharField(max_length=7)),
                ('session', models.CharField(db_column='session_key', max_length=100, verbose_name=django.contrib.sessions.models.Session)),
                ('ready', models.CharField(max_length=5)),
            ],
        ),
        migrations.CreateModel(
            name='Games',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lobby', models.CharField(max_length=7)),
                ('start', models.CharField(max_length=5)),
                ('queue', models.IntegerField()),
                ('round', models.CharField(max_length=5)),
                ('roundend', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Teams',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Team', models.CharField(max_length=7)),
                ('lobby', models.CharField(max_length=7)),
                ('score', models.IntegerField()),
                ('player_quest', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Words',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word', models.CharField(max_length=50)),
                ('lobby', models.CharField(max_length=7)),
            ],
        ),
    ]