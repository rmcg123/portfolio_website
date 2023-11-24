from django.db import models


class EmissionPlot(models.Model):
    """Model class for the emissions plots of the 2022 EEA emissions data."""

    # Available choices for emissions calculations.
    emission_choices = [
        ("T", "Total"),
        ("PCp", "Per Capita"),
        ("Pct", "Percentage Share")
    ]

    # Available choices for the sector the emissions come from.
    sector_choices = [
        ("O", "Overall"),
        ("E", "Energy"),
        ("I", "Industrial"),
        ("A", "Agriculture"),
        ("L", "LULUCF"),
        ("W", "Waste")
    ]

    # Emissions calculation model field.
    emissions = models.CharField(
        "Emissions calculation", max_length=3, choices=emission_choices
    )

    # Sector model field.
    sector = models.CharField(
        "Sector emissions are from", max_length=1, choices=sector_choices
    )

    # Image of corresponding plot.
    emissions_plot = models.FileField(upload_to="emission_plots/static/emission_plots/")

    # Description of plot.
    plot_description = models.TextField()



