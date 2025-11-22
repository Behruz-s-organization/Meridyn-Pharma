from django.db import models

# shared
from core.apps.shared.models import BaseModel
# accounts
from core.apps.accounts.models import User


class District(BaseModel):
    name = models.CharField(max_length=200, unique=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='districts', null=True
    )

    def __str__(self):
        return self.name
