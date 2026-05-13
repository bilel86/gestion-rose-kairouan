from django.urls import path
from . import views
urlpatterns = [
    path('', views.liste, name='production_liste'),
    path('ajouter/', views.ajouter, name='production_ajouter'),
    path('<int:pk>/supprimer/', views.supprimer, name='production_supprimer'),
]
