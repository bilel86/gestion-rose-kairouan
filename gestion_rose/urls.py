from django.contrib import admin
from django.urls import path, include
from dashboard.views import dashboard

urlpatterns = [
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
    path('', dashboard, name='dashboard'),
    path('terrain/', include('terrain.urls')),
    path('employes/', include('employes.urls')),
    path('production/', include('production.urls')),
    path('ventes/', include('ventes.urls')),
    path('couts/', include('couts.urls')),
    path('graphiques/', include('dashboard.urls')),
]
