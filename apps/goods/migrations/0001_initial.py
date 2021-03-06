# Generated by Django 2.1.2 on 2018-10-11 12:38

import DjangoUeditor.models
import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='banner', verbose_name='轮播图')),
                ('index', models.IntegerField(default=0, verbose_name='轮播图循序')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
            ],
            options={
                'verbose_name': '商品图片',
                'verbose_name_plural': '商品图片',
            },
        ),
        migrations.CreateModel(
            name='GoodImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='', verbose_name='商品图片')),
                ('image_url', models.CharField(blank=True, max_length=300, null=True, verbose_name='图片url')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
            ],
            options={
                'verbose_name': '商品图片',
                'verbose_name_plural': '商品图片',
            },
        ),
        migrations.CreateModel(
            name='Goods',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('goods_sn', models.CharField(default='', max_length=50, verbose_name='商品唯一货号')),
                ('name', models.CharField(max_length=200, verbose_name='商品名称')),
                ('fav_nums', models.IntegerField(default=0, verbose_name='收藏数')),
                ('click_nums', models.IntegerField(default=0, verbose_name='点击数')),
                ('sold_nums', models.IntegerField(default=0, verbose_name='商品销售量')),
                ('goods_nums', models.IntegerField(default=0, verbose_name='库存数')),
                ('market_price', models.FloatField(default=0, verbose_name='市场价')),
                ('shop_price', models.IntegerField(default=0, verbose_name='零售价')),
                ('goods_brief', models.TextField(max_length=500, verbose_name='商品简介')),
                ('goods_desc', DjangoUeditor.models.UEditorField(default='', verbose_name='商品详细描述')),
                ('goods_front_image', models.ImageField(blank=True, null=True, upload_to='', verbose_name='封面图')),
                ('ship_free', models.BooleanField(default=True, verbose_name='是否免邮')),
                ('is_new_product', models.BooleanField(default=False, verbose_name='是否新品')),
                ('is_hot_product', models.BooleanField(default=False, verbose_name='是否热卖')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
            ],
            options={
                'verbose_name': '商品',
                'verbose_name_plural': '商品',
            },
        ),
        migrations.CreateModel(
            name='GoodsCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', help_text='类别名', max_length=30, verbose_name='类别名')),
                ('code', models.CharField(default='', help_text='类别代码', max_length=30, verbose_name='类别代码')),
                ('desc', models.CharField(default='', help_text='类别描述', max_length=300, verbose_name='类别描述')),
                ('category_type', models.CharField(choices=[(1, '一级类目'), (2, '二级类目'), (3, '三级类目')], help_text='类别级别', max_length=10, verbose_name='类别级别')),
                ('is_tab', models.BooleanField(default=False, help_text='是否放置于导航', verbose_name='是否放置于导航')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
                ('parent_category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sub_cat', to='goods.GoodsCategory', verbose_name='父类别')),
            ],
            options={
                'verbose_name': '商品类别',
                'verbose_name_plural': '商品类别',
            },
        ),
        migrations.CreateModel(
            name='GoodsCategoryBrand',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', help_text='商家品牌名', max_length=30, verbose_name='商家品牌名')),
                ('desc', models.TextField(default='', help_text='品牌描述', max_length=300, verbose_name='品牌描述')),
                ('image', models.ImageField(max_length=200, upload_to='brand/images', verbose_name='品牌logo')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
            ],
            options={
                'verbose_name': '商家品牌',
                'verbose_name_plural': '商家品牌',
            },
        ),
        migrations.AddField(
            model_name='goods',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goods.GoodsCategory', verbose_name='商品类别'),
        ),
        migrations.AddField(
            model_name='goodimage',
            name='goods',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='goods.Goods', verbose_name='商品'),
        ),
        migrations.AddField(
            model_name='banner',
            name='goods',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goods.Goods', verbose_name='商品'),
        ),
    ]
