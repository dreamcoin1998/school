from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('forum/', include('forum.urls')),
    path('transaction/', include('transaction.urls')),
    path('auth/', include('yonghu.urls')),
]