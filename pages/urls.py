from django.urls import path
from django.views.generic import TemplateView
from pages import views

urlpatterns = [
    path("", views.home, name='home'),
    path("django_website/", views.django_website, name="django_website"),
    path("guindex_package/", views.guindex_package, name="guindex_package"),
    path("simpsons_ratings/", views.simpsons_ratings, name="simpsons_ratings"),
    path("irish_rail_rt/", views.irish_rail_rt, name="irish_rail_rt"),
    path("example_map/", TemplateView.as_view(
        template_name="pages/example_map.html"), name='example_map'),
    path("guinness_pricing_post/", views.guinness_pricing_post, name="guinness_pricing_post"),
    path("transport_emissions_scenarios/", views.transport_emissions_scenarios, name="transport_emissions_scenarios"),
    path("statistical_learning/", views.stat_learning, name="statistical_learning"),
    path("abp_pt_applications/", views.abp, name="abp_pt_applications"),
    path("about/", views.about, name="about"),
    path("last_fm_analysis/", views.last_fm, name="last_fm_analysis"),
    path("guindex_map/", views.guindex_maps, name="guindex_map"),
    path("eirgrid_analysis/", views.eirgrid_analysis, name="eirgrid_analysis"),
]
