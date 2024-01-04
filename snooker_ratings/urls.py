from django.urls import path
from snooker_ratings import views


urlpatterns = [
    path("", views.snooker_ratings, name="snooker_ratings"),
]
