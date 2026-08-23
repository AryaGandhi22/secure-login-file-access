from django.db import models
from django.contrib.auth.models import User


class UserFile(models.Model):

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="files"
    )

    file = models.FileField(upload_to="uploads/")

    original_filename = models.CharField(max_length=255)

    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.original_filename