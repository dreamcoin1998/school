from django.contrib import admin
from .models import ImagePath


@admin.register(ImagePath)
class ImagePathAdmin(admin.ModelAdmin):
    list_display = ('imgPath',)