from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from script.models import SpeechScript
from script.serializers import SpeechScriptSerializer, UserSerializer
from django.http import JsonResponse, HttpResponse
from rest_framework import viewsets, permissions, status
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.models import User
import random, string
from django.contrib.auth import login, authenticate
from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import detail_route, list_route


@csrf_exempt
def CreateGuestUser(request):
    if request.method == "GET":
        return HttpResponse("Not allow GET Method", status=400)

    if request.method == "POST":
        username = ''.join(
            random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
        email = username + '@scriptslide.com'
        password = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))

        user_instance = User.objects.create_user(username=username, email=email, password=password)
        user_instance.save()
        if user_instance.is_authenticated:
            login(request, user_instance, backend='django.contrib.auth.backends.ModelBackend')
            token = Token.objects.create(user=user_instance)
            token.save()
            return JsonResponse({"token_key": token.key})  # token은 key와 user(username을 출력)를 필드로 가진다
        else:
            return HttpResponse(status=500)


class SpeechScriptViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    #authentication_classes = (TokenAuthentication,)

    queryset = SpeechScript.objects.all()
    serializer_class = SpeechScriptSerializer

    def get_queryset(self):  # token으로부터 해당 user의 data만 출력
        user = self.request.user
        if user.is_superuser:
            return SpeechScript.objects.all()
        else:
            return SpeechScript.objects.filter(user=user, is_deleted=False)

    def create(self, request, **kwargs):  # token으로부터 해당 user의 정보를 파악하고 생성
        # request.user는 User객체의 username값을 가져오고 request.user.id는 User의 id값을 가져온다!
        serializer = SpeechScriptSerializer(data={"title": request.data["title"], "content": request.data["content"],
                                                  "user": request.user.id})
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_deleted = True
        instance.save()
        return Response(status=status.HTTP_200_OK)



    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('user',)


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAdminUser,)
    queryset = User.objects.all()
    serializer_class = UserSerializer


def HealthCheck(request):
    return HttpResponse(status=200)


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
