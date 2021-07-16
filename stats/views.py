from stats.models import Champion, ChampionClassImage, ChampionImage
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
import csv, requests as rs
from django.http import HttpResponse


def get_champion_stats(request, class_filter='All', sort_type='Winrate'):
    stats = Champion.objects.order_by('-winrate')

    if sort_type != 'Winrate':
        stats = Champion.objects.filter().order_by(f'-{sort_type}')

    if class_filter != 'All':
        stats = Champion.objects.filter(champion_class=class_filter).order_by('-winrate')

    classes_img = ChampionClassImage.objects.all()
    champions_img = ChampionImage.objects.all()
    
    return render(
        request, 'stats/champion_stats.html', 
        {'champion_stats':stats, 'champions_img_url':champions_img,
         'champion_classes_url': classes_img,
         })

def create_databases():
    create_champion_db()
    create_champion_image_db()
    create_class_db()

def create_champion_image_db():
    champion_query = Champion.objects.all()
    champion_dict = {}

    for champion in champion_query:
        champion_dict[champion.name] = champion.name

    for champion in champion_dict:
        champion_image = ChampionImage(champion_name=champion, image_url=f'../../static/img/{champion}.jpg')
        champion_image.save()
        
def create_class_db():
    damage = ChampionClassImage(champion_class_name='Damage', image_url='../../static/img/damage.jpg')
    damage.save()

    support = ChampionClassImage(champion_class_name='Support', image_url='../../static/img/support.jpg')
    support.save()

    flank = ChampionClassImage(champion_class_name='Flank', image_url='../../static/img/flank.jpg')
    flank.save()

    frontline = ChampionClassImage(champion_class_name='Frontline', image_url='../../static/img/frontline.jpg')
    frontline.save()

def create_champion_db():
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
        confidence_interval_minus=row[6])
        champion_data.save()
           
def data_format(csv_file):
        for row in csv_file:
            row[1] = row[1].lower().replace(' ', '_').replace('\'','_')
            row[3] = row[3].replace('%','')
            row[4] = int(row[4].replace(',',''))
            row[5] = row[5].replace('%','')
            row[6] = row[6].replace('%','')
        return csv_file
    
@login_required
def request_csv(request):
    csv_url='https://docs.google.com/spreadsheets/u/0/d/1g05xgJnAR0JQXzreEOqG-xV5cd0izx67ZvOTXMZe_Zg/export?format=csv&id=1g05xgJnAR0JQXzreEOqG-xV5cd0izx67ZvOTXMZe_Zg&gid=0'
    res=rs.get(url=csv_url)
    open('winrate_all_ranks.csv', 'wb').write(res.content)
    data_format()
    return HttpResponse("CSV Imported and saved to database")