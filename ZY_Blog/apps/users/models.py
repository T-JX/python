from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

import random

def random_nm(nm_len=8):
    '''
    随机产生用户昵称
    :param nm_len: 随机名称长度
    :return:随机名称
    '''
    string = 'QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm0123456789'
    str = ''
    for x in range(nm_len):
        str += random.choice(string)
    
    return str
    

class UserProfile(AbstractUser):
    
    nick_name = models.CharField(max_length=50,
                                 verbose_name='昵称',
                                 default=random_nm()
                                 ) # 用户昵称
    birday = models.DateField(verbose_name='生日',
                              null=True,
                              blank=True) # 用户生日
    phone = models.CharField(max_length=11,
                             verbose_name='手机号') # 用户手机号
    image = models.ImageField(upload_to='images/head/%Y/%m/',
                              verbose_name='用户头像') # 用户头像
    address = models.CharField(max_length=20,verbose_name='地址') # 所在地
    
    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name
        
    #  在后台界面中展示该类型对象时,这个函数返回结果就是在界面显示的结果
    def __str__(self):

        return self.nick_name
    
class EmailRecord(models.Model):

    code = models.CharField(max_length=32,verbose_name='验证码')
    email = models.CharField(max_length=100,verbose_name='邮箱')
    send_time = models.DateTimeField(auto_now_add=True,verbose_name='发送时间')
    send_type = models.CharField(choices=(('register','注册'),('forget',
                                                             '找回密码')),
                                 max_length=10,verbose_name='邮件类型')
    is_use = models.BooleanField(choices=((True,'已使用'),(False,'未使用')),
                                 default=False,
                                 verbose_name='是否使用')
    expri_time = models.DateTimeField(null=True,verbose_name='过期时间')
    
    class Meta:
        
        verbose_name = '邮件'
        verbose_name_plural = verbose_name
        
    def __str__(self):
        return '{}:{}'.format(self.email,self.code)


    
    

