from django import forms
from emission_plots.models import EmissionPlot

class EmissionPlotForm(forms.ModelForm):
    """Form to select the emission plot"""

    class Meta:
        model = EmissionPlot
        fields = ["emissions", "sector"]