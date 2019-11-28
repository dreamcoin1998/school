from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from utils.Timetable import Timetable
from utils.ReturnCode import ReturnCode
from rest_framework.response import Response
from yonghu.models import Yonghu


@csrf_exempt
@api_view()
def timeTable(request):
    timename = request.query_params.get('TimeName')
    openid = request.query_params.get('openid')
    print(timename)
    user = Yonghu.objects.get(pk=openid)
    print(user)
    if user.is_auth:
        usc = user.usc
        result = Timetable.USC_Timetable(usc.UserName, usc.Password, timename)
        return Response(ReturnCode(0, data=result))
    else:
        return Response(ReturnCode(1, msg='账号身份未认证'))