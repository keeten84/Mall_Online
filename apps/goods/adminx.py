#!/usr/bin/env python
# encoding: utf-8

"""
@version: 1.0
@author: liyao
@license: Apache Licence 
@contact: yli@posbao.net
@site: http://www.piowind.com/
@software: PyCharm
@file: adminx.py
@time: 2017/7/4 17:04
"""
import xadmin
from .models import Goods, GoodsCategory, GoodsImage, GoodsCategoryBrand, Banner, HotSearchWords, IndexAd


# from .models import IndexAd

class GoodsCategoryAdmin(object):
    list_display = ["name", 'code', 'desc', "category_type", "parent_category", 'is_tab', "add_time"]
    search_fields = ["name", 'code', 'desc', "category_type", "parent_category", 'is_tab']
    list_filter = ["name", 'code', 'desc', "category_type", "parent_category", 'is_tab', "add_time"]
    model_icon = 'fa fa-hand-pointer-o'


class GoodsCategoryBrandAdmin(object):
    list_display = ["category", "name", "desc", "image", 'add_time']
    search_fields = ["category", "name", "desc", "image"]
    list_filter = ["category", "name", "desc", "image", 'add_time']
    model_icon = 'fa fa-bandcamp'

    def get_context(self):
        context = super(GoodsCategoryBrandAdmin, self).get_context()
        if 'form' in context:
            context['form'].fields['category'].queryset = GoodsCategory.objects.filter(category_type=1)
        return context


class GoodsAdmin(object):
    list_display = ['category', 'goods_sn', 'name', 'fav_num', 'click_num', 'sold_num', 'goods_num',
                    'market_price', 'shop_price', 'goods_brief', 'goods_desc', 'goods_front_image',
                    'ship_free', 'is_new', 'is_hot', 'add_time']

    search_fields = ['category', 'goods_sn', 'name', 'fav_num', 'click_num', 'sold_num', 'goods_num',
                    'market_price', 'shop_price', 'goods_brief', 'goods_desc', 'goods_front_image',
                    'ship_free', 'is_new', 'is_hot']

    list_filter = ['category', 'goods_sn', 'name', 'fav_num', 'click_num', 'sold_num', 'goods_num',
                    'market_price', 'shop_price', 'goods_brief', 'goods_desc', 'goods_front_image',
                    'ship_free', 'is_new', 'is_hot', 'add_time']

    list_editable = ["is_hot", ]

    style_fields = {"goods_desc": "ueditor"}

    model_icon = 'fa fa-sitemap'

    class GoodsImagesInline(object):
        model = GoodsImage
        exclude = ["add_time"]
        extra = 1
        style = 'tab'

    inlines = [GoodsImagesInline]


class GoodsImageAdmin(object):
    list_display = ["goods", "image", "image_url", 'add_time']
    search_fields = ["goods", "image", "image_url"]
    list_filter = ["goods", "image", "image_url", 'add_time']
    model_icon = 'fa fa-file-image-o'


class BannerAdmin(object):
    list_display = ["goods", "image", "index", 'add_time']
    search_fields = ["goods", "image", "index"]
    list_filter = ["goods", "image", "index", 'add_time']
    model_icon = 'fa fa-image'

class HotSearchAdmin(object):
    list_display = ["keywords", "index", "add_time"]


class IndexAdAdmin(object):
    list_display = ["category", "goods"]

xadmin.site.register(GoodsCategory, GoodsCategoryAdmin)
xadmin.site.register(GoodsCategoryBrand, GoodsCategoryBrandAdmin)
xadmin.site.register(Goods, GoodsAdmin)
xadmin.site.register(GoodsImage, GoodsImageAdmin)
xadmin.site.register(Banner, BannerAdmin)
xadmin.site.register(HotSearchWords, HotSearchAdmin)
xadmin.site.register(IndexAd, IndexAdAdmin)



# xadmin.site.register(HotSearchWords, HotSearchAdmin)
# xadmin.site.register(IndexAd, IndexAdAdmin)
