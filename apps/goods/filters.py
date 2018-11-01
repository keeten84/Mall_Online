# _*_ coding: utf-8 _*_
# __author__ = 'Keeten_Qiu'
# __date__ = '2018/10/25 下午3:43'
import django_filters
from django.db.models import Q
from django_filters import rest_framework as filters
from rest_framework import generics

from .models import Goods


class GoodsFilter(django_filters.rest_framework.FilterSet):
    '''
    商品的过滤类
    '''
    # 设置最大价格和最小价格的区间范围,注意变量名称应该与前端保持一样
    pricemin = django_filters.NumberFilter(field_name="sale_price", lookup_expr='gte')
    pricemax = django_filters.NumberFilter(field_name="sale_price", lookup_expr='lte')
    # 通过下面自定义方法进行筛选
    top_category = django_filters.NumberFilter(method='top_category_filter')
    # 模糊查询lookup_expr='icontains
    name = filters.CharFilter(field_name="name", lookup_expr='icontains')

    def top_category_filter(self, queryset, name, value):
        return queryset.filter(Q(category_id=value) |
                               Q(category__parent_category_id=value) |
                               Q(category__parent_category__parent_category_id=value))

    # Meta类提供了一个fields属性，可用于轻松指定多个过滤器而无需重复代码重复
    class Meta:
        model = Goods
        fields = ['pricemin', 'pricemax', 'name']
