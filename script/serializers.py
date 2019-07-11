from rest_framework import serializers
from script.models import SpeechScript
from django.contrib.auth.models import User


class SpeechScriptSerializer(serializers.ModelSerializer):

    class Meta:
        model = SpeechScript
        fields = '__all__'






