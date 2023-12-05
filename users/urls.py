from django.urls import path, include
from .views import UserViewSet, SignUpView, FeedbackCRUD
from rest_framework.routers import SimpleRouter

router_user = SimpleRouter()
router_user.register(r'userlist', UserViewSet)

router_feedback = SimpleRouter()
router_feedback.register(r'feedbacklist', FeedbackCRUD)

urlpatterns = [
    path('', include(router_user.urls)),
    path('my_profile/', UserViewSet.as_view({'get': 'my_profile'})),
    path('user_registration/', SignUpView.as_view(), name='user_registration'),

    path('', include(router_feedback.urls)),
    path('feedbacklist/byuserid/<int:user_id>/', FeedbackCRUD.as_view({'get': 'byuserid'})),
    path('feedbacklist/delete_by_userid/<int:user_id>/', FeedbackCRUD.as_view({'delete': 'delete_by_userid'})),

]
