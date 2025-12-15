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
    
# users/models.py 맨 아래

class Review(models.Model):
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='written_reviews')
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_reviews')
    auction = models.OneToOneField('auctions.Auction', on_delete=models.CASCADE) # 경매 하나당 리뷰 하나
    
    rating = models.IntegerField(default=5, choices=[(i, i) for i in range(1, 6)]) # 1~5점
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.reviewer} -> {self.seller} ({self.rating}점)"