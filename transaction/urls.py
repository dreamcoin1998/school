from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CreateListRetrieveTransaction

router = DefaultRouter()
router.register('transaction', CreateListRetrieveTransaction, base_name='transaction') # 商品列表


urlpatterns = [
]