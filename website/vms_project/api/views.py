from django.http import HttpResponse
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

from .serializers import CustomUserSerializer, TaskSerializer

from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth import logout, login

from vms_app.models import CustomUser

@api_view(['POST'])
def driverLogin(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = CustomUserSerializer(data=data)
        if serializer.is_valid():
            lUser = CustomUser.objects.filter(username=serializer.validated_data['username'],
                                              password=serializer.validated_data['password'],
                                              user_type=CustomUser.DRIVER).last()
            login(request, lUser)
            return Response({'status':'success',
                             'data':serializer.validated_data}, status=status.HTTP_200_OK)
        else:
            return Response({'status':'fail',
                             'data':serializer.error_messages}, status=status.HTTP_400_BAD_REQUEST)

def driverLogout(request):
    logout(request)
    return HttpResponse("Logged out!")

@api_view(['POST'])
@csrf_exempt
def finishTask(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = TaskSerializer(data=data)
        if serializer.is_valid():
            task = serializer.validated_data['Task']
            task.status = serializer.validated_data['task_status']
            task.save()
            return Response("Good!",status=status.HTTP_200_OK)
        else:
            return Response({'status': 'fail',
                             'data': serializer.error_messages}, status=status.HTTP_400_BAD_REQUEST)