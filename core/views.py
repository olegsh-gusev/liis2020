import random

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.views.decorators.csrf import csrf_exempt
from parser import ParserError

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from core.models import User, WorkPlace, Reservation
from core.response import response_incorrect_id, response_incorrect_date
from core.serialaizers import WorkPlaceSerializer, ReservationSerializer
from core.utils import get_reservation, get_date


@csrf_exempt
@api_view(["GET"])
@staff_member_required()
def reservation_info(request):
    try:
        reservation_id = int(request.query_params.get('id'))
    except (TypeError, ValueError):
        return response_incorrect_id()
    return Response(ReservationSerializer(Reservation.objects.filter(workplace=reservation_id), many=True).data,
                    status=HTTP_200_OK)


@csrf_exempt
@api_view(['POST'])
@staff_member_required()
def reservation(request):
    try:
        reservation_id = int(request.query_params.get('id'))
    except (TypeError, ValueError):
        return response_incorrect_id()
    try:
        datetime_from, datetime_to = get_date(request)
    except (ParserError, ValueError) as e:
        return response_incorrect_date(e)
    workplace = WorkPlace.objects.filter(pk=reservation_id)
    if not workplace.exists():
        return Response('WorkPlace with this id does not exists', status=HTTP_400_BAD_REQUEST)
    if workplace.exclude(reservation__in=get_reservation(datetime_from, datetime_to)).exists():
        Reservation.objects.create(user=request.user, workplace=workplace.first(), date_from=datetime_from,
                                   date_to=datetime_to)
        return Response("Reservation created", status=HTTP_200_OK)
    else:
        return Response("Cannot make reservation for this period of time", status=HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(["POST"])
def register(request):
    first_name = request.data.get('first name', '')
    last_name = request.data.get('last name', '')
    email = request.data.get('email', None)
    # password_confirmed
    password = request.data.get('password', None)

    if first_name =='' and last_name =='':
        return Response("add first_name or last_name", status=HTTP_400_BAD_REQUEST)

    if email is not None:
        try:
            validate_email(email)
        except ValidationError:
            return Response('Not valid email', status=HTTP_400_BAD_REQUEST)
    username = first_name + last_name
    while User.objects.filter(username=username).exists():
        username += str(random.randint(1, 100))
    User.objects.create_user(username=username, first_name=first_name, last_name=last_name,  email= email, password=password)
    return Response('Username: ' + username, status=HTTP_200_OK)


@csrf_exempt
@api_view(["GET"])
@login_required()
def vacant_space(request):
    try:
        datetime_from, datetime_to = get_date(request)
    except (ParserError, ValueError) as e:
        return response_incorrect_date(e)
    return Response(
        WorkPlaceSerializer(WorkPlace.objects.exclude(reservation__in=get_reservation(datetime_from, datetime_to)),
                            many=True).data,
        status=HTTP_200_OK)
