from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ListCreateMainMessage, ListCreateReplyMessage, ListPersonalMessage


router = DefaultRouter()
router.register('main_message', ListCreateMainMessage, basename='main_message')
router.register('reply_message', ListCreateReplyMessage, basename='reply_message')
router.register('personal', ListPersonalMessage, basename='personal')


urlpatterns = [
] + router.urls