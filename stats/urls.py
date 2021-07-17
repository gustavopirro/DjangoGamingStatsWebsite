from os import name
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('requestcsv/',views.request_csv, name='request_csv'),
    path('', views.get_champion_stats, name='get_champion_stats'),
    path('<sort_type>/<class_filter>/', views.get_champion_stats, name='get_champion_stats'),
    path('createdb', views.create_dbs, name='create_dbs')
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)