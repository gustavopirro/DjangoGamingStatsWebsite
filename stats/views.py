from stats.models import Champion
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import csv, requests as rs
from django.http import HttpResponse


def get_champion_stats(request, class_filter='All', sort_type='Winrate'):
    stats = Champion.objects.order_by('-winrate')

    if sort_type != 'Winrate':
        stats = Champion.objects.filter().order_by(f'-{sort_type}')

    if class_filter != 'All':
        stats = Champion.objects.filter(champion_class=class_filter).order_by('-winrate')

    return render(request, 'stats/champion_stats.html', {'champion_stats':stats})

def save_data_to_db(csvfile):
    for row in csvfile:
        champion_data = Champion(
        champion_class=row[0],
        name=row[1],
        talent=row[2],
        winrate=row[3],
        match_count=row[4],
        confidence_interval_plus=row[5], 
        confidence_interval_minus=row[6])
        champion_data.save()
        
def data_format():
    with open('winrate_all_ranks.csv', newline='') as f:
        reader = csv.reader(f)
        for i in range(3): next(reader)
        data_list = list(reader)
        for row in data_list:
            row[3] = row[3].replace('%','')
            row[4] = int(row[4].replace(',',''))
            row[5] = row[5].replace('%','')
            row[6] = row[6].replace('%','')
        save_data_to_db(data_list)
    
@login_required
def request_csv(request):
    csv_url='https://docs.google.com/spreadsheets/u/0/d/1g05xgJnAR0JQXzreEOqG-xV5cd0izx67ZvOTXMZe_Zg/export?format=csv&id=1g05xgJnAR0JQXzreEOqG-xV5cd0izx67ZvOTXMZe_Zg&gid=0'
    res=rs.get(url=csv_url)
    open('winrate_all_ranks.csv', 'wb').write(res.content)
    data_format()
    return HttpResponse("CSV Imported and saved to database")