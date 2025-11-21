# auctions/services.py (새로 만들기)

from django.db import transaction
from django.utils import timezone
from .models import Auction, Bid
from wallet.models import Wallet, Transaction

def place_bid(auction_id, user, amount):
    """
    입찰을 수행하는 핵심 함수 (트랜잭션 적용)
    """
    with transaction.atomic():
        # 1. 경매 정보를 가져오되, 동시성 문제를 막기 위해 'Lock'을 겁니다.
        # (누가 입찰하는 동안 다른 사람은 이 경매 정보를 수정 못하게 막음)
        auction = Auction.objects.select_for_update().get(id=auction_id)
        
        # 경매 상태 확인
        if auction.status != 'ACTIVE':
            raise ValueError("진행 중인 경매가 아닙니다.")
        
        if auction.end_time < timezone.now():
            raise ValueError("이미 종료된 경매입니다.")
            
        # 가격 검증 (현재가 + 입찰단위보다 높아야 함)
        min_bid_price = auction.current_price + auction.bid_unit
        # (첫 입찰인 경우 시작가보다 높아야 함)
        if auction.current_price == 0:
            min_bid_price = auction.start_price
            
        if amount < min_bid_price:
            raise ValueError(f"최소 {min_bid_price}원 이상 입찰해야 합니다.")

        # 입찰자의 지갑 확인
        wallet = Wallet.objects.select_for_update().get(user=user)
        if wallet.balance < amount:
            raise ValueError("잔액이 부족합니다.")

        # ============================================
        # 여기서부터 진짜 돈 처리 (가장 중요!)
        # ============================================

        # 2. 이전 최고 입찰자가 있다면 돈 돌려주기 (잠금 해제)
        # 현재가(current_price)가 0이 아니고, 입찰 기록이 있다면
        if auction.current_price > 0:
            last_bid = auction.bids.order_by('-amount').first()
            if last_bid:
                prev_bidder_wallet = Wallet.objects.select_for_update().get(user=last_bid.bidder)
                
                # 묶여있던 돈(locked)을 다시 잔액(balance)으로 이동
                prev_bidder_wallet.locked_balance -= last_bid.amount
                prev_bidder_wallet.balance += last_bid.amount
                prev_bidder_wallet.save()
                
                # 로그 남기기
                Transaction.objects.create(
                    wallet=prev_bidder_wallet,
                    amount=last_bid.amount,
                    transaction_type='BID_REFUND',
                    description=f"경매({auction.title}) 상위 입찰 발생으로 환불"
                )

        # 3. 내 돈 잠그기 (지갑에서 차감 -> 잠금으로 이동)
        wallet.balance -= amount
        wallet.locked_balance += amount
        wallet.save()
        
        Transaction.objects.create(
            wallet=wallet,
            amount=-amount, # 내역에는 음수로 표시하거나 0으로 표시 (잠금이니까)
            transaction_type='BID_LOCK',
            description=f"경매({auction.title}) 입찰 예약금"
        )

        # 4. 입찰 기록 생성
        Bid.objects.create(
            auction=auction,
            bidder=user,
            amount=amount
        )

        # 5. 경매 현재가 업데이트
        auction.current_price = amount
        auction.save()

        return f"성공! {amount}원에 입찰했습니다."