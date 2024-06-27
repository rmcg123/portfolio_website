from django.shortcuts import render
import pandas as pd

from abp_applications.models import ABPApplication

# Create your views here.
def abp_pt_applications(request):

    abp_applications = ABPApplication.objects.all().order_by("-application_time_taken")
    abp_applications_df = pd.DataFrame(list(abp_applications.values()))

    description_text = make_description_text(
        planning_applications_df=abp_applications_df
    )

    context = {
        "title": "How Long is An Bord Pleanála Taking to Decide Public Transport Planning Applications?",
        "applications_description": description_text,
        "applications": abp_applications
    }

    return render(request, "abp_pt_applications/abp_pt_applications.html", context)


def make_description_text(planning_applications_df):
    applications_descriptions = f"""
        So far {planning_applications_df["application_decision_date"].notnull().sum()} of the public transport projects have had their applications decided on. The projects that have had their application decided are {", ".join(planning_applications_df.loc[planning_applications_df['application_decision_date'].notnull(), "application_name"].to_list())}. The decided applications have taken an average
         of {int(planning_applications_df.loc[planning_applications_df['application_decision_date'].notnull(), "application_time_taken"].mean().round(0))} days.  
        The planning application that has been in the system the longest without having a decision reached is the {planning_applications_df.loc[planning_applications_df['application_time_taken'].idxmax(), 'application_name']} which has taken {int(planning_applications_df["application_time_taken"].max())} days so far.""".replace(
        "\n", " ")

    return applications_descriptions
