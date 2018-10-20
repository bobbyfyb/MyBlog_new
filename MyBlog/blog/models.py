from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.six import python_2_unicode_compatible
from django.utils.html import strip_tags
import markdown
# Create your models here.
class Category(models.Model):
    """
    blog文章的种类
    """
    name=models.CharField(max_length=100)

    def __str__(self):
            return self.name

class Tag(models.Model):
    """ 
    blog文章的标签
    """
    name=models.CharField(max_length=100)

    def __str__(self):
        return self.name

@python_2_unicode_compatible
class Post(models.Model):
    """ 
    blog文章的结构
    """
    #文章的标题
    title=models.CharField(max_length=70)
    
    #文章正文
    body=models.TextField()

    #文章的创建时间和最后一次修改时间
    created_time=models.DateTimeField()
    modified_time=models.DateTimeField()

    #文章摘要，可以为空
    excert=models.CharField(max_length=200,blank=True)

    #文章的分类和标签，分类和标签定义如上
    #一篇文章只对应一个分类，但是一个分类下可以有多篇文章，故使用ForeignKey,即一对多关联关系
    #一篇文章可以有多个标签，一个标签也可对应多个文章，故使用ManyToManyField,即多对多关联关系
    #文章可以没有标签，故标签tags指定blank=True.
    category=models.ForeignKey(Category)
    tags=models.ManyToManyField(Tag,blank=True)

    #文章作者，一篇文章只能有一个作者但是一个作者可以有多篇文章，类似Category
    author=models.ForeignKey(User)

    #文章阅读量
    views=models.PositiveIntegerField(default=0)

    #增加文章阅读量
    def increase_views(self):
        self.views+=1
        self.save(update_fields=['views'])

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:detail',kwargs={'pk':self.pk})

    def save(self,*args,**kwargs):
        if not self.excert:
            md=markdown.Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
                ])
            self.excert=strip_tags(md.convert(self.body))[:54]

            super(Post,self).save(*args,**kwargs)

    class Meta:
        ordering=['-created_time','title']

