from django.urls import path, include
from script import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('scripts', views.SpeechScriptViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('create/', views.CreateRandom),

]