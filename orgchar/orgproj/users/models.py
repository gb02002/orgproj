from django.db import models
from .validators import CharNullField
from django.contrib.auth.models import User
from orgs.models import Organisation


class UserProfile(models.Model):
    STATUS_CHOICES = (
        ('None', 'None'),
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
    )

    profile = models.OneToOneField(User, on_delete=models.PROTECT, primary_key=True, related_name='profile')
    name = models.CharField(max_length=20, blank=True)
    surname = models.CharField(max_length=30, blank=True)
    phone = CharNullField(max_length=20, unique=True, blank=True, null=True)
    is_org_agent = models.CharField(max_length=20, choices=STATUS_CHOICES, null=True, blank=True, default='pending')

    def __str__(self):
        return f"Profile of {self.name, self.surname}"

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'
        ordering = ['-profile', ]
