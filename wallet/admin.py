# wallet/admin.py

from django.contrib import admin
from .models import Wallet, Transaction

class TransactionInline(admin.TabularInline):
    model = Transaction
    extra = 0
    readonly_fields = ('transaction_type', 'amount', 'description', 'created_at')
    can_delete = False # 거래 내역은 함부로 지우면 안 되니까 삭제 금지

class WalletAdmin(admin.ModelAdmin):
    list_display = ('user', 'balance', 'locked_balance')
    inlines = [TransactionInline] # 지갑 정보 밑에 거래 내역을 같이 보여줌

admin.site.register(Wallet, WalletAdmin)
admin.site.register(Transaction)