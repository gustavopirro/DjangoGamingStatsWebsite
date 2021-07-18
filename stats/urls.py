from os import name
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('requestcsv/',views.request_csv, name='request_csv'),
    path('', views.get_champion_stats, name='get_champion_stats'),
    path('<sort_type>/<class_filter>/', views.get_champion_stats, name='get_champion_stats'),
    path('createchampiondb', views.create_winrate_per_champion_db, name='create_champion_db'),
    path('createmapdb', views.create_winrate_per_map_db, name='create_map_db'),
    path('createcarddb', views.create_winrate_per_card_db, name='create_card_db'),
    path('map/', views.get_map_stats, name='get_map_stats'),
    path('card/', views.get_card_stats, name='get_card_stats'),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)