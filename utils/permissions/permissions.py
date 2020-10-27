from rest_framework import permissions
from yonghu.models import QQUser, WXUser, APPUser, NewUSCINFO
from django.core.exceptions import ObjectDoesNotExist
from yonghu.models import UserCommon


def get_user_obj(request):
    pk = request.session['pk']
    platform = request.session['plt']
    if platform == 'WX':
        user_obj = WXUser.objects.get(pk=pk)
    elif platform == "APP":
        user_obj = APPUser.objects.get(pk=pk)
    else:
        user_obj = QQUser.objects.get(pk=pk)
    return user_obj


class IsOwnerOrReadOnlyInfo(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        # 如果是只读的请求则放行
        if request.method in permissions.SAFE_METHODS:
            return True
        # 如果是超级管理员放行
        if request.user.is_superuser:
            return True
        # 如果是该用户则放行
        try:
            user_obj = get_user_obj(request)
            return obj == user_obj
        except KeyError as e:
            return False


class CreateOrReadOnlyInfo(permissions.BasePermission):

    def has_object_permission(self, request, view, usc_obj):
        # 如果是只读的请求则放行
        if request.method in permissions.SAFE_METHODS or request.method == 'POST':
            return True
        # 如果是超级管理员放行
        if request.user.is_superuser:
            return True
        # 如果是该用户则放行
        try:
            user_obj = get_user_obj(request)
            the_usc_obj = NewUSCINFO.objects.get(pk=user_obj.pk)
            return usc_obj == the_usc_obj
        except KeyError as e:
            return False
        except ObjectDoesNotExist as e:
            return False


class IsAuthenticated(permissions.BasePermission):

    def has_permission(self, request, view):
        # if request.method in permissions.SAFE_METHODS:
        #     return True
        try:
            if isinstance(request.user, UserCommon):
                return True
            else:
                return False
        except KeyError as e:
            return False
