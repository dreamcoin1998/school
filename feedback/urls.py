from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import ListPersonalCreateFeedback


router = DefaultRouter()
router.register('feedback', ListPersonalCreateFeedback, basename='feedback')


urlpatterns = [

] + router.urls