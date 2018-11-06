# _*_ coding: utf-8 _*_
# __author__ = 'Keeten_Qiu'
# __date__ = '2018/10/17 下午2:32'
from rest_framework import serializers
from .models import GoodsCategory, Goods, GoodsImage, HotSearchWords


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