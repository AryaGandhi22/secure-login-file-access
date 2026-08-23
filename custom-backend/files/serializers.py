from rest_framework import serializers
from .models import UserFile


class FileUploadSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserFile
        fields = [
            "id",
            "file",
            "original_filename",
            "uploaded_at",
        ]
        read_only_fields = [
            "id",
            "original_filename",
            "uploaded_at",
        ]