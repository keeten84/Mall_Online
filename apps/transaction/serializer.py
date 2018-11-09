# _*_ coding: utf-8 _*_
# __author__ = 'Keeten_Qiu'
# __date__ = '2018/10/17 下午2:32'
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from .models import Goods, ShoppingCart
from goods.serializer import GoodsSerializer

class ShoppingCartDetailSerizalizer(serializers.ModelSerializer):
    '''购物车详情'''
    goods = GoodsSerializer(many=False)
    class Meta:
        model = ShoppingCart
        fields = "__all__"




#使用serializers.Serializer可以更加灵活去自定义需要序列化的字段的逻辑
class ShoppingCartSerializer(serializers.Serializer):

    user = serializers.HiddenField(default=serializers.CurrentUserDefault(), label='用户名')

    # goods是外键,由于用的是serializers.Serializer，所以需要指明queryset
    goods = serializers.PrimaryKeyRelatedField(required=True, queryset=Goods.objects.all(),help_text='商品',label='商品名')

    nums = serializers.IntegerField(required=True, min_value=1,
                                    error_messages={"min_value":"商品的数量不能小于1",
                                                    "required":"请选择购买数量"},
                                    help_text='商品数量',
                                    label='商品数量',
                                    )

    add_time = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M")


    def create(self, validated_data):
        '''添加商品到购物车'''
        # 首先获取用户，数量，商品
        user = self.context["request"].user
        nums = validated_data["nums"]
        goods = validated_data["goods"]
        # 从数据库中查找是否存在有该商品的记录
        existed = ShoppingCart.objects.filter(user=user, goods=goods)
        # 如果有这个商品的数据
        if existed:
            # 获取第一条数据
            existed = existed[0]
            existed.nums += nums
            existed.save()
        else:
            # 如果商品数据不存在，则调用objects.create()的方法，将validated_data里面的数据保存
            existed = ShoppingCart.objects.create(**validated_data)
        return existed

    def update(self, instance, validated_data):
        # 修改商品数量
        instance.nums = validated_data["nums"]
        instance.save()
        return instance


