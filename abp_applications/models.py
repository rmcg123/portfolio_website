from django.db import models

# Create your models here.
class ABPApplication(models.Model):
    """Model for planning application."""

    application_id = models.IntegerField(primary_key=True)
    application_date = models.DateTimeField()
    application_name = models.CharField(max_length=60)
    application_inf_type = models.CharField(max_length=20)
    application_decision = models.CharField(max_length=50)
    application_decision_date = models.DateTimeField(null=True)
    application_time_taken = models.IntegerField()

