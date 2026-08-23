from django.urls import path
from .views import (
    UploadFileView,
    UserFilesView,
    UserFileDetailView,
    DownloadFileView,
)

urlpatterns = [
    path("upload/", UploadFileView.as_view(), name="upload-file"),
    path("", UserFilesView.as_view(), name="user-files"),
    path("<int:pk>/download/", DownloadFileView.as_view(), name="file-download"),
    path("<int:pk>/", UserFileDetailView.as_view(), name="file-detail"),
]