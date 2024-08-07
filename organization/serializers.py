from rest_framework import serializers
from .models import CustomUser, Photo

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'

class GetPhotoSerializer(serializers.ModelSerializer):
    user = UserSerializer() 

    class Meta:
        model = Photo
        fields = ['id', 'user', 'image', 'description', 'uploaded_at']

class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = '__all__'

class PhotoUploadSerializer(serializers.Serializer):
    images = serializers.ListField(
        child=serializers.ImageField(), 
        allow_empty=False,
    )
    description = serializers.CharField(required=False, allow_blank=True)

    def create(self, validated_data):
        images = validated_data.pop('images')
        description = validated_data.get('description', '')
        user = self.context['request'].user
        photos = []
        for image in images:
            photo = Photo.objects.create(user=user, image=image, description=description)
            photos.append(photo)
        return photos
