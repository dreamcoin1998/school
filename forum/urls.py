from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ListCreatePost,ListPostByType,PostListType,searchPostByNameOrDescription
router = DefaultRouter()
router.register('post', ListCreatePost, basename='post')
router.register('list_type', ListPostByType, basename='list_type')
router.register('post_types', PostListType, basename='post_types')


urlpatterns = [
        path('post_search', searchPostByNameOrDescription),
] + router.urls

