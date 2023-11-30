from django.shortcuts import render

def home(request):
    return render(request, "pages/home.html", {"title": "My Personal Portfolio"})

def django_website(request):
    return render(request, "pages/django_website.html", {"title": "Here's how I made this website..."})

def guindex_package(request):
    return render(request, "pages/guindex_package.html", {"title": "Gunidex python package"})

def irish_rail_rt(request):
    return render(request, "pages/irish_rail_rt.html", {"title": "Real time tracking of Irish trains"})

def simpsons_ratings(request):
    return render(request, "pages/simpsons_ratings.html", {"title": "Determining the golden age of The Simpsons"})

def guinness_pricing_post(request):
    return render(request, "pages/guinness_pricing_post.html", {"title": "Variation of Guinness print pricing"})

def transport_emissions_scenarios(request):
    return render(request, "pages/transport_emissions_scenarios.html", {"title": "Ireland transport emissions scenarios"})

def about(request):
    return render(request, "pages/about.html", {"title": "About"})

def stat_learning(request):
    return render(request, "pages/statistical_learning.html", {"title": "Solutions to 'An Introduction to Statistical Learning'"})

def abp(request):
    return render(request, "pages/abp_pt_applications.html", {"title": "How long is ABP taking to decide public transport planning applications"})

def last_fm(request):
    return render(request, "pages/last_fm_analysis.html", {"title": "Exploring the last.fm API"})
