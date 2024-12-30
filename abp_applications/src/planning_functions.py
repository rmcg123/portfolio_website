"""Functions to facilitate the transport planning analysis."""
import datetime as dt
from textwrap import wrap

import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from abp_applications.models import ABPApplication


def planning_request(application_url):
    """A function to send a request to the An Bord Pleanala planning
    application page of a specified project and to extract the information from
    the respsonse into a DataFrame."""

    # Send HTTP request.
    req = requests.get(application_url)

    # Parse the returned HTML.
    planning_soup = BeautifulSoup(req.content, "html.parser")

    # Find all divs that contain desired information.
    content_divs = planning_soup.find_all("div", "grid-x grid-padding-x")
    content_divs = [
        x
        for x in content_divs
        if (x.find("div", "medium-3 cell") and x.find("div", "medium-9 cell"))
    ]

    # Loop over divs and extract information from each.
    planning_app_df = pd.DataFrame()
    skip_idxs = []
    for idx, content_div in enumerate(content_divs):
        if idx in skip_idxs:
            continue

        try:
            column = (
                content_div.find("div", "medium-3 cell")
                .text.strip("\n")
                .strip(" ")
            )

            if column != "Documents" and not column.startswith("\r"):
                if column == "History":
                    history_details = content_div.find_all(
                        "div", "grid-x grid-padding-x"
                    )
                    for jdx, history_detail in enumerate(history_details):
                        skip_idxs.append(idx + (jdx + 1))
                        column = (
                            history_detail.find("div", "medium-9 cell")
                            .text.strip("\n")
                            .strip(" ")
                        )
                        value = (
                            history_detail.find("div", "medium-3 cell")
                            .text.strip("\n")
                            .strip(" ")
                        )
                        planning_app_df[column] = [value]
                else:
                    value = (
                        content_div.find("div", "medium-9 cell")
                        .text.strip("\n")
                        .strip(" ")
                    )
                    planning_app_df[column] = [value]

        except AttributeError:
            continue

    return planning_app_df


def clean_planning_columns(planning_apps_df, acronym_replacements):
    """Function to return the retrieved project information."""

    # Make column names snake_case.
    planning_apps_df.columns = (
        planning_apps_df.columns.str.replace("   ", " ")
        .str.replace(" ", "_")
        .str.lower()
    )

    # Correctly format Boolean columns.
    for bool_col in ["eiar", "nis"]:
        planning_apps_df[bool_col] = planning_apps_df[bool_col].astype(bool)

    # Correctly format date columns.
    for date_col in ["lodged", "make_railway_order_w_cons", "date_signed"]:
        planning_apps_df[date_col] = planning_apps_df[date_col].str.strip(
            "\r\n"
        )
        planning_apps_df[date_col] = pd.to_datetime(
            planning_apps_df[date_col], format="%d/%m/%Y"
        )

    # Clean up applicant column.
    planning_apps_df["parties"] = planning_apps_df["parties"].str.strip(
        "\r\n ~"
    )

    # Calculate time taken to decision or to date.
    planning_apps_df["time_taken"] = np.where(
        planning_apps_df["date_signed"].isna(),
        (dt.datetime.today() - planning_apps_df["lodged"]).dt.days,
        (planning_apps_df["date_signed"] - planning_apps_df["lodged"]).dt.days,
    )

    # Replace acronyms with full project names.
    planning_apps_df["project_name"] = planning_apps_df["short_name"].copy()
    for acronym, replacement in acronym_replacements.items():
        planning_apps_df["project_name"] = planning_apps_df[
            "project_name"
        ].str.replace(acronym, replacement)

    planning_apps_df["description"] = planning_apps_df[
        "description"
    ].str.lower()
    planning_apps_df["project_name"] = np.where(
        planning_apps_df["project_name"].str.startswith("Dublin CBC"),
        planning_apps_df["project_name"]
        + ": "
        + (
            planning_apps_df["description"]
            .str.replace(" core", "")
            .str.replace("bus", "")
            .str.replace("connects ", "")
            .str.replace("connect", "")
            .str.replace("corridor", "")
            .str.replace("scheme", "")
            .str.replace(".", "")
            .str.strip()
        ).str.title(),
        planning_apps_df["project_name"],
    )
    planning_apps_df["project_name"] = np.where(
        planning_apps_df["project_name"].apply(lambda x: len(x)).gt(50),
        planning_apps_df["project_name"].str.wrap(
            width=50, break_long_words=False
        ),
        planning_apps_df["project_name"],
    )

    # Sort from longest to shortest taken.
    planning_apps_df.sort_values(
        by="time_taken", ascending=False, inplace=True
    )

    return planning_apps_df


def plot_time_taken(planning_apps_df, save_dir, save_name, kind="transport"):
    """Function to create a barplot showing the time taken by ABP for each of
    the public transport projects."""

    fig, ax = plt.subplots()

    if kind == "transport":
        planning_apps_df = planning_apps_df.loc[
            planning_apps_df["infrastructure_type"].ne("Offshore Wind")
        ].reset_index(drop=True)
        title = "Days Taken So Far by An Bord Pleanála on Public Transport Projects"
    else:
        planning_apps_df = planning_apps_df.loc[
            planning_apps_df["infrastructure_type"].eq("Offshore Wind")
        ].reset_index(drop=True)
        planning_apps_df["infrastructure_type"] = pd.Categorical(
            planning_apps_df["infrastructure_type"],
            ordered=False,
            categories=["Offshore Wind", "Onshore Wind", "Solar", "Batteries"],
        )
        title = (
            "Days Taken So Far by An Bord Pleanála on Offshore Wind Projects"
        )

    # Create plot.
    sns.barplot(
        data=planning_apps_df,
        x="time_taken",
        y="project_name",
        hue="infrastructure_type",
    )

    # Set plot labels and title.
    ax.set_xlabel("Days Taken So Far")
    ax.set_ylabel("Project")
    ax.set_title(title)

    # Change the patterning of the bars for any projects where a decision has
    # been reached.
    if kind != "Offshore Wind":
        bar_patches = ax.patches[:-2]
    else:
        bar_patches = ax.patches[:-4]
    patch_sorted_df = planning_apps_df.sort_values(
        by=["infrastructure_type", "time_taken"],
        ascending=False,
    ).reset_index(drop=True)
    for idx, bar_patch in enumerate(bar_patches):
        if pd.notna(patch_sorted_df.loc[idx, "date_signed"]):
            bar_patch.set_hatch("/")

    # Reformat hue legend.
    handles, labels = ax.get_legend_handles_labels()
    inf_legend = ax.legend(
        handles,
        labels,
        title="Infrastructure",
    )
    ax.add_artist(inf_legend)

    # Create decision status legend.
    if len(handles) > 2:
        status_handles = handles[:2]
        bbox_bottom = 0.15 + 0.075 * (len(handles) - 2)
    elif len(handles) == 2:
        status_handles = handles
        bbox_bottom = 0.15
    else:
        status_handles = [handles[0], handles[0]]
        bbox_bottom = 0.1
    [x.set_facecolor("white") for x in status_handles]
    [x.set_edgecolor("black") for x in status_handles]
    status_handles[1].set_hatch("/")
    status_legend = ax.legend(
        handles=status_handles,
        labels=["Ongoing", "Decided"],
        title="Decision Status",
        loc="lower right",
        bbox_to_anchor=(1.0, bbox_bottom),
    )
    ax.add_artist(status_legend)

    # Annotate to indicate when the plot was produced.
    ax.annotate(
        f"Accurate as of {dt.datetime.today().strftime('%Y-%m-%d %H:%M')}",
        xy=(0.05, 0.01),
        xycoords="figure fraction",
        fontsize=14,
    )

    number_of_vlines = int(
        round(planning_apps_df["time_taken"].max().squeeze() // (18 * 7), 0)
    )
    for i in range(1, number_of_vlines + 1):
        plt.axvline(
            x=i * (18 * 7), ls="--", color="lightgray", lw=0.75, alpha=0.85
        )

    # Save plot.
    fig.tight_layout()
    fig.savefig(save_dir + save_name)
    plt.close()

    return fig, ax


def save_applications_to_db(planning_applications_df):
    db_applications = ABPApplication.objects.all()
    db_application_ids = [x.application_id for x in db_applications]

    for _, planning_app in planning_applications_df.iterrows():
        if int(planning_app["planning_id_code"]) not in db_application_ids:
            print("Adding new")
            tmp_app = ABPApplication()
            tmp_app.application_id = int(planning_app["planning_id_code"])
            tmp_app.application_name = planning_app["project_name"]
            tmp_app.application_date = pd.to_datetime(planning_app["lodged"])
            tmp_app.application_inf_type = planning_app["infrastructure_type"]
            tmp_app.application_decision = planning_app["decision"]
            if pd.notna(planning_app["date_signed"]):
                tmp_app.application_decision_date = pd.to_datetime(
                    planning_app["date_signed"]
                )
            tmp_app.application_time_taken = planning_app["time_taken"]
            tmp_app.save()
        else:
            print("Updating")
            tmp_app = db_applications[
                db_application_ids.index(int(planning_app["planning_id_code"]))
            ]
            tmp_app.application_decision = planning_app["decision"]
            if pd.notna(planning_app["date_signed"]):
                tmp_app.application_decision_date = pd.to_datetime(
                    planning_app["date_signed"]
                )
            tmp_app.application_time_taken = planning_app["time_taken"]
            tmp_app.save()
