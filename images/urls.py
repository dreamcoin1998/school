from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CreateImagePath

router = DefaultRouter()
router.register('images', CreateImagePath, basename='images')


urlpatterns = [
] + router.urls