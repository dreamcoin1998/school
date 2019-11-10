from rest_framework import permissions

class IsOwnerOrReadOnlyInfo(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        # 如果是只读的请求则放行
        if request.method in permissions.SAFE_METHODS:
            return True
        # 如果是超级管理员放行
        if request.user.is_superuser:
            return True
        # 如果是该用户则放行
        return obj == request.user