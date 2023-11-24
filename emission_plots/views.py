from django.shortcuts import render
from emission_plots.models import EmissionPlot
from emission_plots.forms import EmissionPlotForm

# Create your views here.
def emissions_page(request):

    context = {}

    if request.method == "POST":
        form = EmissionPlotForm(request.POST)
        if form.is_valid():

            emissions = form.cleaned_data["emissions"]
            sector = form.cleaned_data["sector"]
            plots = EmissionPlot.objects.filter(
                emissions=emissions, sector=sector
            )

    else:
        form = EmissionPlotForm()
        plots = EmissionPlot.objects.filter(emissions="T", sector="O")

    context["form"] = form
    context["plots"] = plots

    return render(request, "emission_plots/emissions_plots.html", context)