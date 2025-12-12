# users/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models
from common.models import Region

class User(AbstractUser):
    # 기본 ID, 비밀번호, 이메일은 장고가 알아서 만들어줍니다.
    # 우리는 추가로 필요한 것만 적으면 됩니다.
    
    # 프로필 닉네임
    nickname = models.CharField(max_length=50, blank=True, null=True)
    
    # 신용도/평판 점수 (기본점수 0점)
    reputation_score = models.IntegerField(default=0)
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True, blank=True, related_name='residents')

    def __str__(self):
        return self.username