# auctions/models.py

from django.db import models
from django.conf import settings

class Auction(models.Model):
    # 판매자 (User와 연결)
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='my_auctions')
    
    # 상품 정보
    title = models.CharField(max_length=100) # 상품명
    description = models.TextField() # 상세 설명
    image = models.ImageField(upload_to='auction_images/', blank=True, null=True) # 상품 이미지
    
    # 가격 설정 (음수 방지를 위해 PositiveIntegerField 사용)
    start_price = models.PositiveIntegerField() # 시작가
    current_price = models.PositiveIntegerField(default=0) # 현재가 (입찰 들어오면 변함)
    instant_price = models.PositiveIntegerField(blank=True, null=True) # 즉시 구매가 (선택사항)
    bid_unit = models.PositiveIntegerField(default=1000) # 입찰 단위 (예: 1000원 단위로 입찰)
    
    # 시간 설정
    start_time = models.DateTimeField() # 경매 시작 시간
    end_time = models.DateTimeField() # 경매 종료 시간
    
    # 경매 상태 (진행중, 종료, 유찰 등)
    STATUS_CHOICES = (
        ('WAITING', '대기중'),
        ('ACTIVE', '진행중'),
        ('ENDED', '종료됨'),
        ('CANCELLED', '취소됨'),
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='WAITING')
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.status}] {self.title}"
    

# auctions/models.py (맨 아래에 추가)
class Bid(models.Model):
    # 어떤 경매에 대한 입찰인지
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name='bids')
    
    # 입찰자 (User)
    bidder = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bids')
    
    # 입찰 금액
    amount = models.PositiveIntegerField()
    
    # 입찰 시간
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.bidder.username} - {self.amount}원 입찰"
