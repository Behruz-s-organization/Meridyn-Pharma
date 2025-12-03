# django
from django.db import models

# shared
from core.apps.shared.models import BaseModel
# orders
from core.apps.orders.models import Product
# accounts
from core.apps.accounts.models import User


class DistributedProduct(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='distributed_products')
    date = models.DateField()
    employee_name = models.CharField(max_length=200)
    quantity = models.PositiveIntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='distributed_products')

    def __str__(self):
        return f'{self.product} recieved for {self.employee_name}, quantity -> {self.quantity}x'
    