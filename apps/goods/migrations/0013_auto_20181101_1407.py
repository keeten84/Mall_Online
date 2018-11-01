# Generated by Django 2.1 on 2018-11-01 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0012_auto_20181101_1402'),
    ]

    operations = [
        migrations.RenameField(
            model_name='goods',
            old_name='click_nums',
            new_name='click_num',
        ),
        migrations.RenameField(
            model_name='goods',
            old_name='fav_nums',
            new_name='fav_num',
        ),
        migrations.RenameField(
            model_name='goods',
            old_name='goods_nums',
            new_name='goods_num',
        ),
        migrations.RenameField(
            model_name='goods',
            old_name='sold_nums',
            new_name='sold_num',
        ),
        migrations.AlterField(
            model_name='goods',
            name='market_price',
            field=models.FloatField(default=0, verbose_name='市场价格'),
        ),
        migrations.AlterField(
            model_name='goods',
            name='shop_price',
            field=models.IntegerField(default=0, verbose_name='本店价格'),
        ),
    ]
