from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('upload/', views.upload_file, name='upload_file'),
    path('files/', views.file_list, name='file_list'),
    path('chart-data/', views.chart_data, name='chart_data'),
    path('ask-ai/', views.ask_ai, name='ask_ai'),
]