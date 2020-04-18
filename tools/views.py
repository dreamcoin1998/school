from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from utils.Timetable import Timetable
from utils.ReturnCode import ReturnCode
from rest_framework.response import Response
from yonghu.models import Yonghu
from utils.NewUSCSystemTimetable import NewTimetable


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


@csrf_exempt
@api_view(['POST'])
def getTimetable(request):
    openid = request.data.get('openid')
    assert openid is not None, 'openid is None'
    print(openid)
    user = Yonghu.objects.get(pk=openid)
    if user.is_auth_new:
        uscNew = user.uscNew
        result = NewTimetable(uscNew.UserName, uscNew.Password).run()
        return Response(ReturnCode(0, data=result))
    else:
        return Response(ReturnCode(1, msg='身份未认证'))
