from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CreateListRetrieveTransaction, searchCommodyByNameOrDescription, ListUpdatePersonalTransactions, ListCommodyByType, ListType

router = DefaultRouter()
router.register('transactions', CreateListRetrieveTransaction, base_name='transaction') # 商品创建、列表、更新
router.register('personal', ListUpdatePersonalTransactions, base_name='personal')
router.register('type', ListCommodyByType, base_name='type')
router.register('types', ListType, base_name='types')

urlpatterns = [
    path('search', searchCommodyByNameOrDescription),
] + router.urls