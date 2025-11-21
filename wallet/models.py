# wallet/models.py

from django.db import models
from django.conf import settings

class Wallet(models.Model):
    # 지갑 주인 (User 모델과 1:1 연결) # cascade로 지우면 사라지도록!
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    # 현재 사용 가능한 잔액 (기본 0원)
    balance = models.DecimalField(max_digits=12, decimal_places=0, default=0)
    
    # 입찰 중 잠긴 재화 (아직 내 돈이지만 못 쓰는 돈) #이중입찰 방지
    locked_balance = models.DecimalField(max_digits=12, decimal_places=0, default=0)
    
    # 언제 지갑이 생성되었는지, 마지막 수정일은 언제인지
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}의 지갑 (잔액: {self.balance})"

class Transaction(models.Model):
    # 어떤 지갑의 거래인지
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='transactions')
    
    # 거래 금액 (양수면 입금, 음수면 출금)
    amount = models.DecimalField(max_digits=12, decimal_places=0)
    
    # 거래 유형 (충전, 입찰, 낙찰, 환불 등)
    TRANSACTION_TYPES = (
        ('DEPOSIT', '충전'),
        ('BID_LOCK', '입찰 잠금'),
        ('BID_REFUND', '입찰금 환불'), # 유찰 시 돌려받음
        ('PAYMENT', '낙찰 결제'),
        ('EARNING', '판매 수익'),
    )
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    
    # 상세 설명 (예: "아이폰 경매 입찰")
    description = models.TextField(blank=True)
    
    # 거래 일시
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.get_transaction_type_display()}] {self.amount}원"