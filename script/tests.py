from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
import pytest, pytest_django
from .views import SpeechScript


def test_simple():
    assert 1

def test_fail():
    assert 1, "fail"

@pytest.mark.django_db
def test_user():
    client = Client()
    user = User.objects.create_user(username="jihoon", email="jihoon522@naver.com",password="98989898@")
    assert user.username=="jihoon"
    script = SpeechScript.objects.create(title="hello", content="world!")
    assert script
    temp = SpeechScript.objects.get(title="hello")
    assert temp.title=="hello"
