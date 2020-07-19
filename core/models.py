from django.contrib.auth.models import AbstractUser
from django.db import models

# further AbstractUser (now not need email, is_staff, all names ...)
from rest_framework.fields import TimeField


class User(AbstractUser):
    def __str__(self):
        return self.username


class WorkPlace(models.Model):
    name = models.CharField(max_length=30, blank=True)
    address = models.CharField(max_length=30, blank=True)
    # TODO add is_active?

    def __str__(self):
        return self.name


class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    workplace = models.ForeignKey(WorkPlace, on_delete=models.CASCADE)
    date_from = models.DateTimeField()
    date_to = models.DateTimeField()
