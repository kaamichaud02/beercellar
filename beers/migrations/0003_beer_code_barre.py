from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("beers", "0002_beer_new_fields"),
    ]

    operations = [
        migrations.AddField(
            model_name="beer",
            name="code_barre",
            field=models.CharField(blank=True, default="", max_length=50, verbose_name="Code-barres"),
        ),
    ]
