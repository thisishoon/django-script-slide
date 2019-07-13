from django.contrib.auth.models import User, AbstractUser
from django.db import models
from django.contrib.sessions.models import Session


class SpeechScript(models.Model): #SpeechScript 변경
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    title = models.CharField("제목", max_length=144, null=False)  # 대본 제목
    content = models.TextField("내용", blank=True, null=False)  # 대본 내용
    created_at = models.DateTimeField("생성 시간", auto_now_add=True)  # 시간 저장
    updated_at = models.DateTimeField("변경 시간", auto_now=True)  # 업데이트 시간 저장

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return "[{}]  {}".format(self.user.id, self.title)


