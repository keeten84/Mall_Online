from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .models import ShoppingCart
from .serializer import ShoppingCartSerializer, ShoppingCartDetailSerizalizer
from utils.permissions import IsOwnerOrReadOnly


class ShoppingCartViewSet(viewsets.ModelViewSet):
    '''
    购物车功能
    list:
        获取购物车的详情
    create:
        加入购物车
    delete:
        删除购物记录
    update:
        更新购物记录
    '''
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = ShoppingCartSerializer
    # 添加lookup_field可以根据设置的字段，直接访问详情页
    lookup_field = "goods_id"

    filter_backends = (DjangoFilterBackend,)

    def get_serializer_class(self):
        if self.action == "list":
            return ShoppingCartDetailSerizalizer
        else:
            return ShoppingCartSerializer

    def get_queryset(self):
        return ShoppingCart.objects.filter(user=self.request.user).order_by('goods_id')