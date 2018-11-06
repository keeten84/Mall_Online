from datetime import datetime

from django.db import models
from DjangoUeditor.models import UEditorField


# Create your models here.


class GoodsCategory(models.Model):
    '''商品类别'''
    CATEGORY_TYPE = (
        (1, '一级类目'),
        (2, '二级类目'),
        (3, '三级类目'),
    )

    name = models.CharField('类别名', max_length=30, default='', help_text='类别名')
    code = models.CharField('类别代码', max_length=30, default='', help_text='类别代码')
    desc = models.TextField('类别描述', max_length=300, default='', help_text='类别描述')
    category_type = models.IntegerField('类目级别', choices=CATEGORY_TYPE, help_text='类目级别')
    parent_category = models.ForeignKey('self', null=True, blank=True, verbose_name='父类别',
                                        related_name='sub_cat', on_delete=models.CASCADE)
    is_tab = models.BooleanField('是否放置于导航', default=False, help_text='是否放置于导航')
    add_time = models.DateTimeField('添加时间', default=datetime.now)

    class Meta:
        verbose_name = '商品类别'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class GoodsCategoryBrand(models.Model):
    '''品牌名'''
    category = models.ForeignKey(GoodsCategory, null=True, blank=True, verbose_name='商品类别', on_delete=models.CASCADE)
    name = models.CharField('商家品牌名', max_length=30, default='', help_text='商家品牌名')
    desc = models.TextField('品牌描述', max_length=300, default='', help_text='品牌描述')
    image = models.ImageField('品牌logo', max_length=200, upload_to='brands/')
    add_time = models.DateTimeField('添加时间', default=datetime.now)

    class Meta:
        verbose_name = '商家品牌名'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Goods(models.Model):
    '''商品'''
    category = models.ForeignKey(GoodsCategory, verbose_name='商品类别', on_delete=models.CASCADE)
    goods_sn = models.CharField('商品唯一货号', max_length=50, default='')
    name = models.CharField('商品名称', max_length=100)
    fav_num = models.IntegerField('收藏数', default=0)
    click_num = models.IntegerField('点击数', default=0)
    sold_num = models.IntegerField('商品销售量', default=0)
    goods_num = models.IntegerField('库存数', default=0)
    market_price = models.FloatField('市场价格', default=0)
    shop_price = models.IntegerField('本店价格', default=0)
    goods_brief = models.TextField('商品简介', max_length=500)
    goods_desc = UEditorField('商品详细描述', width=900, height=500, toolbars='full',
                              imagePath='goods/images/', filePath='goods/files/', default='')
    goods_front_image = models.ImageField('封面图', upload_to='', null=True, blank=True)
    ship_free = models.BooleanField('是否免邮', default=True)
    is_new = models.BooleanField('是否新品', default=False)
    is_hot = models.BooleanField('是否热卖', default=False)
    add_time = models.DateTimeField('添加时间', default=datetime.now)

    class Meta:
        verbose_name = '商品'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class GoodsImage(models.Model):
    '''商品轮播图'''
    goods = models.ForeignKey(Goods, verbose_name='商品', related_name='images', on_delete=models.CASCADE)
    image = models.ImageField('商品图片', upload_to='', null=True, blank=True)
    image_url = models.CharField('图片url', max_length=300, null=True, blank=True)
    add_time = models.DateTimeField('添加时间', default=datetime.now)

    class Meta:
        verbose_name = '商品的图片'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.goods.name


class Banner(models.Model):
    '''index轮播商品'''
    goods = models.ForeignKey(Goods, verbose_name='商品', on_delete=models.CASCADE)
    image = models.ImageField('轮播图', upload_to='banner')
    index = models.IntegerField('轮播图循序', default=0)
    add_time = models.DateTimeField('添加时间', default=datetime.now)

    class Meta:
        verbose_name = '轮播图'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.goods.name


class HotSearchWords(models.Model):
    """
    热搜词
    """
    keywords = models.CharField(default="", max_length=20, verbose_name="热搜词")
    index = models.IntegerField(default=0, verbose_name="排序")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = '热搜词'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.keywords