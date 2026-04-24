from django.urls import path
from . import views

urlpatterns = [
    path("", views.BeerListView.as_view(), name="beer-list"),
    path("add/", views.BeerCreateView.as_view(), name="beer-add"),
    path("<int:pk>/", views.BeerDetailView.as_view(), name="beer-detail"),
    path("<int:pk>/edit/", views.BeerUpdateView.as_view(), name="beer-edit"),
    path("<int:pk>/delete/", views.BeerDeleteView.as_view(), name="beer-delete"),
    path("<int:pk>/noter/", views.noter_biere, name="beer-noter"),
    path("<int:pk>/supprimer-note/", views.supprimer_note, name="beer-supprimer-note"),
]
