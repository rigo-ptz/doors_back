from django.views.generic import TemplateView
from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework import permissions
from rest_framework_jwt.views import ObtainJSONWebToken
from .models import Room, KeyCell, Lesson, DoorsUser
from .rest.serializers import RoomSerializer, JWTSerializer

from .utils import pretty_time_delta

import uuid
from django.utils.dateparse import parse_datetime
import datetime


class IndexView(TemplateView):
    template_name = "doors/index.html"


@api_view(["POST"])
@permission_classes(())
def api_user_authorize(request):
    return ObtainJSONWebToken.as_view(serializer_class=JWTSerializer)(request._request)


@api_view(["DELETE"])
@permission_classes((permissions.IsAuthenticated,))
def api_user_logout(request):
    user = request.user
    user.jwt_secret = uuid.uuid4()
    user.save()
    return Response(status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((permissions.IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def api_room_get_key(request, room_id):
    try:
        key_cell = KeyCell.objects.get(room__number=room_id)
    except KeyCell.DoesNotExist:
        content = {'reason': 'Такого ключа нет в системе.'}
        return Response(content)

    if key_cell.has_key:
        key_cell.has_key = False
        key_cell.user_who_get = DoorsUser.objects.get(phone_number=request.user.phone_number)
        key_cell.save()
        room = Room.objects.get(number=room_id)
        serializer = RoomSerializer(room)
        return Response(serializer.data)
    else:
        content = {'reason': 'Ключ от кабинета {0} уже взят.'.format(room_id)}
        return Response(content)


@api_view(['GET'])
@permission_classes((permissions.IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def api_room_return_key(request, room_id):
    # TODO: its possible to make check here on user who returns the key
    try:
        key_cell = KeyCell.objects.get(room__number=room_id)
    except KeyCell.DoesNotExist:
        content = {'reason': 'Такого ключа нет в системе.'}
        return Response(content)

    if not key_cell.has_key:
        key_cell.has_key = True
        key_cell.user_who_get = None
        key_cell.save()
        room = Room.objects.get(number=room_id)
        serializer = RoomSerializer(room)
        return Response(serializer.data)
    else:
        content = {'reason': 'Ключ от кабинета {0} уже находится в ячейке.'.format(room_id)}
        return Response(content)


@api_view(['GET'])
@permission_classes((permissions.IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def api_room_get_key_by_schedule(request, date_str):
    client_time = parse_datetime(date_str)
    print(client_time)

    try:
        lesson = Lesson.objects.filter(
            teacher__phone_number=request.user.phone_number
        ).filter(
            time_start__gte=client_time
        ).order_by('time_start').first()
        if lesson is None:
            raise Lesson.DoesNotExist
    except Lesson.DoesNotExist:
        content = {'reason': 'В расписании нет предметов'}
        return Response(content)

    diff = lesson.time_start - client_time
    diff_sec = diff.total_seconds()
    print(diff, diff_sec)

    if diff_sec > 1800:
        content = {
            'reason': 'Ваше занятие через {0} Вы можете взять ключ за 30 минут.'.format(
                pretty_time_delta(diff_sec)
            )
        }
        return Response(content)
    else:
        try:
            key_cell = KeyCell.objects.get(room__number=lesson.room.number)
        except KeyCell.DoesNotExist:
            content = {'reason': 'Такого ключа нет в системе.'}
            return Response(content)

        if key_cell.has_key:
            key_cell.has_key = False
            key_cell.user_who_get = DoorsUser.objects.get(phone_number=request.user.phone_number)
            key_cell.save()
            room = Room.objects.get(number=lesson.room.number)
            serializer = RoomSerializer(room)
            return Response(serializer.data)
        else:
            if key_cell.user_who_get is None:
                content = {'reason': 'Не можем найти преподавателя, взявшего ключ.'}
                return Response(content)
            else:
                content = {
                    'reason': 'Ключ от кабинета {0} уже взят. {1} ({2})'.format(
                        lesson.room.number,
                        key_cell.user_who_get.__str__(),
                        key_cell.user_who_get.phone_number
                    )
                }
                return Response(content)

            # delta_prev = client_time - datetime.timedelta(minutes=30)
            # try:
            #     previous_lesson_in_room = Lesson.objects.filter(
            #         room__number=lesson.room.number
            #     ).filter(
            #         time_end__gte=delta_prev
            #     ).filter(
            #         time_start__lte=delta_prev
            #     ).order_by('time_end').first()
            #
            #     if previous_lesson_in_room is None:
            #         raise Lesson.DoesNotExist
            # except Lesson.DoesNotExist:
            #     content = {'reason': 'Не можем найти преподавателя, взявшего ключ.'}
            #     return Response(content)
            #
            # content = {
            #     'reason': 'Ключ от кабинета {0} уже взят. {1} ({2})'.format(
            #         lesson.room.number,
            #         previous_lesson_in_room.teacher.__str__(),
            #         previous_lesson_in_room.teacher.phone_number
            #     )
            # }
            # return Response(content)
