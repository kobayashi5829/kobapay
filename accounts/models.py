from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    total_amount = models.IntegerField(blank=True, null=False, default=0)
    
    class Meta:
        verbose_name_plural = 'CustomUser'