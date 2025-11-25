from django.db import models

# shared
from core.apps.shared.models import BaseModel, District, Doctor, Place, Pharmacy
# accounts
from core.apps.accounts.models import User


class Location(BaseModel):
    district = models.ForeignKey(District, on_delete=models.SET_NULL, related_name='locations', null=True, blank=True)
    place = models.ForeignKey(Place, on_delete=models.SET_NULL, related_name='locations', null=True, blank=True) 
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, related_name='locations', null=True, blank=True)
    pharmacy = models.ForeignKey(Pharmacy, on_delete=models.SET_NULL, related_name='locations', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='locations')

    longitude = models.FloatField()
    latitude = models.FloatField()

    def __str__(self):
        return f"{self.user} sended location from {self.longitude} long and {self.langitude} lat"


class UserLocation(BaseModel):
    latitude = models.FloatField()
    longitude = models.FloatField()

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_locations')

    def __str__(self):
        return f"{self.user}'s location: {self.longitude} long and {self.latitude} lat at {self.created_at.date}/{self.created_at.time}"