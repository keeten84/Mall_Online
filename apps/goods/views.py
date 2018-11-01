from rest_framework import mixins
from rest_framework import generics, viewsets
from rest_framework import filters, status
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend

from .filters import GoodsFilter
from .models import Goods, GoodsCategory
from .serializer import GoodsSerializer, CategorySerializer


# 定制属于某个View的Pagination的方法
class GoodsListViewPagination(PageNumberPagination):
    page_size = 12  # 每页想取多少条数据
    page_size_query_param = 'page_size'
    page_query_param = 'page'
    max_page_size = 100  # 最大页数


# 方法三 使用最高届别的GenericVieSet来生成商品列表页的数据
class GoodsListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    '''商品列表页, 分页, 过滤，搜索, 排序'''
    # 如果没有添加order_by('id')，列表页顺序将没有顺序，并服务器报错会生成一个没有排序的queryset
    queryset = Goods.objects.all().order_by('id')
    serializer_class = GoodsSerializer
    pagination_class = GoodsListViewPagination
    # 配置过滤数据的方法
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    # 从自己写的filter方法中调入作为filter的
    filter_class = GoodsFilter
    # 添加search_filter
    search_fields = ('name', 'goods_brief', 'goods_desc')
    # 添加排序
    ordering_fields = ('sold_num','shop_price')


class CategoryViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    '''
    list:
        商品分类列表数据
    '''
    # 首先返回商品分类的所有数据
    queryset = GoodsCategory.objects.filter(category_type=1)
    serializer_class = CategorySerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
