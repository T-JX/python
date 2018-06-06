from django.contrib import admin
from .models import UserProfile,EmailRecord
# Register your models here.


class UserAdmin(admin.ModelAdmin):
    
    list_display = ['username','nick_name','email','phone','address','birday']
    # search_fields 不能填写日期时间字段
    search_fields =  ['username','nick_name','email']
    # 过滤器,筛选器,日期时间可以使用筛选器
    list_filter = ['birday']
    
# 绑定注册
admin.site.register(UserProfile,UserAdmin)



admin.site.register(EmailRecord)