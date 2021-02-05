from django.contrib.auth.models import AbstractUser
from django.db import models


# Custom user model
# fields like name, username, password, email are provided in django by default
# other fields you can add manually like age, address, etc.
class CustomUser(AbstractUser):
    age = models.PositiveIntegerField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)

