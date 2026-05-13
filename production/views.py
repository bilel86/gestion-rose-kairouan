from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.db.models import Sum
from .models import Recolte
from terrain.models import Parcelle

def liste(request):
    recoltes = Recolte.objects.all()
    total_kg = recoltes.aggregate(t=Sum('quantite_kg'))['t'] or 0
    return render(request, 'production/liste.html', {'recoltes': recoltes, 'total_kg': total_kg})

def ajouter(request):
    if request.method == 'POST':
        Recolte.objects.create(
            date=request.POST.get('date', timezone.now().date()),
            parcelle_id=request.POST.get('parcelle') or None,
            quantite_kg=request.POST['quantite_kg'],
            qualite=request.POST.get('qualite', 'A'),
            notes=request.POST.get('notes', ''),
        )
        messages.success(request, 'Récolte enregistrée / Harvest logged')
        return redirect('production_liste')
    return render(request, 'production/form.html', {
        'parcelles': Parcelle.objects.all(),
        'qualites': Recolte.QUALITE,
        'today': timezone.now().date()
    })

def supprimer(request, pk):
    get_object_or_404(Recolte, pk=pk).delete()
    messages.success(request, 'Récolte supprimée / Harvest deleted')
    return redirect('production_liste')
