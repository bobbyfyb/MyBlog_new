from django.contrib.syndication.views import Feed

from .models import Post

class AllPostsRssFeed(Feed):
    #标题
    title="Artorias个人博客"

    #网址
    link="/"

    #描述信息
    descreption="Artorias 的个人博客"

    #需要显示的内容条目
    def items(self):
        return Post.objects.all()

    #聚合器中显示的内容条目的标题
    def item_title(self,item):
        return '[%s] %s' % (item.category,item.title)

    #聚合器中显示的内容条目的描述
    def item_description(self, item):
        return item.body

