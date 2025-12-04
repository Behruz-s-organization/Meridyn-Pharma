# django
from django.db import models

# shared
from core.apps.shared.models import BaseModel, District
# accounts
from core.apps.accounts.models import User


class Support(BaseModel):
    TYPE = (
        ('PROBLEM', 'muammo'),
        ('HELP', 'yordam'),
    )

    district = models.ForeignKey(
        District,
        on_delete=models.SET_NULL, 
        related_name='supports', 
        blank=True, 
        null=True
    )
    problem = models.TextField()
    date = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='supports')
    type = models.CharField(choices=TYPE, default="PROBLEM", max_length=8)

    def __str__(self):
        return f"#{self.id} problem from {self.user.first_name} {self.user.last_name}"
    