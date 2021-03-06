from datetime import datetime
from rest_framework_jwt.settings import api_settings


def jwt_get_secret_key(user):
    return user.jwt_secret


def jwt_username_handler(payload):
    return payload.get('email')


def jwt_payload_handler(user):
    """ Custom payload handler
    Token encrypts the dictionary returned by this function, and can be decoded by rest_framework_jwt.utils.jwt_decode_handler
    """
    return {
        'user_id': user.pk,
        'first_name': user.first_name,
        'surname': user.surname,
        'last_name': user.last_name,
        'phone': user.phone_number,
        'email': user.email,
        'pin_code': user.pin_code,
        'expire': (datetime.utcnow() + api_settings.JWT_EXPIRATION_DELTA).isoformat()
    }


def jwt_response_payload_handler(token, user=None, request=None):
    """ Custom response payload handler.

    This function controlls the custom payload after login or token refresh. This data is returned through the web API.
    """
    return {
        'token': token,
        'user': {
            'first_name': user.first_name,
            'surname': user.surname,
            'last_name': user.last_name
        }
    }
