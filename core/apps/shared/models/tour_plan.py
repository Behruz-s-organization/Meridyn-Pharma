from django.db import models

# shared
from core.apps.shared.models import BaseModel, District
# accounts
from core.apps.accounts.models import User


class TourPlan(BaseModel):
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name='tour_plans')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tour_plans')

    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.first_name}'s tour plan to {self.district.name}"