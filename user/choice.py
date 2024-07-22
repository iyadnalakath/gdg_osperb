from django.db import models

class RoleChoice(models.TextChoices):
  ADMIN = 'admin', 'Admin'
  STAFF = 'staff', 'Staff'
