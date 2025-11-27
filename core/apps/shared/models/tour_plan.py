from django.db import models

# shared
from core.apps.shared.models import BaseModel, District
# accounts
from core.apps.accounts.models import User


class TourPlan(BaseModel):
    place_name = models.CharField(max_length=200, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tour_plans')

    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    location_send = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.first_name}'s tour plan to {self.place_name}"
    
    def save(self, *args, **kwargs):
        if self.longitude and self.latitude:
            self.location_send = True
        return super().save(*args, **kwargs)