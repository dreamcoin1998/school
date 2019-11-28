from rest_framework import permissions
from yonghu.models import Yonghu


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
            pk = request.session['pk']
            yonghu = Yonghu.objects.get(pk=pk)
            return obj == yonghu
        except Exception as e:
            return False


class IsAuthenticated(permissions.BasePermission):

    def has_permission(self, request, view):
        try:
            if request.session['pk']:
                return True
            else:
                return False
        except Exception as e:
            return False

