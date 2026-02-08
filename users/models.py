from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    ADMIN = 'ADMIN'
    OPERATOR = 'OPERATOR'
    DELIVERY = 'DELIVERY'
    
    ROLE_CHOICES = (
        (ADMIN, 'Admin'),
        (OPERATOR, 'Operator'),
        (DELIVERY, 'Delivery'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=DELIVERY)

    is_deleted = models.BooleanField(default=False, verbose_name="Is Deleted")

    def __str__(self):
        return f"{self.first_name} {self.last_name} - ({self.role})"

    @property
    def full_name(self):
        return f"{self.last_name}, {self.first_name}"