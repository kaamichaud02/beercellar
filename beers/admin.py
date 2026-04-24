from django.contrib import admin
from .models import Beer, UserBeerNote


@admin.register(Beer)
class BeerAdmin(admin.ModelAdmin):
    list_display = ["nom", "brasserie", "style", "note_moyenne", "ajoute_par", "created_at"]
    list_filter = ["style"]
    search_fields = ["nom", "brasserie"]
    readonly_fields = ["created_at", "updated_at"]


@admin.register(UserBeerNote)
class UserBeerNoteAdmin(admin.ModelAdmin):
    list_display = ["user", "beer", "note", "created_at"]
    list_filter = ["note"]
    search_fields = ["user__email", "beer__nom"]
