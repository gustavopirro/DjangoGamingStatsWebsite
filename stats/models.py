from django.db import models
from django.shortcuts import get_object_or_404

class Champion(models.Model):
    champion_class = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    talent = models.CharField(max_length=100)
    winrate = models.IntegerField(default=0)
    match_count = models.IntegerField(default=0)
    confidence_interval_plus = models.IntegerField(default=0)
    confidence_interval_minus = models.IntegerField(default=0)
    champion_image = models.ImageField(blank=True, default=None)
    champion_class_image = models.ImageField(blank=True, default=None)

    def formated_name(self):
        name_formated = f'{self.name}'.replace('_', ' ').title()
        return name_formated
    
    def class_lower_case(self):
        class_formated = f'{self.champion_class}'.lower()
        return class_formated

class ChampionMap(models.Model):
    champion = models.ForeignKey(Champion, on_delete=models.CASCADE)
    map_name = models.CharField(max_length=100)
    winrate = models.IntegerField(default=0)
    match_count = models.IntegerField(default=0)
    confidence_interval_plus = models.IntegerField(default=0)
    confidence_interval_minus = models.IntegerField(default=0)

    def map_name_formated(self):
        map_name_formated = f'{self.map_name}'.replace('_', ' ').title()
        return map_name_formated

class ChampionCard(models.Model):
    champion = models.ForeignKey(Champion, on_delete=models.CASCADE)
    talent = models.CharField(max_length=100)
    card = models.CharField(max_length=100)
    card_level = models.CharField(max_length=100)
    winrate = models.IntegerField(default=0)
    match_count = models.IntegerField(default=0)
    confidence_interval_plus = models.IntegerField(default=0)
    confidence_interval_minus = models.IntegerField(default=0)
    
    def formated_name(self):
        name_formated = f'{self.name}'.replace('_', ' ').title()
        return name_formated

    def talent_name_formated(self):
        talent_name_formated = f'{self.talent}'.replace('_', ' ').title()
        return talent_name_formated

    def card_name_formated(self):
        card_name_formated = f'{self.card}'.replace('_', ' ').title()
        return card_name_formated