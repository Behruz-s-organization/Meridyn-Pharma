from django.db import models

# shared
from core.apps.shared.models import BaseModel, Pharmacy
# accounts
from core.apps.accounts.models import User



class Order(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    pharmacy = models.ForeignKey(Pharmacy, on_delete=models.CASCADE, related_name='orders')

    total_price = models.DecimalField(decimal_places=2, max_digits=15)
    paid_price = models.DecimalField(decimal_places=2, max_digits=15)
    advance = models.FloatField()
    employee_name = models.CharField(max_length=200)

    def __str__(self):
        return f'#{self.id} from {self.user.first_name}, total_price - {self.total_price}, paid - {self.paid_price}'
    