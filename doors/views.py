from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework_jwt.views import ObtainJSONWebToken
from rest_framework.response import Response
from rest_framework.request import clone_request
from .models import DoorsUser
from .rest.serializers import UserSerializer
from .rest.serializers import JWTSerializer
from rest_framework import permissions


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
    print(request.user)
    return Response("STUB")