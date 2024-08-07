from django.shortcuts import render
from rest_framework import viewsets,generics, mixins, permissions
from .models import *
from .serializers import *
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action

class CustomUserViewSet(viewsets.GenericViewSet,mixins.ListModelMixin,mixins.CreateModelMixin):
    permission_classes = [AllowAny]
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

class GetPhotoViewSet(viewsets.GenericViewSet,mixins.ListModelMixin):
    permission_classes = [AllowAny]
    queryset = Photo.objects.all()
    serializer_class = GetPhotoSerializer
def calculate_file_hash(file):
    hash_md5 = hashlib.md5()
    for chunk in file.chunks():
        hash_md5.update(chunk)
    return hash_md5.hexdigest()

class PhotoViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin, mixins.UpdateModelMixin):

    permission_classes = [AllowAny]
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer

    @action(detail=False, methods=['post'], url_path='upload')
    def upload_photos(self, request, *args, **kwargs):
        # Validate the input data
        serializer = PhotoUploadSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            photos = []
            errors = []
            for file in request.FILES.getlist('photos'):
                file_hash = calculate_file_hash(file)
                
                # Check if a photo with the same hash already exists
                if Photo.objects.filter(file_hash=file_hash).exists():
                    errors.append({
                        'file': file.name,
                        'error': 'Duplicate file detected'
                    })
                else:
                    # Create a new photo instance if not a duplicate
                    photo_data = {
                        'file': file,
                        'file_hash': file_hash,
                    }
                    photo_serializer = PhotoSerializer(data=photo_data)
                    if photo_serializer.is_valid():
                        photo = photo_serializer.save()
                        photos.append(photo)
                    else:
                        errors.append({
                            'file': file.name,
                            'error': photo_serializer.errors
                        })
            
            # Return errors if any
            if errors:
                return Response({'errors': errors}, status=status.HTTP_400_BAD_REQUEST)
            
            # Return the serialized photo data if no errors
            serialized_photos = [PhotoSerializer(photo).data for photo in photos]
            return Response(serialized_photos, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)