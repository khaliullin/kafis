from django.db import models

from compare.models import GENDER_CHOICES


# Create your models here.

class Photo(models.Model):
    name = models.CharField(max_length=100, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True)
    image = models.ImageField(upload_to='photos/')

    def __str__(self):
        return f'{self.name} ({self.gender})'
