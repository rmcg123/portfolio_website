from django.urls import path
from emission_plots import views


urlpatterns = [
    path("", views.emissions_page, name="eu_emissions"),
]
