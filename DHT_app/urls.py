from django.urls import path
from . import views, api, alerts, verifyDhtValues


urlpatterns = [

    path("api/", api.dhtser, name='json'),
    path("", views.table, name="HOME"),
    path("index/", views.index_view, name="index"),
    path("graphique/", views.graphique, name="graphique"),
    path("download_csv/", views.download_csv, name="download_csv"),
    path("data_json/", views.chart_data, name="data_json"),
    path("data_jour_json/", views.chart_data_jour, name="data_jour_json"),
    path("data_heure_json/", views.chart_data_heure, name="data_semaine_json"),
    path("data_mois_json/", views.chart_data_mois, name="data_mois_json"),
    path('recieve_data/', views.receive_data, name='receive_data'),
    path('about/', views.about_view, name = 'about page'),
    path('notifications/', views.notifications_view, name = 'notifications'),

]
