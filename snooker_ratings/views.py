from datetime import datetime, timedelta

from django.shortcuts import render
from snooker_ratings.models import SnookerMatch, SnookerEvent, SnookerPlayer

# Create your views here.
def snooker_ratings(request):

    matches = SnookerMatch.objects.filter(
        match_datetime__gte=datetime.now().astimezone() - timedelta(days=7)
    )
    events = SnookerEvent.objects.filter(
        event_id__in=[x.event_id for x in matches]
    )
    players = SnookerPlayer.objects.all()
    matches = [
        x for x in matches if x.event_id in [y.event_id for y in events]
    ]
    matches = [
        x for x in matches if (
            x.player1_id in [y.player_id for y in players] and
            x.player2_id in [z.player_id for z in players]
        )
    ]
    for match in matches:
        match.event_name = events.filter(
            event_id=match.event_id
        ).first().event_name
        match.player1_name = players.filter(
            player_id=match.player1_id
        ).first().player_name
        match.player2_name = players.filter(
            player_id=match.player2_id
        ).first().player_name

    players = [x for x in players if x.player_professional]

    context = {
        "title": "An alternative rating system for snooker players",
        "matches": matches,
        "events": events,
        "players": players
    }

    return render(request, "snooker_ratings/snooker_ratings.html", context)