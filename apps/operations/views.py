from rest_framework import mixins
from rest_framework import generics, viewsets
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication
from django_filters.rest_framework import DjangoFilterBackend

from utils.permissions import IsOwnerOrReadOnly
from .models import UserFav, UserLeavingMessage, UserAddress
from .serializer import UserFavSerizalizer, UserFavDetailSerializer, LeavingMessageSerizalizer, AddressSerizalizer


class UserFavViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                     mixins.RetrieveModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    '''
    list:
        获取用户收藏列表
    retrieve:
        判断某个商品是否已经收藏
    create:
        收藏商品
    '''

    # queryset = UserFav.objects.all()
    serializer_class = UserFavSerizalizer
    # 配置permission验证: 登录验证，自定义只能读取自己的记录
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    # token验证
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    lookup_field = 'goods_id'
    filter_backends = (DjangoFilterBackend,)

    # 重载获取queryset方法,根据前端请求的user来筛选出数据的queryset
    def get_queryset(self):
        return UserFav.objects.filter(user=self.request.user)

    # 根据使用的方法去动态选择序列化类
    def get_serializer_class(self):
        if self.action == "list":
            return UserFavDetailSerializer
        elif self.action == "create":
            return UserFavSerizalizer
        return UserFavSerizalizer


class LeavingMessageViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                            mixins.DestroyModelMixin, viewsets.GenericViewSet):
    '''
    list:
        获取用户留言数据
    create:
        添加用户留言数据
    delete:
        删除用户留言数据
    '''
    serializer_class = LeavingMessageSerizalizer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    filter_backends = (DjangoFilterBackend,)

    # 获取当前用户的queryset数据
    def get_queryset(self):
        return UserLeavingMessage.objects.filter(user=self.request.user).order_by('id')


class AddressViewSet(viewsets.ModelViewSet):
    '''
    收货地址管理
    list:
        获取用户收货地址信息
    create:
        增加用户收货地址信息
    update:
        更新用户收货地址信息
    delete:
        删除用户收货地址信息
    '''
    serializer_class = AddressSerizalizer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    filter_backends = (DjangoFilterBackend,)
    def get_queryset(self):
        return UserAddress.objects.filter(user=self.request.user).order_by('id')