# _*_ coding: utf-8 _*_
# __author__ = 'Keeten_Qiu'
# __date__ = '2018/10/17 下午2:32'
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from .models import UserFav, UserLeavingMessage, UserAddress
from goods.serializer import GoodsSerializer


class UserFavDetailSerializer(serializers.ModelSerializer):
    goods = GoodsSerializer()

    class Meta:
        model = UserFav
        fields = "__all__"


class UserFavSerizalizer(serializers.ModelSerializer):
    '''用户收藏'''
    # 获取当前用户
    user = serializers.HiddenField(default=serializers.CurrentUserDefault(), label='用户名')

    class Meta:
        model = UserFav

        validators = [UniqueTogetherValidator(queryset=UserFav.objects.all(),
                                              fields=('user', 'goods'),
                                              message='已收藏')]
        fields = ('user', 'goods', 'id')


class LeavingMessageSerizalizer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault(), label='用户名')
    add_time = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M")
    class Meta:
        model = UserLeavingMessage
        fields = ("user", "message_type", "subject", "message", "file", "id", "add_time")


class AddressSerizalizer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault(), label='用户名')
    add_time = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M")

    class Meta:
        model = UserAddress
        fields = ("id", "user", "province", "city", "district", "address", "signer_name", "signer_mobile","add_time")