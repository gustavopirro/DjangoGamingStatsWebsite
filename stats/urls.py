from os import name
from django.urls import path
from . import views

urlpatterns = [
    path('requestcsv/',views.request_csv, name='request_csv'),
    path('', views.get_champion_stats, name='get_champion_stats'),
    path('<sort_type>/<class_filter>/', views.get_champion_stats, name='get_champion_stats'),
    path('create_db', views.create_databases, name='create_db')
    
]