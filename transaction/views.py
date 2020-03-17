from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets, mixins
from utils.permissions import IsOwnerOrReadOnlyInfo
from utils.permissions import IsAuthenticated
from utils import code2Session
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication
from django.contrib.auth.backends import ModelBackend
from .serializers import CommodySerializer, MessageSerializer, ImagePathSerializer
from yonghu.views import CsrfExemptSessionAuthentication
from .models import Commody


class CreateListRetrieveTransaction(mixins.CreateModelMixin,
                                    mixins.ListModelMixin,
                                    mixins.RetrieveModelMixin,
                                    viewsets.GenericViewSet):
    lookup_field = 'type'
    serializer_class = CommodySerializer
    permission_classes = None
    authentication_classes = [JSONWebTokenAuthentication, CsrfExemptSessionAuthentication]

    def get_queryset(self):
        if self.kwargs.get('type'):
            type = self.kwargs.get('type')
            return Commody.objects.filter(type=type)
        else:
            return Commody.objects.all()