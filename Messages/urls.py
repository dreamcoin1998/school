from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ListCreateCommodyMainMessage, ListCreateCommodyReplyMessage, ListPersonalMessage


router = DefaultRouter()
router.register('main_message', ListCreateCommodyMainMessage, basename='main_message')
router.register('reply_message', ListCreateCommodyReplyMessage, basename='reply_message')
router.register('personal', ListPersonalMessage, basename='personal')


urlpatterns = [
] + router.urls