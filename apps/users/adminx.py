#!/usr/bin/env python
# encoding: utf-8

import xadmin
from xadmin import views
from .models import VerifyCode


class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


class GlobalSettings(object):
    site_title = "xxx生鲜超市管理平台"
    site_footer = "xxx生鲜超市"
    menu_style = "accordion"


class VerifyCodeAdmin(object):
    list_display = ['code', 'mobile', "add_time"]
    search_fields = ['code', 'mobile']
    list_filter = ['code', 'mobile', "add_time"]
    model_icon = 'fa fa-free-code-camp'


xadmin.site.register(VerifyCode, VerifyCodeAdmin)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)