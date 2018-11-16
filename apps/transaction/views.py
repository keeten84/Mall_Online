import time
from datetime import datetime
from django.shortcuts import redirect
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters, mixins
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.response import Response
from Mall_online.settings import private_key_path, ali_pub_key_path
from utils.alipay import AliPay
from .models import ShoppingCart, OrderInfo, OrderGoods
from .serializer import ShoppingCartSerializer, ShoppingCartDetailSerizalizer, OrderSerializer, OrderDetailSerializer
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

    # 新增商品到购物车，库存减去相应到数量
    def perform_create(self, serializer):
        shop_cart = serializer.save()
        goods = shop_cart.goods
        goods.goods_num -= shop_cart.nums
        goods.save()

    # 删除购物车记录，库存增加相应到数量
    def perform_destroy(self, instance):
        goods = instance.goods
        goods.goods_num += instance.nums
        # goods需要在delete之前取
        instance.delete()

    # 修改购物车里某个商品的数量
    def perform_update(self, serializer):
        # 获取已有购物车的数据的值
        existed_record = ShoppingCart.objects.get(id=serializer.instance.id)
        # 获取到保存之前到数量
        existed_nums = existed_record.nums
        # 获取到保存之后的数量
        saved_record = serializer.save()
        # 获得保存后的数量减去保存前的数量的值
        nums = saved_record.nums - existed_nums
        goods = saved_record.goods
        goods.goods_num -= nums
        goods.save()

    def get_serializer_class(self):
        if self.action == "list":
            return ShoppingCartDetailSerizalizer
        else:
            return ShoppingCartSerializer

    def get_queryset(self):
        return ShoppingCart.objects.filter(user=self.request.user).order_by('goods_id')


class OrderViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
    '''
    订单管理
    list:
        获取个人的订单信息
    create:
        新增订单
    delete:
        删除订单
    '''
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = OrderSerializer
    filter_backends = (DjangoFilterBackend,)

    def get_queryset(self):
        return OrderInfo.objects.filter(user=self.request.user).order_by('id')

    # 订单详情页面需要动态选择serializer
    def get_serializer_class(self):
        if self.action == "retrieve":
            return OrderDetailSerializer
        return OrderSerializer

    def perform_create(self, serializer):
        order = serializer.save()
        # 获取当前用户所有购物车的数据
        shop_carts = ShoppingCart.objects.filter(user=self.request.user)
        # 遍历
        for shop_cart in shop_carts:
            order_goods = OrderGoods()
            order_goods.goods = shop_cart.goods
            order_goods.goods_nums = shop_cart.nums
            order_goods.order = order
            order_goods.save()

            shop_cart.delete()
        return order


# 由于这里不存在model的关系，所以我们可以直接使用底层的apiview来实现，直接重写get和post请求
class AlipayView(APIView):
    def get(self, request):
        '''
        处理支付宝的return_url返回
        :param request:
        :return:
        '''
        processed_dict = {}
        for key, value in request.GET.items():
            processed_dict[key] = value

        sign = processed_dict.pop("sign", None)

        alipay = AliPay(
            appid="",
            app_notify_url="http://127.0.0.1:8000/alipay/return/",
            app_private_key_path=private_key_path,
            alipay_public_key_path=ali_pub_key_path,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            debug=True,  # 默认False,
            return_url="http://127.0.0.1:8000/alipay/return/"
        )

        verify_re = alipay.verify(processed_dict, sign)

        if verify_re is True:
            order_sn = processed_dict.get('out_trade_no', None)
            trade_no = processed_dict.get('trade_no', None)
            trade_status = processed_dict.get('trade_status', None)

            existed_orders = OrderInfo.objects.filter(order_sn=order_sn)
            for existed_order in existed_orders:
                existed_order.pay_status = trade_status
                existed_order.trade_no = trade_no
                existed_order.pay_time = datetime.now()
                existed_order.save()

            response = redirect("index")
            response.set_cookie("nextPath", "pay", max_age=3)
            return response
        else:
            response = redirect("index")
            return response

    def post(self, request):
        '''
        处理支付宝的notify_url
        :param request:
        :return:
        '''
        processed_dict = {}
        for key, value in request.POST.items():
            processed_dict[key] = value

        # 在支付宝post过来的数据中抽取sign字段的数据
        sign = processed_dict.pop("sign", None)

        alipay = AliPay(
            appid="",
            app_notify_url="http://127.0.0.1:8000/alipay/return/",
            app_private_key_path = private_key_path,
            alipay_public_key_path = ali_pub_key_path,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            debug=True,  # 默认False,
            return_url="http://127.0.0.1:8000/alipay/return/"
        )

        verify_re = alipay.verify(processed_dict, sign)

        if verify_re is True:
            order_sn = processed_dict.get('out_trade_no', None)
            trade_no = processed_dict.get('trade_no', None)
            trade_status = processed_dict.get('trade_status', None)

            existed_orders = OrderInfo.objects.filter(order_sn=order_sn)
            for existed_order in existed_orders:
                order_goods = existed_order.goods.all()
                for order_good in order_goods:
                    goods = order_good.goods
                    goods.sold_num += order_good.goods_num
                    goods.save()

                existed_order.pay_status = trade_status
                existed_order.trade_no = trade_no
                existed_order.pay_time = datetime.now()
                existed_order.save()

            return Response("success")