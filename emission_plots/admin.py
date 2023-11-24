from django.contrib import admin
from emission_plots.models import EmissionPlot

# Register your models here.

class EmissionPlotAdmin(admin.ModelAdmin):
    pass

admin.site.register(EmissionPlot, EmissionPlotAdmin)
