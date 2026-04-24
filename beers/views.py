from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.db import models
from django.http import JsonResponse
from .models import Beer, UserBeerNote
from .forms import BeerForm, UserBeerNoteForm


class BeerListView(LoginRequiredMixin, ListView):
    model = Beer
    template_name = "beers/beer_list.html"
    context_object_name = "beers"
    paginate_by = 12

    def get_queryset(self):
        qs = Beer.objects.prefetch_related("notes").all()
        q = self.request.GET.get("q", "").strip()
        if q:
            qs = qs.filter(
                models.Q(nom__icontains=q) |
                models.Q(brasserie__icontains=q) |
                models.Q(code_barre__icontains=q)
            )
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["q"] = self.request.GET.get("q", "")
        user_notes = {
            n.beer_id: n
            for n in UserBeerNote.objects.filter(user=self.request.user)
        }
        ctx["user_notes"] = user_notes
        return ctx


class BeerDetailView(LoginRequiredMixin, DetailView):
    model = Beer
    template_name = "beers/beer_detail.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["note_form"] = UserBeerNoteForm()
        ctx["toutes_notes"] = self.object.notes.select_related("user").all()
        try:
            ctx["ma_note"] = UserBeerNote.objects.get(user=self.request.user, beer=self.object)
        except UserBeerNote.DoesNotExist:
            ctx["ma_note"] = None
        return ctx


class BeerCreateView(LoginRequiredMixin, CreateView):
    model = Beer
    form_class = BeerForm
    template_name = "beers/beer_form.html"
    success_url = reverse_lazy("beer-list")

    def form_valid(self, form):
        form.instance.ajoute_par = self.request.user
        return super().form_valid(form)


class BeerUpdateView(LoginRequiredMixin, UpdateView):
    model = Beer
    form_class = BeerForm
    template_name = "beers/beer_form.html"
    success_url = reverse_lazy("beer-list")


class BeerDeleteView(LoginRequiredMixin, DeleteView):
    model = Beer
    template_name = "beers/beer_confirm_delete.html"
    success_url = reverse_lazy("beer-list")


@login_required
def check_barcode(request):
    code = request.GET.get("code", "").strip()
    if not code:
        return JsonResponse({"found": False})
    try:
        beer = Beer.objects.get(code_barre=code)
        return JsonResponse({"found": True, "pk": beer.pk, "nom": beer.nom, "brasserie": beer.brasserie})
    except Beer.DoesNotExist:
        return JsonResponse({"found": False})


@login_required
def noter_biere(request, pk):
    beer = get_object_or_404(Beer, pk=pk)
    try:
        note_obj = UserBeerNote.objects.get(user=request.user, beer=beer)
        form = UserBeerNoteForm(request.POST, instance=note_obj)
    except UserBeerNote.DoesNotExist:
        form = UserBeerNoteForm(request.POST)
    if form.is_valid():
        note = form.save(commit=False)
        note.user = request.user
        note.beer = beer
        note.save()
        messages.success(request, "Note enregistrée !")
    return redirect("beer-detail", pk=pk)


@login_required
def supprimer_note(request, pk):
    beer = get_object_or_404(Beer, pk=pk)
    UserBeerNote.objects.filter(user=request.user, beer=beer).delete()
    messages.success(request, "Note supprimée.")
    return redirect("beer-detail", pk=pk)
