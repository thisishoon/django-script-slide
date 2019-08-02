from django.urls import path, include
from script import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('scripts', views.SpeechScriptViewSet)
router.register('users', views.UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('create/', views.CreateGuestUser),
    path('health-check/', views.HealthCheck),
]