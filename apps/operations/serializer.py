# _*_ coding: utf-8 _*_
# __author__ = 'Keeten_Qiu'
# __date__ = '2018/10/17 下午2:32'
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from .models import UserFav

class UserFavSerizalizer(serializers.ModelSerializer):
    '''用户收藏'''
    # 获取当前用户
    user = serializers.HiddenField(default=serializers.CurrentUserDefault(),label='用户名')
    class Meta:
        model = UserFav

        validators = [UniqueTogetherValidator(queryset=UserFav.objects.all(),
                                              fields=('user', 'goods'),
                                              message='已收藏')]
        fields = ('user', 'goods','id')