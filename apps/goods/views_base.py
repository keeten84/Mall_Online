# _*_ coding: utf-8 _*_
# __author__ = 'Keeten_Qiu'
# __date__ = '2018/10/16 下午11:10'
import json

from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic.base import View
from goods.models import Goods


class GoodsListViews(View):
    def get(self,request):
        '''通过Django的View来实现商品列表页'''
        goods = Goods.objects.all()[:10]
        json_list = []
        for good in goods:
            json_dict = {}
            json_dict['name'] = good.name
            json_dict['category'] = good.category.name
            json_dict['market_price'] = good.market_price
            json_dict['sale_price'] = good.sale_price
            json_dict['goods_desc'] = good.goods_desc
            json_dict['goods_brief'] = good.goods_brief
            json_list.append(json_dict)

        return HttpResponse(json.dumps(json_list),content_type='application/json')
