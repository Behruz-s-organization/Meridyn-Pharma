from django.db import models

# shared
from core.apps.shared.models import BaseModel


class Factory(BaseModel):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    
    