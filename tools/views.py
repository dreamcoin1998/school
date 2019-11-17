from rest_framework import viewsets, mixins, generics
from yonghu.serializers import UserSerializer
from utils.permissions import IsOwnerOrReadOnlyInfo
from rest_framework.permissions import IsAuthenticated
from yonghu.views import CsrfExemptSessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from django.contrib.auth import get_user_model
from utils.Timetable import Timetable
from utils.ReturnCode import ReturnCode
from rest_framework.response import Response


class Timetables(viewsets.ReadOnlyModelViewSet):
    '''
    获取课表
    '''
    lookup_field = 'pk'
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnlyInfo)
    authentication_classes = [JSONWebTokenAuthentication, CsrfExemptSessionAuthentication]

    def get_queryset(self):
        print(self.kwargs.get('pk'))
        if self.kwargs.get('pk'):
            pk = self.kwargs['pk']
        else:
            pk = self.request.user.pk
        return get_user_model().objects.filter(pk=pk)

    def list(self, request, *args, **kwargs):
        timename = request.query_params.get('TimeName')
        user = self.get_object()
        if user.is_active:
            usc = user.usc
            timetable = Timetable()
            result = timetable.USC_Timetable(usc.UserName, usc.Password, timename)
            return Response(ReturnCode(0, data=result))
        else:
            return Response(ReturnCode(1, msg='账号身份未认证'))