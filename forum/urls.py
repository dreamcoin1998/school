from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ListCreatePost,ListCreatePostMainMessage,ListCreatePostReplyMessage,ListPersonalMessage

router = DefaultRouter()
router.register('post', ListCreatePost, basename='post')


urlpatterns = [
] + router.urls

