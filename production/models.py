from django.db import models
from terrain.models import Parcelle

class Recolte(models.Model):
    QUALITE = [
        ('A', 'Grade A — Bouquet / Fresh'),
        ('B', 'Grade B — Distillation'),
        ('C', 'Grade C — Pétales séchés / Dried petals'),
    ]
    date = models.DateField()
    parcelle = models.ForeignKey(Parcelle, on_delete=models.SET_NULL, null=True, blank=True)
    quantite_kg = models.DecimalField(max_digits=10, decimal_places=2)
    qualite = models.CharField(max_length=1, choices=QUALITE, default='A')
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.date} — {self.quantite_kg} kg ({self.qualite})"

    class Meta:
        ordering = ['-date']
