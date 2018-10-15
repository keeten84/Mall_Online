# -*- coding: utf-8 -*-
__author__ = 'bobby'

import xadmin
from .models import ShoppingCart, OrderInfo, OrderGoods

class ShoppingCartAdmin(object):
    list_display = ["user", "goods", "goods_nums",'add_time']
    search_fields = ["user", "goods", "goods_nums"]
    list_filter = ["user", "goods", "goods_nums",'add_time']
    model_icon = 'fa fa-shopping-cart'

class OrderInfoAdmin(object):
    list_display = ["user", "order_sn",  "trade_no", "pay_status", "post_script", "order_amount","pay_time", "add_time"]

    search_fields = ["user", "order_sn",  "trade_no", "pay_status", "post_script", "order_amount","pay_time"]

    list_filter = ["user", "order_sn",  "trade_no", "pay_status", "post_script", "order_amount","pay_time", "add_time"]

    model_icon = 'fa fa-info-circle'

    class OrderGoodsInline(object):
        model = OrderGoods
        exclude = ['add_time', ]
        extra = 1
        style = 'tab'

    inlines = [OrderGoodsInline, ]


class OrderGoodsAdmin(object):
    list_display = ["order", "goods", "goods_nums", 'add_time']
    search_fields = ["order", "goods", "goods_nums"]
    list_filter = ["order", "goods", "goods_nums", 'add_time']



xadmin.site.register(ShoppingCart, ShoppingCartAdmin)
xadmin.site.register(OrderInfo, OrderInfoAdmin)
xadmin.site.register(OrderGoods,OrderGoodsAdmin)