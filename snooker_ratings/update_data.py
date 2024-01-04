"""Script to update data"""
import time
import os
import datetime as dt

import requests
import pandas as pd
from dotenv import load_dotenv
import numpy as np
from apscheduler.schedulers.background import BackgroundScheduler

import snooker_ratings.update_data_config as cfg
from snooker_ratings.models import SnookerMatch, SnookerEvent, SnookerPlayer

load_dotenv(".env")


def get_info_from_api(url, params, headers):
    """Gets all events from all seasons from snooker.org api."""

    response = requests.get(url, params=params, headers=headers)

    if response.status_code == 200:
        if response.json() != "":
            response_df = pd.json_normalize(response.json())

            response_df.drop_duplicates(inplace=True)
        else:
            response_df = pd.DataFrame()
    else:
        response_df = pd.DataFrame()

    time.sleep(6)

    return response_df


def get_recent_matches():

    url = cfg.SNOOKER_API_URL
    params = {
        "t": cfg.API_METHODS["latest_matches"],
        "ds": 2,
    }
    headers = {"X-Requested-By": os.environ["API_REQUEST_HEADER"]}

    matches = get_info_from_api(
        url=url, params=params, headers=headers
    )

    return matches

def check_matches(matches):

    matches = matches.loc[
        matches["Status"].eq(3) &
        matches["StartDate"].notnull() &
        ~(matches["Walkover1"] | matches["Walkover2"])
    ]
    if len(matches) > 0:
        events = list(matches["EventID"].unique())
        db_events = SnookerEvent.objects.filter(event_id__in=events)
        db_event_ids = [x.event_id for x in db_events]
        db_event_seasons_max = max([x.event_season for x in db_events])
        events_not_in_db = list(set(events) - set(db_event_ids))
        if len(events_not_in_db) > 0:
            new_events = pd.DataFrame()
            for event in events_not_in_db:
                url = cfg.SNOOKER_API_URL
                headers = {"X-Requested-By": os.environ["API_REQUEST_HEADER"]}
                params = {"t": cfg.API_METHODS["event"], "e": event}
                new_event = get_info_from_api(url=url, headers=headers, params=params)
                new_events = pd.concat(
                    [new_events, new_event], ignore_index=True
                )
            keep_events_mask = (
                new_events["Tour"].eq("main") &
                new_events["Sex"].eq("Both") &
                new_events["AgeGroup"].ne("S") &
                new_events["Type"].isin(["Ranking","Invitational","Qualifying"]) &
                (new_events["RankingType"].isna()|new_events["RankingType"].isin([
                    "WR", "Unknown"
                ]))
            )

            keep_new_events = new_events.loc[keep_events_mask]
            drop_new_events = new_events.loc[~keep_events_mask]

            drop_new_event_ids = drop_new_events["ID"].to_list()
            matches = matches.loc[
                ~matches["EventID"].isin(drop_new_event_ids)
            ]
            if len(keep_new_events) > 0:
                max_new_event_season = keep_new_events["Season"].max()
                if max_new_event_season > db_event_seasons_max:
                    params = {
                        "t": cfg.API_METHODS["professional_players_season"],
                        "s": max_new_event_season,
                        "st": "p"
                    }
                    pros = get_info_from_api(
                        url=url,
                        headers=headers,
                        params=params
                    )
                    db_players = SnookerPlayer.onjects.all()
                    db_pros = [x for x in db_players if x.player_professional]
                    still_pros = [
                        x for x in db_pros if x.player_id in pros["ID"].to_list()
                    ]
                    no_longer_pros = [
                        x for x in db_pros if x.player_id not in pros["ID"].to_list()
                    ]
                    new_pros = [
                        x for x in pros["ID"].to_list() if x not in [y.player_id for y in db_pros]
                    ]
                    if len(still_pros) > 0:
                        for still_pro in still_pros:
                            still_pro.player_last_pro_season = max_new_event_season
                            still_pro.save()

                    if len(no_longer_pros) > 0:
                        for no_longer_pro in no_longer_pros:
                            no_longer_pro.player_professional = False
                            no_longer_pro.update()

                    if len(new_pros) > 0:
                        for new_pro in new_pros:
                            if new_pro in [x.player_id for x in db_players]:
                                tmp_player = db_players.filter(player_id=new_pro)[0]
                                tmp_player.player_professional = True
                                tmp_player.save()
                            else:
                                player_info = pros.loc[pros["ID"].eq(new_pro)]
                                if player_info["SurnameFirst"]:
                                    player_name = (
                                        player_info["LastName"] +
                                        " " + player_info["FirstName"]
                                    )
                                else:
                                    player_name = (
                                        player_info["FirstName"] +
                                        " " + player_info["LastName"]
                                    )
                                tmp_player = SnookerPlayer()
                                tmp_player.player_id = new_pro
                                tmp_player.player_name = player_name
                                tmp_player.player_professional = True
                                tmp_player.player_last_pro_season = max_new_event_season
                                tmp_player.player_rating = 1250
                                tmp_player.save()

                for _, keep_new_event in keep_new_events.iterrows():
                    tmp_event = SnookerEvent()
                    tmp_event.event_id = keep_new_event["ID"]
                    tmp_event.event_name = keep_new_event["Name"]
                    tmp_event.event_country = keep_new_event["Country"]
                    tmp_event.event_city = keep_new_event["City"]
                    tmp_event.event_season = keep_new_event["Season"]
                    tmp_event.event_start_date = keep_new_event["StartDate"]
                    tmp_event.event_end_date = keep_new_event["EndDate"]
                    tmp_event.save()

        if len(matches) > 0:
            db_matches = SnookerMatch.objects.filter(
                match_datetime__gte=dt.datetime.now().astimezone() - dt.timedelta(days=3)
            )

            ids_to_drop = [x.match_id for x in db_matches]
            matches = matches.loc[
                ~matches["ID"].isin(ids_to_drop)
            ]

            if len(matches) > 0:
                matches["Season"] = matches["EventID"].map(
                    pd.DataFrame(
                        list(db_events.values())
                    ).groupby("event_id")["event_season"].first().to_dict()
                )
                matches["BestOf"] = np.where(
                    matches["Score1"].gt(matches["Score2"]),
                    2 * matches["Score1"] - 1,
                    np.where(
                        matches["Score1"].lt(matches["Score2"]),
                        2 * matches["Score2"] - 1,
                        2 * matches["Score1"]
                    )
                )
                for _, match in matches.iterrows():
                    tmp_match = SnookerMatch()
                    tmp_match.match_id = match["ID"]
                    tmp_match.event_id = match["EventID"]
                    tmp_match.player1_id = match["Player1ID"]
                    tmp_match.player2_id = match["Player2ID"]
                    tmp_match.player1_score = match["Score1"]
                    tmp_match.player2_score = match["Score2"]
                    tmp_match.player1_walkover = match["Walkover1"]
                    tmp_match.player2_walkover = match["Walkover2"]
                    tmp_match.winner_id = match["WinnerID"]
                    tmp_match.best_of = match["BestOf"]
                    tmp_match.match_season = match["Season"]
                    tmp_match.match_datetime = match["StartDate"]
                    tmp_match.save()


def update_data_once():

    matches = get_recent_matches()
    check_matches(matches)

def main():
    """Run this once a day."""

    schedule = BackgroundScheduler(
        {
            'apscheduler.timezone': 'UTC',
        }
    )

    schedule.add_job(update_data_once, "interval", days=1)
    schedule.start()
    try:
        while True:
            time.sleep(120)
    except (KeyboardInterrupt, SystemExit):
        schedule.shutdown()


if __name__ == "__main__":
    main()