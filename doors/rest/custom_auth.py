from django.contrib.auth.models import BaseUserManager
from ..models import User


def authenticate(phone, pin_code):
    user = User.objects.get(phone_number=phone, pin_code=pin_code)
    return user

