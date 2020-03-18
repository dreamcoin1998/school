from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CreateListRetrieveTransaction

router = DefaultRouter()
router.register('transactions', CreateListRetrieveTransaction, base_name='transaction') # 商品创建、列表、更新


urlpatterns = [
] + router.urls