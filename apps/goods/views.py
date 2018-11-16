from rest_framework import mixins
from rest_framework import generics, viewsets
from rest_framework.response import Response
from rest_framework import filters, status
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_extensions.cache.mixins import CacheResponseMixin

from .filters import GoodsFilter
from .models import Goods, GoodsCategory, HotSearchWords, Banner
from .serializer import GoodsSerializer, CategorySerializer, HotWordsSerializer, BannerSerializer, \
    IndexCategorySerializer

from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication


# 定制属于某个View的Pagination的方法
class GoodsListViewPagination(PageNumberPagination):
    page_size = 12  # 每页想取多少条数据
    page_size_query_param = 'page_size'
    page_query_param = 'page'
    max_page_size = 100  # 最大页数

# 方法三 使用最高届别的GenericVieSet来生成商品列表页的数据
class GoodsListViewSet(CacheResponseMixin,mixins.ListModelMixin, mixins.RetrieveModelMixin,viewsets.GenericViewSet):
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

    # 实现商品点击数的自动修改，通过重写retrieve方法去实现
    def retrieve(self, request, *args, **kwargs):
        # 获取商品
        instance = self.get_object()
        # 当获取到当前的商品之后，商品的点击数自动加1
        instance.click_num += 1
        # 保存
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class CategoryViewSet(CacheResponseMixin,mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    '''
    list:
        商品分类列表数据
    retrieve:
        获取商品分类详情
    '''
    # 首先返回商品分类的所有数据
    queryset = GoodsCategory.objects.filter(category_type=1).order_by('id')
    serializer_class = CategorySerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)

class HotSearchsViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    获取热搜词列表
    """
    queryset = HotSearchWords.objects.all().order_by("-index")
    serializer_class = HotWordsSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)

class BannerViewSet(mixins.ListModelMixin,viewsets.GenericViewSet):
    '''
    获取轮播图列表
    '''
    queryset = Banner.objects.all().order_by('index')
    serializer_class = BannerSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)

class IndexCategoryViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    首页商品分类数据
    """
    queryset = GoodsCategory.objects.filter(is_tab=True, name__in=["生鲜食品", "酒水饮料"])
    serializer_class = IndexCategorySerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)