from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField

class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    submitted_at= models.DateTimeField(blank=True, null=True, auto_now_add=True)


    class Meta():
    	ordering = ('-submitted_at',)

    def __str__(self):
        return f"Registration by {self.name} with ({self.email} at {self.submitted_at}"
