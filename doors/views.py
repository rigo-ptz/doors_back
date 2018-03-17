from django.views.generic import TemplateView
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework import permissions
from rest_framework_jwt.views import ObtainJSONWebToken
from .models import DoorsUser, Room, KeyCell
from .rest.serializers import UserSerializer, RoomSerializer, JWTSerializer

import uuid


class IndexView(TemplateView):
    template_name = "doors/index.html"


@csrf_exempt
def api_user_list_test(request):
    if request.method == "GET":
        users = DoorsUser.objects.all()
        serializer = UserSerializer(users, many=True)
        return JsonResponse(serializer.data, safe=False)


@api_view(["POST"])
@permission_classes(())
def api_user_authorize(request):
    return ObtainJSONWebToken.as_view(serializer_class=JWTSerializer)(request._request)


@api_view(["DELETE"])
@permission_classes((permissions.IsAuthenticated, ))
def api_user_logout(request):
    user = request.user
    user.jwt_secret = uuid.uuid4()
    user.save()
    return Response(status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((permissions.IsAuthenticated, ))
@renderer_classes((JSONRenderer, ))
def api_room_get_key(request, room_id):
    key_cell = KeyCell.objects.get(room__number=room_id)
    if key_cell.has_key:
        key_cell.has_key = False
        key_cell.save()
        room = Room.objects.get(number=room_id)
        serializer = RoomSerializer(room)
        return Response(serializer.data)
    else:
        content = {'reason': 'Ключ от кабинета {0} уже взят.'.format(room_id)}
        return Response(content)

@api_view(['POST'])
@permission_classes((permissions.IsAuthenticated, ))
def api_room_return_key(request, room_id):
    pass