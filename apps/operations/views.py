from rest_framework import mixins
from rest_framework import generics, viewsets
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication
from django_filters.rest_framework import DjangoFilterBackend

from utils.permissions import IsOwnerOrReadOnly
from operations.models import UserFav
from operations.serializer import UserFavSerizalizer


class UserFavViewSet(mixins.CreateModelMixin,mixins.ListModelMixin,mixins.RetrieveModelMixin,mixins.DestroyModelMixin, viewsets.GenericViewSet):
    '''用户收藏'''
    # queryset = UserFav.objects.all()
    serializer_class = UserFavSerizalizer
    # 配置permission验证: 登录验证，自定义只能读取自己的记录
    permission_classes = (IsAuthenticated,IsOwnerOrReadOnly)
    # token验证
    authentication_classes = (JSONWebTokenAuthentication,SessionAuthentication)
    lookup_field = 'goods_id'
    filter_backends = (DjangoFilterBackend,)

    # 重载获取queryset方法,根据前端请求的user来筛选出数据的queryset
    def get_queryset(self):
        return  UserFav.objects.filter(user=self.request.user)

