# _*_ coding: utf-8 _*_
# __author__ = 'Keeten_Qiu'
# __date__ = '2018/10/17 下午2:32'
from rest_framework import serializers
from .models import UserFav

class UserFavSerizalizer(serializers.ModelSerializer):
    '''用户收藏'''
    class Meta:
        model = UserFav
        fields = ('user','goods')