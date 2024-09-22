from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField

class Attendee(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    instagram_handle = models.CharField(max_length=100, blank=True, null=True)  # New field
    ticket_type = models.CharField(max_length=50, blank=True, null=True)
    # children = models.CharField(max_length=100, blank=True, null=True)
    submitted_at= models.DateTimeField(blank=True, null=True, auto_now_add=True)


    class Meta():
        verbose_name = "Attendee"  # Singular display name
        verbose_name_plural = "Attendees"
        ordering = ('-submitted_at',)

    def __str__(self):
        return f"Registration by {self.name} with {self.email} and ticket type as {self.ticket_type} instagram handle@{self.instagram_handle} at {self.submitted_at}"

class Child(models.Model):
    attendee = models.ForeignKey(Attendee, related_name='children', on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100)
    submitted_at= models.DateTimeField(blank=True, null=True, auto_now_add=True)


    class Meta():
        verbose_name = "Child"  # Singular display name
        verbose_name_plural = "Children"  # Plural display name
        ordering = ('-submitted_at',)

    def __str__(self):
        return self.name 
