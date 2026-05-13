from django.db import models

class Employe(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    cin = models.CharField(max_length=20, blank=True)
    telephone = models.CharField(max_length=20, blank=True)
    village = models.CharField(max_length=100, blank=True)
    tarif_jour = models.DecimalField(max_digits=8, decimal_places=2, default=30)
    actif = models.BooleanField(default=True)
    date_embauche = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.prenom} {self.nom}"

    class Meta:
        ordering = ['nom']

class Presence(models.Model):
    employe = models.ForeignKey(Employe, on_delete=models.CASCADE, related_name='presences')
    date = models.DateField()
    present = models.BooleanField(default=True)
    avance = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    notes = models.CharField(max_length=200, blank=True)

    class Meta:
        unique_together = ['employe', 'date']
        ordering = ['-date']

    def salaire_jour(self):
        return self.employe.tarif_jour if self.present else 0
