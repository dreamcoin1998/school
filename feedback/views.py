from rest_framework import viewsets, mixins
from .serializers import FeedbackSerializer
from utils.permissions import IsAuthenticated, IsOwnerOrReadOnlyInfo
from yonghu.views import JSONWebTokenAuthentication, CsrfExemptSessionAuthentication
from rest_framework.response import Response
from utils.ReturnCode import ReturnCode
from utils.getPerson import GetPersonal
from .models import Feedback
from images.models import ImagePath
from images.views import GetImagePath


class ListPersonalCreateFeedback(mixins.ListModelMixin,
                                 mixins.CreateModelMixin,
                                 viewsets.GenericViewSet,
                                 GetPersonal,
                                 GetImagePath):
    lookup_field = 'pk'
    serializer_class = FeedbackSerializer
    permission_classes = (IsOwnerOrReadOnlyInfo, IsAuthenticated)
    authentication_classes = (JSONWebTokenAuthentication, CsrfExemptSessionAuthentication)

    def list(self, request, *args, **kwargs):
        try:
            yonghu_obj = self.get_person(request)
        except KeyError:
            return Response(ReturnCode(1, msg='not login.'))
        feedbacks = yonghu_obj.feedbacks.all()
        serializers = FeedbackSerializer(feedbacks, many=True)
        return Response(ReturnCode(0, data=serializers.data))

    def create(self, request, *args, **kwargs):
        try:
            yonghu_obj = self.get_person(request)
        except KeyError:
            return Response(ReturnCode(1, msg='not login.'))
        title = request.data.get('title')
        content = request.data.get('content')
        status = 0
        # 图片，前端这里用json序列化image数组
        imagePaths = self.get_image_path(request)
        try:
            feedback_obj = Feedback()
            feedback_obj.title = title
            feedback_obj.content = content
            feedback_obj.status = status
            feedback_obj.yonghu = yonghu_obj
            feedback_obj.save()
            for imagepath in imagePaths:
                imgPath_obj = ImagePath()
                imgPath_obj.imgPath = imagepath
                imgPath_obj.content_type = feedback_obj
                imgPath_obj.object_id = feedback_obj.pk
                imgPath_obj.save()
            serializer = FeedbackSerializer(feedback_obj)
            return Response(ReturnCode(0, data=serializer.data))
        except Exception:
            return Response(ReturnCode(1, msg='field error.'))