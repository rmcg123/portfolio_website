from django.shortcuts import render

def home(request):
    return render(request, "pages/home.html", {})

def guindex_package(request):
    return render(request, "pages/guindex_package.html", {})

def irish_rail_rt(request):
    return render(request, "pages/irish_rail_rt.html", {})

def simpsons_ratings(request):
    return render(request, "pages/simpsons_ratings.html", {})

def guinness_pricing_post(request):
    return render(request, "pages/guinness_pricing_post.html", {})

def transport_emissions_scenarios(request):
    return render(request, "pages/transport_emissions_scenarios.html", {})


