from django.urls import path
from . import views
urlpatterns = [
    path('', views.liste, name='couts_liste'),
    path('ajouter/', views.ajouter, name='couts_ajouter'),
    path('<int:pk>/supprimer/', views.supprimer, name='couts_supprimer'),
]
