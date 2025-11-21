from django.db import models
from django.contrib.auth.models import AbstractUser

# shared 
from core.apps.shared.models import BaseModel, Region


class User(AbstractUser, BaseModel):
    telegram_id = models.CharField(max_length=200, null=True)
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, related_name='regions', null=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.telegram_id}"

    