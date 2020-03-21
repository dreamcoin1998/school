from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ListCreateCommodyMainMessage, ListCreateCommodyReplyMessage


router = DefaultRouter()
router.register('main_message', ListCreateCommodyMainMessage, base_name='main_message')
router.register('reply_message', ListCreateCommodyReplyMessage, base_name='reply_message')


urlpatterns = [
] + router.urls