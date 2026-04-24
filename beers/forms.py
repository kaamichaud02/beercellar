from django import forms
from .models import Beer, UserBeerNote


class BeerForm(forms.ModelForm):
    class Meta:
        model = Beer
        fields = ["nom", "brasserie", "style", "photo"]
        widgets = {
            "nom": forms.TextInput(attrs={"class": "form-control", "placeholder": "Ex: Duvel"}),
            "brasserie": forms.TextInput(attrs={"class": "form-control", "placeholder": "Ex: Moortgat"}),
            "style": forms.Select(attrs={"class": "form-select"}),
            "photo": forms.ClearableFileInput(attrs={
                "class": "form-control",
                "accept": "image/*",
                "capture": "environment",  # ouvre la camera arrière sur mobile
            }),
        }


class UserBeerNoteForm(forms.ModelForm):
    class Meta:
        model = UserBeerNote
        fields = ["note", "commentaire"]
        widgets = {
            "note": forms.NumberInput(attrs={"class": "form-control", "min": 1, "max": 5}),
            "commentaire": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Optionnel..."}),
        }
