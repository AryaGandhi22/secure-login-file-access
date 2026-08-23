from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
#from rest_framework_simplejwt.tokens import RefreshToken
from django.http import FileResponse

from .models import UserFile
from .serializers import FileUploadSerializer


class UploadFileView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        if "file" not in request.FILES:
            return Response(
                {"message": "No file uploaded"},
                status=status.HTTP_400_BAD_REQUEST
            )

        uploaded_file = request.FILES["file"]

        user_file = UserFile.objects.create(
            owner=request.user,
            file=uploaded_file,
            original_filename=uploaded_file.name,
        )

        serializer = FileUploadSerializer(user_file)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
class UserFilesView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        files = UserFile.objects.filter(owner=request.user)

        serializer = FileUploadSerializer(files, many=True)

        return Response(serializer.data)
from django.shortcuts import get_object_or_404


class UserFileDetailView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, pk):

        file = get_object_or_404(
            UserFile,
            id=pk,
            owner=request.user
        )

        serializer = FileUploadSerializer(file)

        return Response(serializer.data)
    
class DownloadFileView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, pk):

        file = get_object_or_404(
            UserFile,
            id=pk,
            owner=request.user
        )

        return FileResponse(
            file.file.open("rb"),
            as_attachment=True,
            filename=file.original_filename
        )
    
#class MeView(APIView):
    


