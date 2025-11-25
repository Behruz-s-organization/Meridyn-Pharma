from django.db import models

# shared
from core.apps.shared.models import BaseModel


class OrderItem(BaseModel):
    product = models.ForeignKey('orders.Product', on_delete=models.CASCADE, related_name='order_items')
    order = models.ForeignKey('orders.Order', on_delete=models.CASCADE, related_name='order_items')

    quantity = models.PositiveIntegerField(default=0)
    total_price = models.DecimalField(max_digits=15, decimal_places=2)

    def __str__(self):
        return f'{self.product.name} - {self.quantity}x' 
