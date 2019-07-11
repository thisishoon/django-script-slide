from rest_framework.authentication import TokenAuthentication

from script.models import SpeechScript
from script.serializers import SpeechScriptSerializer
from django.http import HttpResponse, JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.models import User
import random, string
from django.contrib.auth import login, authenticate
from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import csrf_exempt


def CreateRandom(request) :   #using token
    username = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))+'@scriptsslide.com'
    password = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
    user_instance = User.objects.create_user(username=username, password=password)
    user_instance.save()
    login(request, user_instance)

    token = Token.objects.create(user=user_instance)
    token.save()
    return JsonResponse({"token_key" : token.key,
                         "token_user" : token.user_id})


class SpeechScriptViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    queryset = SpeechScript.objects.all()
    serializer_class = SpeechScriptSerializer


    @csrf_exempt
    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return SpeechScript.objects.all()
        else :
            return SpeechScript.objects.filter(user=user)

    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('user',)






''' 
class ScriptList(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None) :
        scripts = Script.objects.all()  #DB의 Script객체들을 모두 불러오기
        serializer = ScriptSerializer(scripts, many=True) #직렬화를 통해 json으로 변환
        return Response(serializer.data) # 모든 json data 반환

    def post(self, request, format=None) :
        serializer = ScriptSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        else :
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ScriptDetail(APIView) :
    permission_classes = (IsAuthenticated,)

    def get_object(self, pk) :
        try :
            return Script.objects.get(pk=pk)
        except Script.DoesNotExist :
            raise Http404

    def get(self, request, pk, format=None) :
        script=self.get_object(pk)
        serializer = ScriptSerializer(script, many=True)
        return Response(serializer.data)

    def put(self, request, pk, format=None) :
        script = self.get_object(pk)
        serializer = ScriptSerializer(script, data=request.data)
        if serializer.is_valid() :
            serializer.save()
            return Response(serializer.data)
        else :
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None) :
        script = self.get_object(pk)
        script.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
'''