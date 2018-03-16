from django.contrib.auth.models import BaseUserManager
from ..models import DoorsUser


def authenticate(email, phone, pin_code):
    user = DoorsUser.objects.get(email=email, phone_number=phone, pin_code=pin_code)
    return user

