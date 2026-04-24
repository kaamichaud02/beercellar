from django import forms
from .models import Beer, UserBeerNote


class BeerForm(forms.ModelForm):
    class Meta:
        model = Beer
        fields = ["nom", "brasserie", "style", "volume", "degre_alcool", "pays_origine", "photo", "image_url"]
        widgets = {
            "nom": forms.TextInput(attrs={"class": "form-control", "placeholder": "Ex: Duvel"}),
            "brasserie": forms.TextInput(attrs={"class": "form-control", "placeholder": "Ex: Moortgat"}),
            "style": forms.Select(attrs={"class": "form-select"}),
            "volume": forms.TextInput(attrs={"class": "form-control", "placeholder": "Ex: 473 ml"}),
            "degre_alcool": forms.NumberInput(attrs={"class": "form-control", "step": "0.1", "placeholder": "Ex: 5.0"}),
            "pays_origine": forms.TextInput(attrs={"class": "form-control", "placeholder": "Ex: Belgique"}),
            "photo": forms.ClearableFileInput(attrs={
                "class": "form-control",
                "accept": "image/*",
                "capture": "environment",
            }),
            "image_url": forms.URLInput(attrs={"class": "form-control", "placeholder": "URL image automatique"}),
        }


class UserBeerNoteForm(forms.ModelForm):
    class Meta:
        model = UserBeerNote
        fields = ["note", "commentaire"]
        widgets = {
            "note": forms.NumberInput(attrs={"class": "form-control", "min": 1, "max": 5}),
            "commentaire": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Optionnel..."}),
        }
