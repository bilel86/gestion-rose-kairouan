from django.urls import path
from . import views
urlpatterns = [
    path('', views.liste, name='employes_liste'),
    path('ajouter/', views.ajouter, name='employes_ajouter'),
    path('pointage/', views.pointage, name='employes_pointage'),
    path('salaires/', views.salaires, name='employes_salaires'),
    path('<int:pk>/modifier/', views.modifier, name='employes_modifier'),
]
