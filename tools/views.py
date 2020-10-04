from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from utils.uscSystem.Timetable import Timetable
from utils.returnCode.ReturnCode import ReturnCode
from rest_framework.response import Response
from yonghu.models import QQUser
from utils.uscSystem.NewUSCSystemTimetable import NewTimetable
from utils.getPerson import GetPersonal
from utils.uscSystem.usc import Usc


@csrf_exempt
@api_view()
def timeTable(request):
    '''
    老系统课表接口，停止维护
    :param request:
    :return:
    '''
    timename = request.query_params.get('TimeName')
    openid = request.query_params.get('openid')
    print(timename)
    user = QQUser.objects.get(pk=openid)
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
    '''
    新系统课表接口
    :param request:
    :return:
    '''
    openid = request.data.get('openid')
    assert openid is not None, 'openid is None'
    print(openid)
    user = QQUser.objects.get(pk=openid)
    if user.is_auth_new:
        uscNew = user.uscNew
        result = NewTimetable(uscNew.UserName, uscNew.Password).run()
        return Response(ReturnCode(0, data=result))
    else:
        return Response(ReturnCode(1, msg='身份未认证'))


@csrf_exempt
@api_view(['POST'])
def check_score(request):
    '''
    查询成绩
    :param request:
    :return:
    '''
    try:
        yonghu_obj = GetPersonal().get_person(request)
    except KeyError:
        return Response(ReturnCode(1, msg='not login.'), status=400)
    if yonghu_obj.is_auth_new:
        usc_new_info = yonghu_obj.uscNew
        result = Usc(usc_new_info.UserName, usc_new_info.Password).check_score(request.data)
        return Response(ReturnCode(0, data=result))
    else:
        return Response(ReturnCode(1, msg='身份未认证'))