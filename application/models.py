from django.db import models
from datetime import datetime
from django.contrib.auth.models import User, auth
# Create your models here.


# python manage.py makemigrations
# python manage.py migrate
# python manage.py runserver

class txt_file(models.Model):
    myFile = models.FileField(upload_to = "files")
    uploaded_by = models.ForeignKey(User, on_delete = models.CASCADE)
    uploaded_at = models.DateTimeField(default = datetime.now())


class recording(models.Model):
    audio_file = models.FileField(upload_to = "recordings")
    uploaded_by = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "uploaded_by")
    uploaded_at = models.DateTimeField(default = datetime.now())
    ratings = models.IntegerField(null = True, blank = True)
    is_checked = models.BooleanField(default = False)
    checked_by = models.ForeignKey(User, on_delete = models.CASCADE, blank = True, null = True, default = None, related_name = "checked_by")
    checked_at = models.DateTimeField(default = datetime.now())

class initial_test(models.Model):
    new_user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "new_user")
    recordings = models.ManyToManyField(recording)
    submitted_at = models.DateTimeField(default = datetime.now())
    ratings = models.IntegerField(null = True, blank = True)
    feedback = models.TextField()
    is_approved = models.BooleanField(default = False)
    approved_by = models.ForeignKey(User, on_delete = models.CASCADE, blank = True, null = True, default = None, related_name = "approved_by")

    