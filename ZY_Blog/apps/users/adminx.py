import xadmin
from .models import UserProfile,EmailRecord
# UserProfile 默认会将用户表注册到后台



class EmailAdmin(object):
    # 展示字段
    list_display = ['code','email','send_type','send_time','is_use']
    # 搜索字段
    search_fields = ['email','send_type']
    # 筛选器字段
    list_filter = ['send_time']
    # 按照某字段排序
    ordering  = ['-send_time']
    # 只读字段,后台管理中只能读取不能修改
    readonly_fields = ['code','email']
    # 在列表页允许修改的页面
    list_editable = ['send_type','is_use']
    # 自动刷新
    refresh_times = [3,5]

xadmin.site.register(EmailRecord,EmailAdmin)

