# Generated by Django 2.1 on 2018-11-09 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0004_auto_20181108_1502'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderinfo',
            name='order_sn',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='订单号'),
        ),
        migrations.AlterField(
            model_name='orderinfo',
            name='pay_status',
            field=models.CharField(choices=[('success', '成功支付'), ('cancel', '取消支付'), ('paying', '待支付')], default='paying', max_length=10, verbose_name='订单支付状态'),
        ),
    ]
