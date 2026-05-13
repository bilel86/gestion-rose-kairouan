from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Parcelle

def liste(request):
    parcelles = Parcelle.objects.all()
    total_ha = sum(float(p.superficie_ha) for p in parcelles)
    return render(request, 'terrain/liste.html', {'parcelles': parcelles, 'total_ha': total_ha})

def ajouter(request):
    if request.method == 'POST':
        Parcelle.objects.create(
            nom=request.POST['nom'],
            superficie_ha=request.POST['superficie_ha'],
            nb_pieds=request.POST.get('nb_pieds', 0),
            date_plantation=request.POST['date_plantation'],
            statut=request.POST.get('statut', 'active'),
            notes=request.POST.get('notes', ''),
        )
        messages.success(request, 'Parcelle ajoutée / Parcel added')
        return redirect('terrain_liste')
    return render(request, 'terrain/form.html', {'statuts': Parcelle.STATUT})

def modifier(request, pk):
    p = get_object_or_404(Parcelle, pk=pk)
    if request.method == 'POST':
        p.nom = request.POST['nom']
        p.superficie_ha = request.POST['superficie_ha']
        p.nb_pieds = request.POST.get('nb_pieds', 0)
        p.date_plantation = request.POST['date_plantation']
        p.statut = request.POST.get('statut', 'active')
        p.notes = request.POST.get('notes', '')
        p.save()
        messages.success(request, 'Parcelle modifiée / Parcel updated')
        return redirect('terrain_liste')
    return render(request, 'terrain/form.html', {'parcelle': p, 'statuts': Parcelle.STATUT})

def supprimer(request, pk):
    get_object_or_404(Parcelle, pk=pk).delete()
    messages.success(request, 'Parcelle supprimée / Parcel deleted')
    return redirect('terrain_liste')
