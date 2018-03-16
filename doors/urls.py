from django.urls import path
from . import views
from rest_framework_jwt.views import ObtainJSONWebToken, obtain_jwt_token
from .rest.serializers import JWTSerializer

app_name = "Doors App"

urlpatterns = [
    path("api/v1/user/alltest",  views.api_user_list_test),
    path("api/v1/user/authorize",  views.api_user_authorize),
    path("api/v1/user/logout", views.api_user_logout),
    path("", views.IndexView.as_view(), name="index")
]
