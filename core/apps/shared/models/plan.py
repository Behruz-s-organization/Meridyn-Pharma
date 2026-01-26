from django.db import models

# shared
from core.apps.shared.models import BaseModel, Doctor, Pharmacy
# accounts
from core.apps.accounts.models import User


class Plan(BaseModel):
    title = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField()
    date = models.DateField()
    is_done = models.BooleanField(default=False)
    comment = models.TextField(null=True, blank=True)
    # relations
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='plans')
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, related_name='plans', null=True, blank=True)
    pharmacy = models.ForeignKey(Pharmacy, on_delete=models.SET_NULL, related_name='plans', null=True, blank=True)
    # location
    longitude = models.FloatField(default=0.00)
    latitude = models.FloatField(default=0.00)
    extra_location = models.JSONField(null=True, blank=True)

    def __str__(self):
        return self.title