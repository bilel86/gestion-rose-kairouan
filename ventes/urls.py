from django.urls import path
from . import views
urlpatterns = [
    path('', views.liste, name='ventes_liste'),
    path('ajouter/', views.ajouter, name='ventes_ajouter'),
    path('<int:pk>/supprimer/', views.supprimer, name='ventes_supprimer'),
]
