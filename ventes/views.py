from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from .models import Vente

def liste(request):
    ventes = Vente.objects.all()
    ca_total = sum(v.ca_total for v in ventes)
    return render(request, 'ventes/liste.html', {'ventes': ventes, 'ca_total': ca_total})

def ajouter(request):
    if request.method == 'POST':
        Vente.objects.create(
            date=request.POST.get('date', timezone.now().date()),
            quantite_kg=request.POST['quantite_kg'],
            prix_kg=request.POST['prix_kg'],
            acheteur=request.POST.get('acheteur', ''),
            notes=request.POST.get('notes', ''),
        )
        messages.success(request, 'Vente enregistrée / Sale recorded')
        return redirect('ventes_liste')
    return render(request, 'ventes/form.html', {'today': timezone.now().date()})

def supprimer(request, pk):
    get_object_or_404(Vente, pk=pk).delete()
    messages.success(request, 'Vente supprimée / Sale deleted')
    return redirect('ventes_liste')
