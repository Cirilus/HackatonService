from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework_simplejwt.views import TokenVerifyView, TokenObtainPairView, TokenRefreshView
from rest_framework.routers import SimpleRouter

from Score.views import *



router_history_point = SimpleRouter()
router_history_point.register(r'historypointlist', HistoryPointByUserCRUD)

router_point_condition = SimpleRouter()
router_point_condition.register(r'pointconditionlist', PointConditionByUserCRUD)
print(router_history_point.urls)


urlpatterns = [
    path('api/v1/', include(router_point_condition.urls)), #http://127.0.0.1:8000/api/v1/pointconditionlist/ (<int:pk>/)
    path('api/v1/', include(router_history_point.urls)),  # http://127.0.0.1:8000/api/v1/historypointlist/ (<int:pk>/)

    #получаем запись из таблицы HistoryPoint по указанному condition_id из таблицы PointCondition
    path('api/v1/historypointlist/bycondition/<int:condition_id>/', HistoryPointByUserCRUD.as_view({'get': 'bycondition'})),
   
    #получаем все записи из таблицы HistoryPoint по указанному user_id 
    path('api/v1/historypointlist/byuserid/<int:user_id>/', HistoryPointByUserCRUD.as_view({'get': 'byuserid'})),

    #получаем все записи из таблицы PointCondition по указанному user_id 
    path('api/v1/pointconditionlist/byuserid/<int:user_id>/', PointConditionByUserCRUD.as_view({'get': 'byuserid'})),

]

