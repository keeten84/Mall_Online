# _*_ coding: utf-8 _*_
# __author__ = 'Keeten_Qiu'
# __date__ = '2018/10/16 下午11:10'

from django.views.generic.base import View
from goods.models import Goods


class GoodsListViews(View):
    def get(self, request):
        '''通过Django的View来实现商品列表页'''
        json_list = []
        goods = Goods.objects.all()[:10]

        # 展示商品的最基础方法
        # for good in goods:
        #     json_dict = {}
        #     json_dict['name'] = good.name
        #     json_dict['category'] = good.category.name
        #     json_dict['market_price'] = good.market_price
        #     json_dict['sale_price'] = good.sale_price
        #     json_dict['goods_desc'] = good.goods_desc
        #     json_dict['goods_brief'] = good.goods_brief
        #     json_list.append(json_dict)

        # 方法二： 使用django model自动转为字典的方法，转化数据
        # from django.forms.models import model_to_dict
        # for good in goods:
        #     json_dict = model_to_dict(good)
        #     json_list.append(json_dict)
        # from django.http import HttpResponse
        # import json
        # return HttpResponse(json.dumps(json_list), content_type='application/json')


        # 方法三：使用django 的序列化方法去转化json数据
        import json
        from django.core import serializers
        from django.http import HttpResponse,JsonResponse

        # json_data = serializers.serialize('json',goods)
        # json_data = json.loads(json_data)
        # return HttpResponse(json.dumps(json_data), content_type='application/json')

        # 或者直接用JsonResponse 直接转化数据
        json_data = serializers.serialize('json', goods)
        json_data = json.loads(json_data)
        return JsonResponse(json_data, safe=False)



