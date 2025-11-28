from django.db import models

# shared
from core.apps.shared.models import BaseModel, District, Place
# accounts
from core.apps.accounts.models import User


class Doctor(BaseModel):
    # information
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=15)
    work_place = models.CharField(max_length=200)
    sphere = models.CharField(max_length=200)
    description = models.TextField()
    # relations
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name='doctors')
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='doctors')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='doctors')
    # location
    longitude = models.FloatField(default=0.00)
    latitude = models.FloatField(default=0.00)
    extra_location = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.work_place}"
    
    