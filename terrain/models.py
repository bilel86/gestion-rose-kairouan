from django.db import models
from datetime import date

class Parcelle(models.Model):
    STATUT = [
        ('active', 'En culture / Active'),
        ('repos', 'En repos / Resting'),
        ('traitement', 'En traitement / Treatment'),
        ('renouvellement', 'À renouveler / To renew'),
    ]
    nom = models.CharField(max_length=100)
    superficie_ha = models.DecimalField(max_digits=5, decimal_places=2)
    nb_pieds = models.IntegerField(default=0)
    date_plantation = models.DateField()
    statut = models.CharField(max_length=20, choices=STATUT, default='active')
    notes = models.TextField(blank=True)

    def age_ans(self):
        return (date.today() - self.date_plantation).days // 365

    def __str__(self):
        return f"{self.nom} ({self.superficie_ha} Ha)"

    class Meta:
        ordering = ['nom']
