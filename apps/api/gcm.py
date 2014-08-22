from django.db.models.query import QuerySet
from push_notifications.models import GCMDevice
#serializers

from django.http import Http404
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status

def send_push(object, message):
    # imported inside function due to circular import 
    from push_notifications.models import GCMDevice
    from django.contrib.auth.models import User
    from apps.users.models import Dept, Subdept, Page
    if isinstance(object, User):
        devices = GCMDevice.objects.filter(user=object)
    if isinstance(object, Dept) or isinstance(object,Subdept) or isinstance(object, Page):
        users= object.related_users()
        devices = GCMDevice.objects.filter(user__in=users)
    
    if isinstance(object, QuerySet):
        object=list(object)
        if isinstance(object[0],User):
            devices=GCMDevice.objects.filter(user__in=object)

    devices.send_message(message)

class GCMViewSet(viewsets.ModelViewSet):
    """
    Used for associating users and their phones the first time the login 
    to send push push notifications
    """
    model=GCMDevice
    # def post(self, request, format=None):
    #     from apps.api.serializers import GCMDeviceSerializer
    #     serializer = GCMDeviceSerializer(data=request.DATA)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
