from datetime import datetime
from django.db import models
from django.contrib.auth import get_user_model
from goods.models import Goods

User = get_user_model()


class ShoppingCart(models.Model):
    user = models.ForeignKey(User, verbose_name='用户', on_delete=models.CASCADE)
    goods = models.ForeignKey(Goods, verbose_name='商品名', on_delete=models.CASCADE)
    nums = models.IntegerField(default=0, verbose_name='商品数量')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '购物车'
        verbose_name_plural = verbose_name
        unique_together = ("user", "goods")

    def __str__(self):
        return '%s:%s(%d)'.format(self.user.name, self.goods.name, self.nums)


class OrderInfo(models.Model):
    '''订单'''
    PAY_STATUS = (
        ('TRADE_SUCCESS', ' 交易支付成功'),
        ('TRADE_CLOSED', '未付款交易超时关闭'),
        ('WAIT_BUYER_PAY', '等待买家付款'),
        ('TRADE_FINISHED','交易结束，不可退款'),
        ('paying','待支付')
    )

    user = models.ForeignKey(User, verbose_name='用户', on_delete=models.CASCADE)
    order_sn = models.CharField(max_length=30, null=True, blank=True,verbose_name='交易号')
    trade_no = models.CharField(max_length=100, unique=True, null=True, blank=True, verbose_name='支付号')
    pay_status = models.CharField(choices=PAY_STATUS,default='paying', max_length=10, verbose_name='订单支付状态')
    post_script = models.CharField(max_length=200, verbose_name='订单留言')
    order_mount = models.FloatField(default=0.0, verbose_name='订单金额')
    pay_time = models.DateTimeField(null=True, blank=True, verbose_name='支付时间')

    # 用户信息
    address = models.CharField(max_length=200, default='', verbose_name='收货地址')
    signer_name = models.CharField(max_length=20, default='', verbose_name='收件人')
    signer_mobile = models.CharField(max_length=11, default='', verbose_name='收件人手机')

    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '订单详情信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.order_sn)


class OrderGoods(models.Model):
    '''订单的商品详情'''
    order = models.ForeignKey(OrderInfo, verbose_name='订单', on_delete=models.CASCADE, related_name="goods")
    goods = models.ForeignKey(Goods, verbose_name='商品', on_delete=models.CASCADE)
    goods_nums = models.IntegerField(default=0, verbose_name='订单数')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '订单中的商品详情'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.order.order_sn)
