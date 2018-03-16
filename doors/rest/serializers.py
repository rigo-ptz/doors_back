from ..models import User
from rest_framework import serializers as rest_serializers
from rest_framework_jwt import serializers as jwt_serializers
from ..rest.custom_jwt import jwt_payload_handler
from ..rest.custom_auth import authenticate


class UserSerializer(rest_serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'surname', 'last_name', 'phone_number', 'pin_code')


class JWTSerializer(jwt_serializers.JSONWebTokenSerializer):
    pin_code = rest_serializers.CharField()
    phone_number = rest_serializers.CharField()
    username = rest_serializers.CharField(required=False, allow_blank=True, allow_null=True)
    password = rest_serializers.CharField(required=False, allow_blank=True, allow_null=True)

    def validate(self, attrs):
        pin_code = attrs.get('pin_code')
        phone_number = attrs.get('phone_number')

        print("validate")
        print(pin_code, phone_number)
        print(attrs)

        if phone_number and pin_code:
            user = authenticate(phone=phone_number, pin_code=pin_code)

            if user:
                payload = jwt_payload_handler(user)

                return {
                    'token': jwt_serializers.jwt_encode_handler(payload),
                    'user': user
                }
            else:
                msg = 'Unable to log in with provided credentials.'
                raise rest_serializers.ValidationError(msg)
        else:
            msg = 'Must include "phone" and "password".'
            raise rest_serializers.ValidationError(msg)