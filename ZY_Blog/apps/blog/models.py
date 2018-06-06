from django.db import models

from users.models import UserProfile
# Create your models here.

# 广告轮播
class Banner(models.Model):
    img_src = models.ImageField(upload_to='images/banner/%Y/%m/',verbose_name='广告轮播图')
    img_alt = models.CharField(max_length=100,verbose_name='轮播图提示')
    # 广告的权重,广告的先后顺序
    img_position = models.IntegerField(verbose_name='广告顺序')
    # 广告链接
    link = models.CharField(max_length=255,verbose_name='广告链接')
    class Meta:
        verbose_name = '广告轮播'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.img_alt
    
    
    



# 博客分类
class Categray(models.Model):
    name = models.CharField(max_length=10, verbose_name="分类名称")
    
    class Meta:
        verbose_name = '博客分类'
        verbose_name_plural = verbose_name
    
    def __str__(self):
        return self.name

# 博客标签
class Tags(models.Model):

    name = models.CharField(max_length=10,verbose_name='标签名')
    class Meta:
        verbose_name = '博客标签'
        verbose_name_plural = verbose_name
        
    def __str__(self):
        return self.name

# 博客
class Blog(models.Model):

    img_src = models.ImageField(upload_to='images/blog/%Y/%m/',default='images/blog/default.jpg',verbose_name='封面图')
    img_alt = models.CharField(max_length=50,verbose_name='封面图描述')
    title = models.CharField(max_length=200,verbose_name='博客标题')
    create_time = models.DateTimeField(auto_now_add=True,verbose_name='发布日期')
    edit_time = models.DateTimeField(auto_now_add=True,verbose_name='修改日期')
    look_num = models.IntegerField(verbose_name='阅读数',default=0)
    comment_num = models.IntegerField(verbose_name='评论数',default=0)
    keep_num = models.IntegerField(verbose_name='收藏数',default=0)
    digg_num = models.IntegerField(verbose_name='点赞数',default=0)
    
    content = models.TextField(verbose_name='博文内容')
    
    # 一篇博客对应一个作者,一个作者对应多篇博客  一对多的关系
    author = models.ForeignKey(UserProfile,verbose_name='作者',on_delete=models.CASCADE)
    
    # 博客分类 例如 : 生活/技术/闲谈........
    # 一篇博客对应一个分类,一个分类对应多篇博客  一对多关系
    categray = models.ForeignKey(Categray,verbose_name='分类',on_delete=models.CASCADE)
    
    # 博客标签
    # 一篇博客对应多个标签,一个标签对应博客  多对多关系
    tag = models.ManyToManyField(Tags,verbose_name='标签')


        

    
    
    









