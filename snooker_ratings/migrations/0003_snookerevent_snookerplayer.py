# Generated by Django 4.2.6 on 2024-01-04 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('snooker_ratings', '0002_snookermatch_match_season'),
    ]

    operations = [
        migrations.CreateModel(
            name='SnookerEvent',
            fields=[
                ('event_id', models.IntegerField(primary_key=True, serialize=False)),
                ('event_name', models.CharField(max_length=200)),
                ('event_country', models.CharField(max_length=50)),
                ('event_city', models.CharField(max_length=50)),
                ('event_start_date', models.DateTimeField()),
                ('event_end_date', models.DateTimeField()),
                ('event_season', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='SnookerPlayer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('player_id', models.IntegerField()),
                ('player_name', models.CharField(max_length=100)),
                ('player_professional', models.BooleanField()),
                ('player_last_pro_season', models.IntegerField(null=True)),
                ('player_rating', models.FloatField()),
            ],
        ),
    ]
