# Generated by Django 2.1 on 2018-11-15 14:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0007_auto_20181109_1536'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordergoods',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='goods', to='transaction.OrderInfo', verbose_name='订单'),
        ),
        migrations.AlterField(
            model_name='orderinfo',
            name='pay_status',
            field=models.CharField(choices=[('TRADE_SUCCESS', ' 交易支付成功'), ('TRADE_CLOSED', '未付款交易超时关闭'), ('WAIT_BUYER_PAY', '等待买家付款'), ('TRADE_FINISHED', '交易结束，不可退款'), ('paying', '待支付')], default='paying', max_length=10, verbose_name='订单支付状态'),
        ),
    ]
