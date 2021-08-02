from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    
    birth_date = models.DateField(null=True)

    def __str__(self):
        return self.username