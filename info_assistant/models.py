from django.db import models

# Create your models here.


class Category(models.Model):
    nid = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name='分类标题', max_length=32)
    create_time = models.DateTimeField('收藏夹创建时间',default=None, null=True)

    def __str__(self):
        return self.title


class Info(models.Model):
    nid = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name="标题", max_length=200)
    search_key = models.CharField(verbose_name="搜索关键字", max_length=32)
    url = models.CharField(verbose_name="网址", max_length=100)
    source = models.CharField(verbose_name="数据来源", max_length=32)
    category = models.ForeignKey(Category, verbose_name="所属类别", on_delete=models.CASCADE)
    create_time = models.DateTimeField('信息爬取时间', default=None, null=True)

    def __str__(self):
        return self.title
