# Generated by Django 2.1 on 2018-11-09 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0005_auto_20181109_1430'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderinfo',
            name='order_sn',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='交易号'),
        ),
    ]