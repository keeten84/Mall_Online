# encoding: utf-8

import xadmin
from .models import UserFav, UserLeavingMessage, UserAddress


class UserFavAdmin(object):
    list_display = ['user', 'goods', "add_time"]
    search_fields = ['user', 'goods']
    list_filter = ['user', 'goods', "add_time"]
    model_icon = 'fa fa-heart'


class UserLeavingMessageAdmin(object):
    list_display = ['user', 'message_type', 'subject', "message", "add_time"]
    search_fields = ['user', 'message_type', 'subject', "message"]
    list_filter = ['user', 'message_type', 'subject', "message", "add_time"]
    model_icon = 'fa fa-envelope'


class UserAddressAdmin(object):
    list_display = ["signer_name", "signer_mobile", "district", "address", 'add_time']
    search_fields = ["signer_name", "signer_mobile", "district", "address"]
    list_filter = ["signer_name", "signer_mobile", "district", "address", 'add_time']
    model_icon = 'fa fa-map-pin'


xadmin.site.register(UserFav, UserFavAdmin)
xadmin.site.register(UserLeavingMessage, UserLeavingMessageAdmin)
xadmin.site.register(UserAddress, UserAddressAdmin)
