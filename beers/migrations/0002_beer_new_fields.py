from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("beers", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="beer",
            name="image_url",
            field=models.URLField(blank=True, default="", verbose_name="URL image (Open Food Facts)"),
        ),
        migrations.AddField(
            model_name="beer",
            name="volume",
            field=models.CharField(blank=True, default="", max_length=50, verbose_name="Volume"),
        ),
        migrations.AddField(
            model_name="beer",
            name="degre_alcool",
            field=models.DecimalField(blank=True, decimal_places=1, max_digits=4, null=True, verbose_name="Degré d'alcool (%)"),
        ),
        migrations.AddField(
            model_name="beer",
            name="pays_origine",
            field=models.CharField(blank=True, default="", max_length=100, verbose_name="Pays d'origine"),
        ),
    ]
