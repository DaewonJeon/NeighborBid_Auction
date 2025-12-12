# common/models.py

from django.db import models
from django.conf import settings

# [1] 지역 정보 (예: 서울 > 중구 > 봉래동2가)
class Region(models.Model):
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='sub_regions')
    name = models.CharField(max_length=50)
    # depth: 1=시/도, 2=시/군/구, 3=읍/면/동
    depth = models.IntegerField(default=1) 
    
    def __str__(self):
        if self.parent:
            return f"{self.parent} > {self.name}"
        return self.name

# [2] 카테고리 정보 (예: 디지털기기, 생활가전)
class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True, allow_unicode=True) # URL에 예쁘게 쓰기 위해

    def __str__(self):
        return self.name

# [3] 알림 정보 (아까 누락된 것 복구!)
class Notification(models.Model):
    # 알림 받을 사람
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    
    # 알림 내용
    message = models.CharField(max_length=255)
    
    # 클릭하면 이동할 주소 (예: /auction/5/)
    link = models.CharField(max_length=255, blank=True, null=True)
    
    # 읽음 여부
    is_read = models.BooleanField(default=False)
    
    # 생성 시간
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at'] # 최신 알림이 맨 위에

    def __str__(self):
        return f"{self.recipient}에게: {self.message}"