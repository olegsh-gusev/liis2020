from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST


def response_incorrect_id():
    return Response('Not correct id', status=HTTP_400_BAD_REQUEST)


def response_incorrect_date(e):
    return Response("Please, use right date format: " + str(e), status=HTTP_400_BAD_REQUEST)
