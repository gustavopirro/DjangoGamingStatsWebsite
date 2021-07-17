from stats.models import Champion
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import csv, requests as rs
from django.http import HttpResponse
from django.core.files import File
def create_dbs(request):
    create_champion_db()
    return HttpResponse("Databases created")

def get_champion_stats(request, class_filter='All', sort_type='Winrate'):
    stats = Champion.objects.order_by('-winrate')

    if sort_type != 'Winrate':
        stats = Champion.objects.filter().order_by(f'-{sort_type}')

    if class_filter != 'All':
        stats = Champion.objects.filter(champion_class=class_filter).order_by('-winrate')

    
    return render(
        request, 'stats/champion_stats.html', 
        {'champion_stats':stats,
         })

def create_champion_db():
    Champion.objects.all().delete()
    with open('winrate_all_ranks.csv', newline='') as f:
        reader = csv.reader(f)
        for i in range(3): next(reader)
        data_list = list(reader)
        csvfile = data_format(data_list)
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
           
def data_format(csv_file):
        for row in csv_file:
            row[0] = row[0].lower()
            row[1] = row[1].lower().replace(' ', '_').replace('\'','_')
            row[3] = row[3].replace('%','')
            row[4] = int(row[4].replace(',',''))
            row[5] = row[5].replace('%','')
            row[6] = row[6].replace('%','')
        return csv_file
    
@login_required
def request_csv():
    csv_url='https://docs.google.com/spreadsheets/u/0/d/1g05xgJnAR0JQXzreEOqG-xV5cd0izx67ZvOTXMZe_Zg/export?format=csv&id=1g05xgJnAR0JQXzreEOqG-xV5cd0izx67ZvOTXMZe_Zg&gid=0'
    res=rs.get(url=csv_url)
    open('winrate_all_ranks.csv', 'wb').write(res.content)
    return HttpResponse("CSV Imported and saved to database")