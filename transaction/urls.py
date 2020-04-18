from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CreateListRetrieveTransaction, searchCommodyByNameOrDescription, ListUpdatePersonalTransactions, ListCommodyByType, ListType

router = DefaultRouter()
router.register('transactions', CreateListRetrieveTransaction, basename='transaction') # 商品创建、列表、更新
router.register('personal', ListUpdatePersonalTransactions, basename='personal')
router.register('type', ListCommodyByType, basename='type')
router.register('types', ListType, basename='types')

urlpatterns = [
    path('search', searchCommodyByNameOrDescription),
] + router.urls