from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()


class Beer(models.Model):
    STYLE_CHOICES = [
        ("lager", "Lager"),
        ("pilsner", "Pilsner"),
        ("blonde", "Blonde"),
        ("blanche", "Blanche"),
        ("ipa", "IPA"),
        ("pale_ale", "Pale Ale"),
        ("stout", "Stout"),
        ("porter", "Porter"),
        ("ambre", "Ambrée"),
        ("triple", "Triple"),
        ("double", "Double"),
        ("saison", "Saison"),
        ("lambic", "Lambic"),
        ("autre", "Autre"),
    ]

    nom = models.CharField(max_length=200, verbose_name="Nom")
    brasserie = models.CharField(max_length=200, verbose_name="Brasserie")
    style = models.CharField(
        max_length=50,
        choices=STYLE_CHOICES,
        default="autre",
        verbose_name="Style",
    )
    photo = models.ImageField(
        upload_to="beers/%Y/%m/",
        blank=True,
        null=True,
        verbose_name="Photo",
    )
    ajoute_par = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="beers_ajoutes",
        verbose_name="Ajouté par",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["nom"]
        verbose_name = "Bière"
        verbose_name_plural = "Bières"

    def __str__(self):
        return f"{self.nom} — {self.brasserie}"

    def note_moyenne(self):
        notes = self.notes.all()
        if not notes:
            return None
        return round(sum(n.note for n in notes) / len(notes), 1)


class UserBeerNote(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="notes",
        verbose_name="Utilisateur",
    )
    beer = models.ForeignKey(
        Beer,
        on_delete=models.CASCADE,
        related_name="notes",
        verbose_name="Bière",
    )
    note = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="Note (1-5)",
    )
    commentaire = models.TextField(blank=True, verbose_name="Commentaire")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("user", "beer")
        verbose_name = "Note"
        verbose_name_plural = "Notes"

    def __str__(self):
        return f"{self.user} → {self.beer} : {self.note}/5"
