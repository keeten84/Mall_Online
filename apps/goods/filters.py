# _*_ coding: utf-8 _*_
# __author__ = 'Keeten_Qiu'
# __date__ = '2018/10/25 下午3:43'
import django_filters
from django_filters import rest_framework as filters
from rest_framework import generics

from .models import Goods


class GoodsFilter(django_filters.rest_framework.FilterSet):
    '''
    商品的过滤类
    '''
    # 设置最大价格和最小价格的区间范围
    min_price = filters.NumberFilter(field_name="sale_price", lookup_expr='gte')
    max_price = filters.NumberFilter(field_name="sale_price", lookup_expr='lte')
    #模糊查询lookup_expr='icontains
    name = filters.CharFilter(field_name="name", lookup_expr='icontains')


    # Meta类提供了一个fields属性，可用于轻松指定多个过滤器而无需重复代码重复
    class Meta:
        model = Goods
        fields = ['min_price', 'max_price','name']