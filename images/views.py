from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from .models import ImagePath
from .serializers import ImagePathSerializer
from rest_framework import mixins
from rest_framework import viewsets
from utils.permissions import IsOwnerOrReadOnlyInfo, IsAuthenticated
from yonghu.views import JSONWebTokenAuthentication, CsrfExemptSessionAuthentication
from transaction.models import Commody
from rest_framework.response import Response
from utils.ReturnCode import ReturnCode
from yonghu.models import Yonghu
from django.contrib.contenttypes.models import ContentType
from transaction.serializers import CommodySerializer
import json


class CreateImagePath(mixins.CreateModelMixin,
                      viewsets.GenericViewSet):
    lookup_field = 'pk'
    serializer_class = CommodySerializer
    permission_classes = [IsOwnerOrReadOnlyInfo, IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication, CsrfExemptSessionAuthentication]

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        return Commody.objects.get(pk=pk)

    def create(self, request, *args, **kwargs):
        '''
        上传图片
        :param request:
        :param args:
        :param kwargs:
        :return:
        '''
        imgPaths = request.data.get('imagePath')
        ct = ContentType.objects.get_for_model(self.get_object())
        img_path_obj = ImagePath()
        img_path_obj.content_type = ct
        img_path_obj.object_id = self.get_object().pk
        img_path_obj.imgPath = imgPaths
        img_path_obj.save()
        serializer = CommodySerializer(self.get_object())
        return Response(ReturnCode(0, data=serializer.data))


class GetImagePath:
    def get_image_path(self, request):
        imagePathsJson = request.data.get('imagePaths')
        imagePaths = json.loads(imagePathsJson)
        return imagePaths