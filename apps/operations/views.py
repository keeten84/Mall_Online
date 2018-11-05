from rest_framework import mixins
from rest_framework import generics, viewsets
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from operations.models import UserFav
from operations.serializer import UserFavSerializer


class UserFavViewSet(mixins.CreateModelMixin,mixins.DestroyModelMixin, viewsets.GenericViewSet):
    '''用户收藏'''
    queryset = UserFav.objects.all()
    serializer_class = UserFavSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)