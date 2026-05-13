from django.shortcuts import render
from django.db.models import Sum
from django.utils import timezone
from ventes.models import Vente
from production.models import Recolte
from couts.models import Cout
from employes.models import Employe
import json

def dashboard(request):
    today = timezone.now().date()
    year = today.year
    ventes_annee = Vente.objects.filter(date__year=year)
    recoltes_annee = Recolte.objects.filter(date__year=year)
    couts_annee = Cout.objects.filter(date__year=year)
    ca_total = sum(v.ca_total for v in ventes_annee)
    charges_total = couts_annee.aggregate(t=Sum('montant'))['t'] or 0
    kg_recoltes = recoltes_annee.aggregate(t=Sum('quantite_kg'))['t'] or 0
    nb_employes = Employe.objects.filter(actif=True).count()
    annees = [year - 2, year - 1, year]
    couleurs = ['#3498db', '#e67e22', '#c0392b']
    mois_labels = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    datasets = []
    for i, a in enumerate(annees):
        data = []
        for m in range(1, 13):
            ca = sum(v.ca_total for v in Vente.objects.filter(date__year=a, date__month=m))
            data.append(round(ca, 2))
        datasets.append({'label': str(a), 'data': data, 'borderColor': couleurs[i],
                         'backgroundColor': couleurs[i] + '33', 'tension': 0.4, 'fill': True})
    prix_ventes = list(Vente.objects.filter(date__year=year).order_by('date').values('date', 'prix_kg'))
    prix_labels = [str(v['date']) for v in prix_ventes]
    prix_data = [float(v['prix_kg']) for v in prix_ventes]
    context = {
        'ca_total': round(ca_total, 2),
        'charges_total': round(float(charges_total), 2),
        'benefice': round(ca_total - float(charges_total), 2),
        'kg_recoltes': round(float(kg_recoltes), 2),
        'nb_employes': nb_employes,
        'annee': year,
        'chart_ca_labels': json.dumps(mois_labels),
        'chart_ca_datasets': json.dumps(datasets),
        'prix_labels': json.dumps(prix_labels),
        'prix_data': json.dumps(prix_data),
    }
    return render(request, 'dashboard/index.html', context)

def graphiques(request):
    year = timezone.now().date().year
    annees = [year - 2, year - 1, year]
    couleurs = ['#3498db', '#e67e22', '#c0392b']
    mois_labels = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    datasets_ca, datasets_kg = [], []
    for i, a in enumerate(annees):
        ca_data, kg_data = [], []
        for m in range(1, 13):
            ca = sum(v.ca_total for v in Vente.objects.filter(date__year=a, date__month=m))
            kg = Recolte.objects.filter(date__year=a, date__month=m).aggregate(t=Sum('quantite_kg'))['t'] or 0
            ca_data.append(round(ca, 2))
            kg_data.append(round(float(kg), 2))
        datasets_ca.append({'label': str(a), 'data': ca_data, 'borderColor': couleurs[i],
                            'backgroundColor': couleurs[i] + '33', 'tension': 0.4})
        datasets_kg.append({'label': str(a), 'data': kg_data, 'borderColor': couleurs[i],
                            'backgroundColor': couleurs[i] + '33', 'tension': 0.4})
    charges_par_cat = {}
    for c in Cout.objects.filter(date__year=year):
        charges_par_cat[c.get_categorie_display()] = charges_par_cat.get(c.get_categorie_display(), 0) + float(c.montant)
    context = {
        'mois_labels': json.dumps(mois_labels),
        'datasets_ca': json.dumps(datasets_ca),
        'datasets_kg': json.dumps(datasets_kg),
        'cat_labels': json.dumps(list(charges_par_cat.keys())),
        'cat_data': json.dumps(list(charges_par_cat.values())),
        'annee': year,
    }
    return render(request, 'dashboard/graphiques.html', context)
