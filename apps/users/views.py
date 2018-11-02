from random import choice
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.mixins import CreateModelMixin

from utils.yunpian import YunPian
from users.models import VerifyCode
from Mall_online.settings import API_KEY
from .serializer import SmsSerializer, UserRegSerializer



User = get_user_model()


class CustomBackend(ModelBackend):
    '''自定义用户登录的验证'''

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username) | Q(mobile=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class SmsCodeViewSet(CreateModelMixin, viewsets.GenericViewSet):
    '''发送短信验证码'''
    serializer_class = SmsSerializer

    def generate_code(self):
        """
        生成四位数字的验证码:
        return:
        """
        # 从种子下随机提取数字作为验证码
        seeds = "1234567890"
        random_str = []
        for i in range(4):
            random_str.append(choice(seeds))
        return "".join(random_str)


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # 在serializer中提出已经验证的mobile手机号
        mobile = serializer.validated_data["mobile"]
        # 实例化云片短信
        yun_pian = YunPian(API_KEY)
        # 生成验证码
        code = self.generate_code()
        # 发送验证码，参数1，验证码使用自己生成的验证码，参数2手机号使用验证过的手机号
        sms_status = yun_pian.send_sms(code=code, mobile=mobile)

        # 根据云片返回的验证码code状态去判断，详细代码意思查看云片api文档
        if sms_status["code"] != 0:
            return Response({
                "mobile": sms_status["msg"]
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            code_record = VerifyCode(code=code, mobile=mobile)
            code_record.save()
            return Response({
                "mobile": mobile
            }, status=status.HTTP_201_CREATED)


class UserViewSet(CreateModelMixin,viewsets.GenericViewSet):
    '''用户'''
    serializer_class = UserRegSerializer