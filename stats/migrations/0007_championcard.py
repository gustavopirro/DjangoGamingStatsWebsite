# Generated by Django 3.2.5 on 2021-07-18 03:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0006_championmap_confidence_interval_minus'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChampionCard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('talent', models.CharField(max_length=100)),
                ('card', models.CharField(max_length=100)),
                ('card_level', models.CharField(max_length=100)),
                ('winrate', models.IntegerField(default=0)),
                ('match_count', models.IntegerField(default=0)),
                ('confidence_interval_plus', models.IntegerField(default=0)),
                ('confidence_interval_minus', models.IntegerField(default=0)),
                ('champion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stats.champion')),
            ],
        ),
    ]
