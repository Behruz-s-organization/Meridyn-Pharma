from django.db import models

# shared
from core.apps.shared.models import BaseModel, District
# accounts
from core.apps.accounts.models import User


class Place(BaseModel):
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name='places')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='places')

    name = models.CharField(max_length=200, unique=True)
    longitude = models.FloatField(default=0.00)
    latitude = models.FloatField(default=0.00)
    extra_location = models.JSONField()

    def __str__(self):
        return self.name