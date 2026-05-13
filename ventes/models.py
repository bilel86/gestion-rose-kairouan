from django.db import models

class Vente(models.Model):
    date = models.DateField()
    quantite_kg = models.DecimalField(max_digits=10, decimal_places=2)
    prix_kg = models.DecimalField(max_digits=8, decimal_places=3)
    acheteur = models.CharField(max_length=150, blank=True)
    notes = models.TextField(blank=True)

    @property
    def ca_total(self):
        return round(self.quantite_kg * self.prix_kg, 3)

    def __str__(self):
        return f"{self.date} — {self.quantite_kg} kg @ {self.prix_kg} TND"

    class Meta:
        ordering = ['-date']

class PrixJour(models.Model):
    date = models.DateField(unique=True)
    prix_min = models.DecimalField(max_digits=8, decimal_places=3)
    prix_max = models.DecimalField(max_digits=8, decimal_places=3)
    prix_moyen = models.DecimalField(max_digits=8, decimal_places=3)

    def __str__(self):
        return f"{self.date} — moy: {self.prix_moyen} TND/kg"

    class Meta:
        ordering = ['-date']
