from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ListCreateCommodyMainMessage, ListCreateCommodyReplyMessage, ListPersonalMessage


router = DefaultRouter()
router.register('main_message', ListCreateCommodyMainMessage, base_name='main_message')
router.register('reply_message', ListCreateCommodyReplyMessage, base_name='reply_message')
router.register('personal', ListPersonalMessage, base_name='personal')


urlpatterns = [
] + router.urls