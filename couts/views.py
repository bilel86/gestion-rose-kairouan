from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.db.models import Sum
from .models import Cout
from terrain.models import Parcelle

def liste(request):
    couts = Cout.objects.all()
    total = couts.aggregate(t=Sum('montant'))['t'] or 0
    par_cat = {}
    for c in couts:
        par_cat[c.categorie] = par_cat.get(c.categorie, 0) + float(c.montant)
    return render(request, 'couts/liste.html', {'couts': couts, 'total': total, 'par_cat': par_cat})

def ajouter(request):
    if request.method == 'POST':
        Cout.objects.create(
            date=request.POST.get('date', timezone.now().date()),
            categorie=request.POST['categorie'],
            description=request.POST['description'],
            montant=request.POST['montant'],
            parcelle_id=request.POST.get('parcelle') or None,
            fournisseur=request.POST.get('fournisseur', ''),
            notes=request.POST.get('notes', ''),
        )
        messages.success(request, 'Charge ajoutée / Cost added')
        return redirect('couts_liste')
    return render(request, 'couts/form.html', {
        'categories': Cout.CATEGORIE,
        'parcelles': Parcelle.objects.all(),
        'today': timezone.now().date()
    })

def supprimer(request, pk):
    get_object_or_404(Cout, pk=pk).delete()
    messages.success(request, 'Charge supprimée / Cost deleted')
    return redirect('couts_liste')
