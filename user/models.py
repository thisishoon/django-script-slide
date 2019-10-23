from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    #locale = models.CharField("국적", max_length=5, blank=True, null=True, )

    def __str__(self):
        return self.user.username
