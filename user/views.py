from django.shortcuts import render
from rest_framework.response import Response
from django.http import JsonResponse, HttpResponse
from rest_framework import permissions
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

# Create your views here.
def show_user_info(request):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)
    print(request.COOKIES)
    if request.method == "GET":
        return JsonResponse({"email": request.user.email, "first_name": request.user.first_name,
                             "last_name": request.user.last_name})


