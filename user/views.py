from django.shortcuts import render
from rest_framework.response import Response
from django.http import JsonResponse, HttpResponse
from rest_framework import permissions
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from script.models import SpeechScript
from django.views.decorators.csrf import csrf_exempt
from rest_framework_jwt.utils import jwt_decode_handler
from django.contrib.auth.models import User

# Create your views here.
def show_user_info(request):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    if request.method == "GET":
        jwt = request.META.get('HTTP_AUTHORIZATION')
        decoded_payload = jwt_decode_handler(jwt[4:])
        user = User.objects.get(id=decoded_payload['user_id'])

        print(request.user.email)
        print(user.email)

        return JsonResponse({"email": user.email, "first_name": user.first_name,
                             "last_name": user.last_name})

@csrf_exempt
def move_script_to_user(request):
    if request.method == "POST":
        token = request.data["token"]
        jwt = request.data["jwt"]

        temp1 = SpeechScript.objects.filter(user=token.user)
        temp2 = SpeechScript.objects.filter(user=jwt.user)
        print(temp1)
        print(temp2)
        return
