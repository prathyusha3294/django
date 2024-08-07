from django.urls import path, include
from rest_framework.routers import DefaultRouter
from organization.views import *

user_router = DefaultRouter()
user_router.register(r'users', CustomUserViewSet, basename='customuser')

photo_router = DefaultRouter()
photo_router.register(r'master/photos', PhotoViewSet, basename='photos')

get_photo_router = DefaultRouter()
get_photo_router.register(r'get/photos', GetPhotoViewSet, basename='photos')

urlpatterns = [
    path('', include(user_router.urls)),
    path('', include(photo_router.urls)),
    path('', include(get_photo_router.urls)),
]
