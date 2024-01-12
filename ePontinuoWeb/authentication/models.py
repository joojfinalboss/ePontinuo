from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name = 'perfil', null=True, default=None)
    idAnalista = models.CharField(max_length=15, blank=True)
    dataStart = models.DateField(null=True, default=None)
    dataEnd = models.DateField(null=True, default=None)
    imgURL = models.TextField(null=True, default=None, blank=True)



