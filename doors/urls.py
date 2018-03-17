from django.urls import path
from . import views
from rest_framework_jwt.views import ObtainJSONWebToken, obtain_jwt_token
from .rest.serializers import JWTSerializer

app_name = "Doors App"

urlpatterns = [
    path("api/v1/user/alltest",  views.api_user_list_test, name='api-user-list'),
    path("api/v1/user/authorize",  views.api_user_authorize, name='api-user-auth'),
    path("api/v1/user/logout", views.api_user_logout, name='api-user-logout'),
    path("api/v1/room/<int:room_id>/keys/get", views.api_room_get_key, name='api-room-get_key'),
    path("api/v1/room/<int:room_id>/keys/return", views.api_room_return_key, name='api-room-return_key'),
    path("", views.IndexView.as_view(), name="index")
]
