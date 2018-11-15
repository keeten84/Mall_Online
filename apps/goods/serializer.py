# _*_ coding: utf-8 _*_
# __author__ = 'Keeten_Qiu'
# __date__ = '2018/10/17 下午2:32'
from django.db.models import Q
from rest_framework import serializers
from .models import GoodsCategory, Goods, GoodsImage, HotSearchWords, Banner, GoodsCategoryBrand, IndexAd


class CategorySerializer3(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategory
        fields = "__all__"


class CategorySerializer2(serializers.ModelSerializer):
    sub_cat = CategorySerializer3(many=True)

    class Meta:
        model = GoodsCategory
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    """
    商品类别序列化
    """
    sub_cat = CategorySerializer2(many=True) # many=True 表示可以显示多个2类的数据，不写会报错

    class Meta:
        model = GoodsCategory
        fields = "__all__"


class GoodsImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsImage
        fields = ('image',)

class GoodsSerializer(serializers.ModelSerializer):
    # 将category字段用序列化之后的GoodsCategory代替，就可以实现序列化嵌套功能
    category = CategorySerializer()
    # 将image数据序列化到goods的序列化中
    images = GoodsImageSerializer(many=True)

    class Meta:
        model = Goods
        # 序列化所有字段，也可以把需要序列化的字段fields = ('category'）写进入
        fields = '__all__'

class HotWordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotSearchWords
        fields = "__all__"

class BannerSerializer(serializers.ModelSerializer):
    goods = GoodsSerializer()
    class Meta:
        model = Banner
        fields = "__all__"


# 序列化brand
class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategoryBrand
        fields = "__all__"

# 把brands的序列化嵌套到indexgoods序列化中，用于以后提取数据
class IndexCategorySerializer(serializers.ModelSerializer):
    brands = BrandSerializer(many=True)
    goods = serializers.SerializerMethodField()
    sub_cat = CategorySerializer2(many=True)
    ad_goods = serializers.SerializerMethodField()

    def get_ad_goods(self, obj):
        goods_json = {}
        ad_goods = IndexAd.objects.filter(category_id=obj.id)
        if ad_goods:
            good_ins = ad_goods[0].goods
            # 添加context = {'request': self.context['request']} 会在数据前添加域名
            goods_json = GoodsSerializer(good_ins, many=False, context={'request': self.context['request']}).data
        return goods_json


    # 自定义goods的获取方法
    def get_goods(self, obj):

        all_goods = Goods.objects.filter(Q(category_id=obj.id) |
                                         Q(category__parent_category_id=obj.id) |
                                         Q(category__parent_category__parent_category_id=obj.id))

        goods_serializer = GoodsSerializer(all_goods, many=True, context={'request': self.context['request']})
        return goods_serializer.data


    class Meta:
        model = GoodsCategory
        fields = "__all__"
