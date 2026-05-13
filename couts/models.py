from django.db import models
from terrain.models import Parcelle

class Cout(models.Model):
    CATEGORIE = [
        ('engrais', 'Engrais / Fertilizer'),
        ('pesticide', 'Pesticide / Medication'),
        ('eau', 'Eau / Water'),
        ('carburant', 'Carburant / Fuel'),
        ('main_oeuvre', "Main d'œuvre / Labor"),
        ('materiel', 'Matériel / Equipment'),
        ('autre', 'Autre / Other'),
    ]
    date = models.DateField()
    categorie = models.CharField(max_length=20, choices=CATEGORIE)
    description = models.CharField(max_length=200)
    montant = models.DecimalField(max_digits=10, decimal_places=3)
    parcelle = models.ForeignKey(Parcelle, on_delete=models.SET_NULL, null=True, blank=True)
    fournisseur = models.CharField(max_length=150, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.date} — {self.get_categorie_display()} : {self.montant} TND"

    class Meta:
        ordering = ['-date']
