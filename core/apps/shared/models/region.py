from django.db import models

from core.apps.shared.models.base import BaseModel


class Region(BaseModel):
    name = models.CharField(max_length=200, unique=True)
    users_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name