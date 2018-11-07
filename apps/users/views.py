from random import choice
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets, mixins, filters, permissions, authentication
from rest_framework.response import Response
from rest_framework.mixins import CreateModelMixin
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler

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


class UserDetailSerializer(object):
    pass


class UserViewSet(CreateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    '''
    create:
        创建用户
    retrieve:
        用户详情
    '''
    serializer_class = UserRegSerializer
    queryset = User.objects.all()
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)

    # 因为前端需要用户注册后返回登录页面，需要使用到token，所以重载create方法
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        re_dict = serializer.data
        payload = jwt_payload_handler(user)
        re_dict["token"] = jwt_encode_handler(payload)
        re_dict["name"] = user.name if user.name else user.username
        headers = self.get_success_headers(serializer.data)
        return Response(re_dict, status=status.HTTP_201_CREATED, headers=headers)

    # 这里需要动态权限配置
    # 1.用户注册的时候不应该有权限限制
    # 2.当想获取用户详情信息的时候，必须登录才行
    def get_permissions(self):
        if self.action == "retrieve":
            return [permissions.IsAuthenticated()]
        elif self.action == "create":
            return []

        return []

    # 这里需要动态选择用哪个序列化方式
    # 1.UserRegSerializer（用户注册），只返回username和mobile，会员中心页面需要显示更多字段，所以要创建一个UserDetailSerializer
    # 2.问题又来了，如果注册的使用userdetailSerializer，又会导致验证失败，所以需要动态的使用serializer
    def get_serializer_class(self):
        if self.action == "retrieve":
            return UserDetailSerializer
        elif self.action == "create":
            return UserRegSerializer

        return UserDetailSerializer

    # 虽然继承了Retrieve可以获取用户详情，但是并不知道用户的id，所有要重写get_object方法
    # 重写get_object方法，就知道是哪个用户了
    def get_object(self):
        return self.request.user

    def perform_create(self, serializer):
        return serializer.save()
