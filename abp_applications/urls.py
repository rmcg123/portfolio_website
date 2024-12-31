from django.urls import path
from abp_applications import views

urlpatterns = [
    path("", views.abp_pt_applications, name="abp_pt_applications"),
    path("energy/", views.abp_energy_applications, name="abp_energy_applications")
]
