from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, mixins, generics
from rest_framework.decorators import api_view

from yonghu.serializers import UserSerializer
from utils.permissions import IsOwnerOrReadOnlyInfo
from rest_framework.permissions import IsAuthenticated
from yonghu.views import CsrfExemptSessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from django.contrib.auth import get_user_model
from utils.Timetable import Timetable
from utils.ReturnCode import ReturnCode
from rest_framework.response import Response


@csrf_exempt
@api_view()
def timeTable(request):
    timename = request.query_params.get('TimeName')
    openid = request.query_params.get('openid')
    print(timename)
    user = get_user_model().objects.get(pk=openid)
    print(user)
    if user.is_auth:
        usc = user.usc
        result = Timetable.USC_Timetable(usc.UserName, usc.Password, timename)
        return Response(ReturnCode(0, data=result))
    else:
        return Response(ReturnCode(1, msg='账号身份未认证'))