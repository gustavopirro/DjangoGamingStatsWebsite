from os import name
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('requestcsv/',views.request_csv, name='request_csv'),
    path('', views.champion_page, name='get_champion_page'),
    path('<sort_type>/<class_filter>/', views.get_champion_stats, name='get_champion_stats'),
    path('createchampiondb', views.create_winrate_per_champion_db, name='create_champion_db'),
    path('createmapdb', views.create_winrate_per_map_db, name='create_map_db'),
    path('createcarddb', views.create_winrate_per_card_db, name='create_card_db'),
    path('map/', views.map_page, name='get_map_page'),
    path('card/', views.card_page, name='get_card_page'),
    path('card/', views.get_card_stats, name='get_card_stats'),
    path('mapajax/', views.get_map_stats, name='get_map_stats'),
    path('championajax/', views.get_champion_stats, name='get_champion_stats'),
    path('cardajax/', views.get_card_stats, name='get_card_stats'),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)