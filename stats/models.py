from django.db import models

# Create your models here.
class Champion(models.Model):
    champion_class = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    talent = models.CharField(max_length=200)
    winrate = models.IntegerField(default=0)
    match_count = models.IntegerField(default=0)
    confidence_interval_plus = models.IntegerField(default=0)
    confidence_interval_minus = models.IntegerField(default=0)

class ChampionImage(models.Model):
    champion_name = models.ForeignKey('stats.Champion', on_delete=models.CASCADE, related_name="champion_image")
    image_url = models.CharField(max_length=300)