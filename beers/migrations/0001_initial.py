from django.conf import settings
from django.db import migrations, models
import django.core.validators
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Beer",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("nom", models.CharField(max_length=200, verbose_name="Nom")),
                ("brasserie", models.CharField(max_length=200, verbose_name="Brasserie")),
                ("style", models.CharField(
                    choices=[
                        ("lager", "Lager"), ("pilsner", "Pilsner"), ("blonde", "Blonde"),
                        ("blanche", "Blanche"), ("ipa", "IPA"), ("pale_ale", "Pale Ale"),
                        ("stout", "Stout"), ("porter", "Porter"), ("ambre", "Ambrée"),
                        ("triple", "Triple"), ("double", "Double"), ("saison", "Saison"),
                        ("lambic", "Lambic"), ("autre", "Autre"),
                    ],
                    default="autre", max_length=50, verbose_name="Style",
                )),
                ("photo", models.ImageField(blank=True, null=True, upload_to="beers/%Y/%m/", verbose_name="Photo")),
                ("ajoute_par", models.ForeignKey(
                    null=True, on_delete=django.db.models.deletion.SET_NULL,
                    related_name="beers_ajoutes", to=settings.AUTH_USER_MODEL, verbose_name="Ajouté par",
                )),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={"verbose_name": "Bière", "verbose_name_plural": "Bières", "ordering": ["nom"]},
        ),
        migrations.CreateModel(
            name="UserBeerNote",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("note", models.PositiveSmallIntegerField(
                    validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)],
                    verbose_name="Note (1-5)",
                )),
                ("commentaire", models.TextField(blank=True, verbose_name="Commentaire")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("beer", models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE, related_name="notes",
                    to="beers.beer", verbose_name="Bière",
                )),
                ("user", models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE, related_name="notes",
                    to=settings.AUTH_USER_MODEL, verbose_name="Utilisateur",
                )),
            ],
            options={"verbose_name": "Note", "verbose_name_plural": "Notes", "unique_together": {("user", "beer")}},
        ),
    ]
