import xadmin
from django.views.static import serve
from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from rest_framework.documentation import include_docs_urls
from rest_framework.authtoken import views
from rest_framework_jwt.views import obtain_jwt_token

from Mall_online.settings import MEDIA_ROOT
from transaction.views import ShoppingCartViewSet
from users.views import SmsCodeViewSet, UserViewSet
from goods.views import GoodsListViewSet, CategoryViewSet, HotSearchsViewset
from operations.views import UserFavViewSet, LeavingMessageViewSet, AddressViewSet

# 通过router去配置访问路径
router = DefaultRouter()

# 配置goods的Url
router.register(r'goods', GoodsListViewSet, base_name='goods')

# 配置category的Url
router.register(r'categorys', CategoryViewSet, base_name="categorys")

# 配置codes验证码的url
router.register(r'codes', SmsCodeViewSet, base_name="codes")

# 配置hotsearch热搜的url
router.register(r'hotsearchs', HotSearchsViewset, base_name="hotsearchs")

# 配置users验证码的url
router.register(r'users', UserViewSet, base_name="users")

# 配置userfav我的收藏功能url
router.register(r'userfavs', UserFavViewSet, base_name="userfavs")

# 配置Message我的信息功能url
router.register(r'messages', LeavingMessageViewSet, base_name="messages")

# 配置收货地址收藏功能url
router.register(r'address', AddressViewSet, base_name="address")

# 配置购物车功能url
router.register(r'shopcarts', ShoppingCartViewSet, base_name="shopcarts")


urlpatterns = [
    url('^admin/', xadmin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # django-rest-framework自带的token认证模式
    url(r'^api-token-auth/', views.obtain_auth_token),

    # JWT的认证接口
    # url(r'^jwt-auth/', obtain_jwt_token),
    url(r'^login/', obtain_jwt_token),

    # 通过router去配置访问路径
    url(r'^', include(router.urls)),

    # 配置上传资源文件的访问处理函数
    url(r'^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),

    # 生成系统文档的配置方法
    url(r'^docs/', include_docs_urls(title='线上生鲜超市')),

]
