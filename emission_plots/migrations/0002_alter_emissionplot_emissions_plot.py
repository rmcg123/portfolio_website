# Generated by Django 4.2.6 on 2023-11-23 20:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emission_plots', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emissionplot',
            name='emissions_plot',
            field=models.FileField(upload_to='emission_plots/static/emission_plots/'),
        ),
    ]
