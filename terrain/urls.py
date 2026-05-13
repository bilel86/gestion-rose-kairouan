from django.urls import path
from . import views
urlpatterns = [
    path('', views.liste, name='terrain_liste'),
    path('ajouter/', views.ajouter, name='terrain_ajouter'),
    path('<int:pk>/modifier/', views.modifier, name='terrain_modifier'),
    path('<int:pk>/supprimer/', views.supprimer, name='terrain_supprimer'),
]
