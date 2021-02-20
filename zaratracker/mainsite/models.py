from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.

class Region(models.Model):

    country                   = models.CharField(max_length=15, null=False, blank=False)
    shortcut                  = models.CharField(max_length=2, null=False, blank=False)
    currency                  = models.CharField(max_length=3, null=False, blank=False)

    def __str__(self):
        return self.shortcut

class Reference(models.Model):

    uuid                      = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name                      = models.CharField(max_length=100, null=False, blank=False)
    reference                 = models.CharField(max_length=9, null=False, blank=False)
    region                    = models.ForeignKey(Region, on_delete=models.CASCADE)
    author                    = models.ForeignKey(User, on_delete=models.CASCADE)
    slug                      = models.SlugField(max_length=50, unique=True)
    
    def __str__(self):
        return str(self.reference)