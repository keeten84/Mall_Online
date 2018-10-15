# _*_ coding: utf-8 _*_
# __author__ = 'Keeten_Qiu'
# __date__ = '2018/10/14 下午11:33'
import xadmin
from transaction.models import ShoppingCart, OrderInfo, OrderGoods


class ShoppingCartAdmin(object):
    list_display = ['user', 'goods', 'goods_nums', 'add_time']
    search_fields = ['user', 'goods', 'goods_nums']
    list_filter = ['user', 'goods', 'goods_nums', 'add_time']
    model_icon = 'fa fa-cart-plus'


class OrderInfoAdmin(object):
    list_display = ['user', 'order_sn', 'trade_no', 'pay_status',
                    'post_script', 'order_amount', 'address', 'signer_mobile', 'add_time']

    search_fields = ['user', 'order_sn', 'trade_no', 'pay_status',
                     'post_script', 'order_amount', 'address', 'signer_mobile']

    list_filter = ['user', 'order_sn', 'trade_no', 'pay_status',
                   'post_script', 'order_amount', 'address', 'signer_mobile', 'add_time']

    model_icon = 'fa fa-info-circle'


class OrderGoodsAdmin(object):
    list_display = ['order', 'goods', 'goods_nums', 'add_time']
    search_fields = ['order', 'goods', 'goods_nums']
    list_filter = ['order', 'goods', 'goods_nums', 'add_time']
    model_icon = 'fa fa-shopping-basket'


xadmin.site.register(ShoppingCart, ShoppingCartAdmin)
xadmin.site.register(OrderInfo, OrderInfoAdmin)
xadmin.site.register(OrderGoods, OrderGoodsAdmin)
