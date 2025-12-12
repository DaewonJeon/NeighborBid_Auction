# common/admin.py

from django.contrib import admin
from .models import Region, Category, Notification

# 관리자 페이지에서 보기 편하게 설정
class RegionAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'depth')
    list_filter = ('depth',)

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)} # 이름 입력하면 slug 자동 생성

admin.site.register(Region, RegionAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Notification)