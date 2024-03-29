# Generated by Django 3.2.5 on 2021-07-13 15:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Champion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('champion_class', models.CharField(max_length=200)),
                ('name', models.CharField(max_length=200)),
                ('talent', models.CharField(max_length=200)),
                ('winrate', models.IntegerField(default=0)),
                ('match_count', models.IntegerField(default=0)),
                ('confidence_interval_plus', models.IntegerField(default=0)),
                ('confidence_interval_minus', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='ChampionImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_url', models.CharField(max_length=300)),
                ('champion_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='champion_image', to='stats.champion')),
            ],
        ),
    ]
