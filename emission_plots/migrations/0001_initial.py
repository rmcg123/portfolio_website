# Generated by Django 4.2.6 on 2023-11-23 19:52

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EmissionPlot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('emissions', models.CharField(choices=[('T', 'Total'), ('PCp', 'Per Capita'), ('Pct', 'Percentage Share')], max_length=3, verbose_name='Emissions calculation')),
                ('sector', models.CharField(choices=[('O', 'Overall'), ('E', 'Energy'), ('I', 'Industrial'), ('A', 'Agriculture'), ('L', 'LULUCF'), ('W', 'Waste')], max_length=1, verbose_name='Sector emissions are from')),
                ('emissions_plot', models.FileField(upload_to='emission_plots/')),
                ('plot_description', models.TextField()),
            ],
        ),
    ]
