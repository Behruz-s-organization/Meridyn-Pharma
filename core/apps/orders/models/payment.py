# django
from django.db import models

# shared
from core.apps.shared.models import BaseModel
# orders
from core.apps.orders.models import Order


class Payment(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='payments')
    price = models.DecimalField(max_digits=15, decimal_places=2)
    
    def __str__(self):
        return self.price
    
