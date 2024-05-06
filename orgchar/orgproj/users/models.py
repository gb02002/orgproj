from django.db import models
from .validators import CharNullField
from django.contrib.auth.models import User
from orgs.models import Organisation
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext as _
from .tasks import send_mail_new_agent


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
    is_org_agent = models.CharField(max_length=20, choices=STATUS_CHOICES, default='None', verbose_name='confirmed user')
    document_file = models.FileField(upload_to='media/users_documents', verbose_name='PDF document')

    def __str__(self):
        return f"Profile of {self.name, self.surname}"

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'
        ordering = ['-profile', ]

    def save(self, *args, **kwargs):
        try:
            if self.pk:  # Check if the instance has already been saved
                original = UserProfile.objects.get(pk=self.pk)  # Get the original instance
                if original.document_file != self.document_file:  # Check if the document_file field has been updated
                    self.is_org_agent = 'pending'  # Set is_org_agent to pending
            #         Тут надо вызвать celery
                    send_mail_new_agent.delay(self.name, self.surname, self.profile.email, self.profile.date_joined)
            super(UserProfile, self).save(*args, **kwargs)
        except ObjectDoesNotExist:
            super(UserProfile, self).save(*args, **kwargs)

    def get_status_display_with_icon(self):
        status_number = [status[0] for status in self.STATUS_CHOICES].index(self.is_org_agent)
        icon = f"/static/images/status-{status_number}.png"
        return icon
