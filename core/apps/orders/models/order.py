from django.db import models

# shared
from core.apps.shared.models import BaseModel, Factory
# accounts
from core.apps.accounts.models import User



class Order(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    factory = models.ForeignKey(Factory, on_delete=models.CASCADE, related_name='orders', null=True)

    total_price = models.DecimalField(decimal_places=2, max_digits=15)
    paid_price = models.DecimalField(decimal_places=2, max_digits=15)
    overdue_price = models.DecimalField(decimal_places=2, max_digits=15, default=0)
    advance = models.FloatField()
    employee_name = models.CharField(max_length=200)

    def __str__(self):
        return f'#{self.id} from {self.user.first_name}, total_price - {self.total_price}, paid - {self.paid_price}'
    
    def save(self, *args, **kwargs):
        self.overdue_price = self.total_price - self.paid_price
        return super().save(*args, **kwargs)