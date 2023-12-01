import time

import guindex
import folium
import numpy as np
import pandas as pd
from folium.plugins import MarkerCluster


def create_guindex_map(county):
    """Function to create a guindex pub map for the selected county"""

    # Retrieve pubs for selected county.
    pubs = guindex.pubs(county=county)

    # Determine pubs that do have prices and are open and serving guinness.
    pubs["price"] = np.where(
        pubs["closed"] | (~pubs["serving_guinness"]), np.nan,
        pubs["last_price"]
    )

    pubs["date"] = pubs['last_submission_time'].dt.date

    # Map centre.
    av_lat = pubs["latitude"].median()
    av_lon = pubs["longitude"].median()

    # Create map.
    guindex_map = folium.Map(location=[av_lat, av_lon], control_scale=True)

    # Set map zoom level to fit pubs.
    guindex_map.fit_bounds(
        [
            pubs[["latitude", "longitude"]].min().to_list(),
            pubs[["latitude", "longitude"]].max().to_list()
        ]
    )

    # Create cluster to add markers to so as to have zoom based clustering
    # of markers.
    cluster = MarkerCluster(
        locations=[[av_lat, av_lon]],
        name=None,
        icons=None,
        popups=None,
        options={
            "disableClusteringAtZoom": 14
        }
    ).add_to(guindex_map)

    # Go through pubs and create appropriate markers.
    for _, pub in pubs.iterrows():

        if pub["closed"]:
            closed_icon = folium.Icon(
                prefix="fa", icon="window-close", color="black",
                icon_color="white"
            )
            marker = folium.Marker(
                [pub["latitude"], pub["longitude"]],
                popup=pub["name"] + " - closed",
                icon=closed_icon
            )

        elif not pub["serving_guinness"]:
            not_serving_icon = folium.Icon(
                prefix="fa", icon="exclamation", color="red"
            )
            marker = folium.Marker(
                [pub["latitude"], pub["longitude"]],
                popup=pub["name"] + " - not serving Guinness",
                icon=not_serving_icon
            )

        elif pd.notnull(pub["price"]):
            price_icon = folium.Icon(
                prefix="fa", icon="beer", color="green"
            )
            marker = folium.Marker(
                [pub["latitude"], pub["longitude"]],
                popup=f"{pub['name']} - €{pub['price']},"
                      f" Submitted: {pub['date']}",
                icon=price_icon
            )

        else:
            no_price_icon = folium.Icon(
                prefix="fa", icon="question", color="lightgray"
            )
            marker = folium.Marker(
                [pub["latitude"], pub["longitude"]],
                popup=pub['name'] + " - No data submitted",
                icon=no_price_icon,
            )

        # Add marker to cluster
        marker.add_to(cluster)

    time.sleep(1)

    return guindex_map
