from django.db import models

# shared
from core.apps.shared.models import BaseModel
# accounts
from core.apps.accounts.models import User


class Plan(BaseModel):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    # relations
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='plans')

    def __str__(self):
        return self.title