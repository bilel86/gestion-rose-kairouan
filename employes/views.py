from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.db.models import Sum
from .models import Employe, Presence

def liste(request):
    employes = Employe.objects.filter(actif=True)
    return render(request, 'employes/liste.html', {'employes': employes})

def ajouter(request):
    if request.method == 'POST':
        Employe.objects.create(
            nom=request.POST['nom'],
            prenom=request.POST['prenom'],
            cin=request.POST.get('cin', ''),
            telephone=request.POST.get('telephone', ''),
            village=request.POST.get('village', ''),
            tarif_jour=request.POST.get('tarif_jour', 30),
        )
        messages.success(request, 'Employé ajouté / Worker added')
        return redirect('employes_liste')
    return render(request, 'employes/form.html')

def modifier(request, pk):
    e = get_object_or_404(Employe, pk=pk)
    if request.method == 'POST':
        e.nom = request.POST['nom']
        e.prenom = request.POST['prenom']
        e.cin = request.POST.get('cin', '')
        e.telephone = request.POST.get('telephone', '')
        e.village = request.POST.get('village', '')
        e.tarif_jour = request.POST.get('tarif_jour', 30)
        e.save()
        messages.success(request, 'Employé modifié / Worker updated')
        return redirect('employes_liste')
    return render(request, 'employes/form.html', {'employe': e})

def pointage(request):
    today = timezone.now().date()
    employes = Employe.objects.filter(actif=True)
    if request.method == 'POST':
        for e in employes:
            present = request.POST.get(f'present_{e.id}') == 'on'
            avance = request.POST.get(f'avance_{e.id}', 0) or 0
            Presence.objects.update_or_create(
                employe=e, date=today,
                defaults={'present': present, 'avance': avance}
            )
        messages.success(request, 'Pointage enregistré / Check-in saved')
        return redirect('employes_pointage')
    presences_qs = Presence.objects.filter(date=today)
    presences_ids = set(presences_qs.values_list('employe_id', flat=True))
    avances_map = {p.employe_id: p.avance for p in presences_qs}
    return render(request, 'employes/pointage.html', {
        'employes': employes,
        'presences_ids': presences_ids,
        'avances_map': avances_map,
        'today': today,
    })

def salaires(request):
    employes = Employe.objects.filter(actif=True)
    mois = request.GET.get('mois', timezone.now().strftime('%Y-%m'))
    annee, m = mois.split('-')
    data = []
    for e in employes:
        presences = Presence.objects.filter(employe=e, date__year=annee, date__month=m, present=True)
        jours = presences.count()
        avances = presences.aggregate(t=Sum('avance'))['t'] or 0
        brut = jours * float(e.tarif_jour)
        data.append({'employe': e, 'jours': jours, 'brut': brut,
                     'avances': float(avances), 'net': brut - float(avances)})
    return render(request, 'employes/salaires.html', {'data': data, 'mois': mois})
