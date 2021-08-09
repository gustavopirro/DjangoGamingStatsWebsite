from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from stats.models import Champion, ChampionCard, ChampionMap

import csv, requests as rs
import logging
import ujson

logger = logging.getLogger(__name__)


######### Render Pages #########


def champion_page(request):
    return render(request, 'stats/champion_stats.html') 

def card_page(request):
    return render(request, 'stats/card_stats.html')

def map_page(request):
    return render(request, 'stats/map_stats.html')  



######### Get Stats #########


def get_map_stats(request):
    stats = ChampionMap.objects.all()
    if not stats:
        logger.error('Could not retrieve Champion map data')
    json_data = []
    for i in stats:
        champion_stat = []
        champion_stat.append(i.champion.champion_class.title())
        champion_stat.append(i.champion.formated_name())
        champion_stat.append(i.map_name_formated())
        champion_stat.append(f'{i.winrate}%')
        champion_stat.append(i.match_count)
        json_data.append(champion_stat)
    return JsonResponse({'map_stats':json_data})
 
def get_card_stats(request):
    with open('./card_stats.json', 'r') as f:
        json_data = ujson.load(f)
        if not json_data:
            logger.error('Could not retrieve card stats json data')
    return JsonResponse(json_data)

def get_champion_stats(request):
    stats = Champion.objects.all()
    if not stats:
        logger.error('Could not retrieve Champion data')
    json_data = []
    for i in stats:
        champion_stat = []
        champion_stat.append(i.champion_class.title())
        champion_stat.append(i.formated_name())
        champion_stat.append(f'{i.winrate}%')
        champion_stat.append(i.talent)
        champion_stat.append(i.match_count)
        json_data.append(champion_stat)
    return JsonResponse({'champion_stats':json_data})



######### Create Databases #########


@login_required
def create_winrate_per_champion_db(request):
    if Champion.objects.all():
        Champion.objects.all().delete()
    with open('winrate_all_ranks.csv', newline='') as f:
        reader = csv.reader(f)
        for i in range(3): next(reader)
        data_list = list(reader)
        csvfile = wr_per_champion_data_format(data_list)
    for row in csvfile:
        champion_data = Champion(
        champion_class=row[0],
        name=row[1],
        talent=row[2],
        winrate=row[3],
        match_count=row[4],
        confidence_interval_plus=row[5], 
        confidence_interval_minus=row[6],
        )
        champion_data.champion_image = f'/static/img/{champion_data.name}.jpg'
        champion_data.champion_class_image = f'/static/img/{champion_data.champion_class}.jpg'
        champion_data.save()
    return HttpResponse("Champion database created, run now create_winrate_per_card_db and create_winrate_per_map_db")

@login_required
def create_winrate_per_card_db(request):
    with open('winrate_per_card.csv', newline='') as f:
        reader = csv.reader(f)
        for i in range(1): next(reader)
        data_list = list(reader)
        csvfile = wr_per_card_data_format(data_list)
        
        for row in csvfile:
            if not row[2]:
                continue
            champion_card_stats = ChampionCard(               
                champion=Champion.objects.all().filter(name=row[0]).first(),
                talent = row[1],
                card = row[2],
                card_level = row[3],
                winrate = row[4],
                match_count = row[5],
                confidence_interval_minus = row[6],
                confidence_interval_plus = row[7]
            )
            champion_card_stats.save()
        return HttpResponse("Card database created, run now create_winrate_per_card_db or create_winrate_per_map_db")

@login_required
def create_winrate_per_map_db(request):  
    with open('winrate_per_map.csv', newline='') as f:
        reader = csv.reader(f)
        for i in range(1): next(reader)
        data_list = list(reader)
        csvfile = wr_per_map_data_format(data_list)
        for row in csvfile:
            champion_map_stats = ChampionMap(
                champion=Champion.objects.all().filter(name=row[1]).first(),
                map_name=row[2],
                winrate=row[3],
                match_count=row[4],
                confidence_interval_plus=row[5],
                confidence_interval_minus=row[6],
            )
            champion_map_stats.save()
        return HttpResponse("Map database created, run now create_winrate_per_card_db and create_winrate_per_map_db")            
 
def wr_per_champion_data_format(csv_file):
        for row in csv_file:
            row[0] = row[0].lower()
            row[1] = row[1].lower().replace(' ', '_').replace('\'','')
            row[3] = row[3].replace('%','')
            row[4] = int(row[4].replace(',',''))
            row[5] = row[5].replace('%','')
            row[6] = row[6].replace('%','')
        return csv_file

def wr_per_card_data_format(csv_file):
    for row in csv_file:
        counter = 0
        for i in row:
            row[counter] = i.lower().replace('%', '').replace('\'','').replace(' ','_')
            counter+=1
        row[5] = int(row[5].replace(',',''))
    return csv_file  

def wr_per_map_data_format(csv_file):
    for row in csv_file:
        counter = 0
        for i in row:
            row[counter] = i.lower().replace('%', '').replace('\'','').replace(' ','_')
            counter+=1
        row[4] = int(row[4].replace(',',''))
    return csv_file

@login_required
def request_csv(request):
    csv_url='https://docs.google.com/spreadsheets/u/0/d/1g05xgJnAR0JQXzreEOqG-xV5cd0izx67ZvOTXMZe_Zg/export?format=csv&id=1g05xgJnAR0JQXzreEOqG-xV5cd0izx67ZvOTXMZe_Zg&gid=0'
    res=rs.get(url=csv_url)
    open('winrate_all_ranks.csv', 'wb').write(res.content)

    csv_url = 'https://docs.google.com/spreadsheets/d/1g05xgJnAR0JQXzreEOqG-xV5cd0izx67ZvOTXMZe_Zg/export?format=csv&id=1g05xgJnAR0JQXzreEOqG-xV5cd0izx67ZvOTXMZe_Zg&gid=2124153663'
    res=rs.get(url=csv_url)
    open('winrate_per_map.csv', 'wb').write(res.content)
    
    csv_url = 'https://docs.google.com/spreadsheets/d/1g05xgJnAR0JQXzreEOqG-xV5cd0izx67ZvOTXMZe_Zg/export?format=csv&id=1g05xgJnAR0JQXzreEOqG-xV5cd0izx67ZvOTXMZe_Zg&gid=1567563930'
    res=rs.get(url=csv_url)
    open('winrate_per_card.csv', 'wb').write(res.content)

    return HttpResponse("CSV Imported and saved to database")