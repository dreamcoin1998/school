from django.contrib import admin
from .models import Post
# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'created_time', 'is_deleted')

