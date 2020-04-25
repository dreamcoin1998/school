from django.contrib import admin
from .models import Post,PostType
# Register your models here.

@admin.register(PostType)
class PostTypeAdmin(admin.ModelAdmin):
    list_display = ('type_name',)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'created_time', 'is_deleted', 'type')

