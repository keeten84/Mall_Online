# _*_ coding: utf-8 _*_
# __author__ = 'Keeten_Qiu'
# __date__ = '2018/10/17 下午2:32'
import time

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from .models import Goods, ShoppingCart, OrderInfo, OrderGoods
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


class OrderGoodsSerializer(serializers.ModelSerializer):
    goods = GoodsSerializer(many=False) #这里的goods是商品的详情信息
    class Meta:
        model = OrderGoods
        fields = "__all__"

class OrderDetailSerializer(serializers.ModelSerializer):
    goods = OrderGoodsSerializer(many=True) #这里的goods是序列化嵌套，将OrderGoods的商品详情序列化
    class Meta:
        model = OrderInfo
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    # 隐藏用户名
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    #因为支付状态/订单号/支付号可以修改的话，会是个漏洞，所以必须设置为只读
    pay_status = serializers.CharField(read_only=True)
    trade_no = serializers.CharField(read_only=True)
    order_sn = serializers.CharField(read_only=True)
    pay_time = serializers.DateTimeField(read_only=True)


    def generate_order_sn(self):
        # 一般生成的当单号的格式:当前时间(精确到秒) + user_id + 随机数
        from random import Random
        random_ins = Random()
        order_sn = "{time_str}{userid}{ranstr}".format(time_str=time.strftime("%Y%m%d%H%M%S"),
                                                       userid=self.context["request"].user.id,
                                                       ranstr=random_ins.randint(10, 99))
        return order_sn

    def validate(self, attrs):
        attrs["order_sn"] = self.generate_order_sn()
        return attrs

    class Meta:
        model = OrderInfo
        fields = "__all__"