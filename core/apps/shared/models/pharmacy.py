from django.db import models

# shared
from core.apps.shared.models import BaseModel, District, Place
# accounts 
from core.apps.accounts.models import User


class Pharmacy(BaseModel):
    # informations
    name = models.CharField(max_length=200)
    inn = models.CharField(max_length=200)
    owner_phone = models.CharField(max_length=15, null=True, blank=True)
    responsible_phone = models.CharField(max_length=15, null=True, blank=True)
    # relations
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name='pharmacies')
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='pharmacies')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pharmacies')
    # location
    longitude = models.FloatField(default=0.00)
    latitude = models.FloatField(default=0.00)
    extra_location = models.JSONField()

    def __str__(self):
        return f"{self.name} - {self.inn}"
    