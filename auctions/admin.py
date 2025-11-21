# auctions/admin.py

from django.contrib import admin
from .models import Auction

class AuctionAdmin(admin.ModelAdmin):
    list_display = ('title', 'seller', 'start_price', 'status', 'end_time')
    list_filter = ('status',) # 상태별로 필터링해서 볼 수 있게 함

admin.site.register(Auction, AuctionAdmin)