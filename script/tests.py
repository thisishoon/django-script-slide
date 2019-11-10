from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
import pytest, pytest_django
from .views import SpeechScript


def test_simple():
    assert 1

def test_fail():
    assert 1, "fail"

