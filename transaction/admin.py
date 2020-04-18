from django.contrib import admin
from .models import Commody, Type

@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    list_display = ('type_name',)


@admin.register(Commody)
class CommodyAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'price', 'create_time', 'type', 'qq', 'wx', 'phone_number', 'read_num', 'reply_num', 'is_end', 'is_delete')