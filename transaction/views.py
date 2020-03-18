from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets, mixins
from utils.permissions import IsOwnerOrReadOnlyInfo
from utils.permissions import IsAuthenticated, IsOwnerOrReadOnlyInfo, CreateOrReadOnlyInfo
from utils import code2Session
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication
from django.contrib.auth.backends import ModelBackend
from yonghu.models import Yonghu
from yonghu.views import CsrfExemptSessionAuthentication
from .models import Commody, Type
from .serializers import CommodySerializer, TypeSerializer
from utils.ReturnCode import ReturnCode
from django.db.models.fields import exceptions


class CreateListRetrieveTransaction(mixins.CreateModelMixin,
                                    mixins.ListModelMixin,
                                    mixins.RetrieveModelMixin,
                                    mixins.UpdateModelMixin,
                                    viewsets.GenericViewSet):
    lookup_field = 'pk'
    serializer_class = CommodySerializer
    permission_classes = [IsOwnerOrReadOnlyInfo]
    authentication_classes = [JSONWebTokenAuthentication, CsrfExemptSessionAuthentication]

    def get_queryset(self):
        if self.kwargs.get('pk'):
            pk = self.kwargs.get('pk')
            return Commody.objects.filter(pk=pk, is_end=False, is_delete=False)
        else:
            return Commody.objects.filter(is_end=False, is_delete=False)

    def create(self, request, *args, **kwargs):
        '''
        创建商品信息
        :param request:
        :param args:
        :param kwargs:
        :return:
        '''
        data = request.data.copy()
        try:
            type_id = data.get('type_id')
            type_obj = Type.objects.get(pk=int(type_id))
            yonghu_pk = request.session['pk']
            yonghu_obj = Yonghu.objects.get(pk=yonghu_pk)
        except exceptions.ObjectDoesNotExist:
            return Response(ReturnCode(1, msg='object do not exists.'))
        try:
            commody = Commody()
            commody.name = data.get('name')
            commody.description = data.get('description')
            commody.price = data.get('price')
            commody.type = type_obj
            commody.qq = data.get('qq')
            commody.wx = data.get('wx')
            commody.phone_number = data.get('phone_number')
            commody.yonghu = yonghu_obj
            commody.save()
            serializer = CommodySerializer(commody)
            return Response(ReturnCode(0, data=serializer.data))
        except exceptions.FieldDoesNotExist:
            return Response(ReturnCode(1, msg='qq wx and phone_number must have at least one.'))
        except exceptions.FieldError:
            return Response(ReturnCode(1, msg='field error.'))

    def update(self, request, *args, **kwargs):
        '''
        更新商品信息
        :param request:
        :param args:
        :param kwargs:
        :return:
        '''
        commody_obj = self.get_object()
        data = request.data.copy()
        type_id = data.get('type_id')
        serializer = CommodySerializer(commody_obj, data=data)
        if serializer.is_valid():
            try:
                if type_id:
                    try:
                        type_new = Type.objects.get(pk=int(type_id))
                    except exceptions.ObjectDoesNotExist:
                        return Response(ReturnCode(1, msg='type objects do not exist.'))
                    commody_obj.type = type_new
                    commody_obj.save()
                serializer.save()
                return Response(ReturnCode(0, msg='success.', data=serializer.data))
            except exceptions.FieldDoesNotExist:
                return Response(ReturnCode(1, msg='qq wx and phone_number must have at least one.'))
        else:
            return Response(ReturnCode(1, msg='error.'))