from django.db import models

# shared
from core.apps.shared.models import BaseModel


class Product(BaseModel):
    name = models.CharField(max_length=200)
    price = models.DecimalField(decimal_places=2, max_digits=15)
    
    def __str__(self):
        return self.name