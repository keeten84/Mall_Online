# _*_ coding: utf-8 _*_
# __author__ = 'Keeten_Qiu'
# __date__ = '2018/10/17 下午2:32'
import re
from datetime import datetime, timedelta
from rest_framework import serializers
from rest_framework.validators import UniqueForYearValidator, UniqueValidator
from django.contrib.auth import get_user_model
from Mall_online.settings import REGEX_MOBILE
from .models import VerifyCode

User = get_user_model()


class SmsSerializer(serializers.Serializer):
    '''验证码的序列化'''
    mobile = serializers.CharField(max_length=11)

    def validate_mobile(self, mobile):
        '''
        验证手机号码
        :param mobile:
        :return:
        '''
        if User.objects.filter(mobile=mobile).count():
            raise serializers.ValidationError("用户已经存在")

        # 验证手机号码是否合法
        if not re.match(REGEX_MOBILE, mobile):
            raise serializers.ValidationError("手机号码非法")

        # 验证码发送频率
        one_minute_ago = datetime.now() - timedelta(hours=0, minutes=1, seconds=0)
        if VerifyCode.objects.filter(add_time__gt=one_minute_ago, mobile=mobile).count():
            raise serializers.ValidationError("距离上一次发送未超过60s")
        return mobile


class UserRegSerializer(serializers.ModelSerializer):
    '''用户注册的序列化'''
    code = serializers.CharField(max_length=4, min_length=4,write_only=True, help_text='验证码',
                                 error_messages={
                                     'blank': '请输入验证码',
                                     'required':'请输入验证码',
                                     'max_length':'验证码格式错误',
                                     'min_length':'验证码格式错误',
                                 })

    username = serializers.CharField(label='用户名',required=True, allow_blank=False,
                                     validators=[UniqueValidator(queryset=User.objects.all(), message="用户已经存在")])

    password = serializers.CharField( style={'input_type': 'password'},
                                      help_text="密码", label="密码",
                                      write_only=True)



    def validate_code(self, code):
        # 首先获取所有验证码记录,从前端post过来的值中取username,并排序，排序目的是从最后一个验证码开始验证
        verify_records = VerifyCode.objects.filter(mobile=self.initial_data["username"]).order_by("-add_time")
        if verify_records:
            # 因为经过排序后，第一条记录就是最后一个次发送的验证码
            last_record = verify_records[0]
            five_minutes_ago = datetime.now() - timedelta(hours=0, minutes=5, seconds=0)
            if five_minutes_ago > last_record.add_time:
                raise serializers.ValidationError('验证码已经过期')
            if last_record.code != code:
                raise serializers.ValidationError("验证码错误")
        else:
            raise serializers.ValidationError("验证码错误")

    def validate(self, attrs):
        attrs["mobile"] = attrs["username"]
        del attrs["code"]
        return attrs

    class Meta:
        model = User
        fields = ('username', 'code', 'mobile','password')
