from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CreateListRetrieveTransaction, searchCommodyByNameOrDescription, ListUpdatePersonalTransactions

router = DefaultRouter()
router.register('transactions', CreateListRetrieveTransaction, base_name='transaction') # 商品创建、列表、更新
router.register('personal', ListUpdatePersonalTransactions, base_name='personal')

urlpatterns = [
    path('search', searchCommodyByNameOrDescription),
] + router.urls