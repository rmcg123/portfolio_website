from django.db import models

# Create your models here.
class SnookerMatch(models.Model):
    """Database table of snooker matches."""

    match_id = models.IntegerField(primary_key=True)
    event_id = models.IntegerField()

    player1_id = models.IntegerField()
    player2_id = models.IntegerField()

    player1_score = models.IntegerField()
    player2_score = models.IntegerField()

    player1_walkover = models.BooleanField()
    player2_walkover = models.BooleanField()

    best_of = models.IntegerField()
    winner_id = models.IntegerField()

    match_datetime = models.DateTimeField()
    match_season = models.IntegerField()


class SnookerEvent(models.Model):
    """Database table of snooker events."""

    event_id = models.IntegerField(primary_key=True)
    event_name = models.CharField(max_length=200)
    event_country = models.CharField(max_length=50)
    event_city = models.CharField(max_length=50)

    event_start_date = models.DateTimeField()
    event_end_date = models.DateTimeField()

    event_season = models.IntegerField()


class SnookerPlayer(models.Model):
    """Database table of snooker players."""

    player_id = models.IntegerField()
    player_name = models.CharField(max_length=100)

    player_professional = models.BooleanField()
    player_last_pro_season = models.IntegerField(null=True)
    player_rating = models.FloatField(null=True)
