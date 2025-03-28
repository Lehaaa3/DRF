from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

from users.apps import UsersConfig
from users.views import PaymentsListApiView, UserListApiView, UserRetrieveApiView, UserCreateApiView, UserUpdateApiView, \
    UserDestroyApiView, UserCreateApiView, PaymentsCreateApiView

app_name = UsersConfig.name

urlpatterns = [
    # token urls
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # user urls
    path('', UserListApiView.as_view(), name='user-list'),
    path('<int:pk>/', UserRetrieveApiView.as_view(), name='user-detail'),
    path('create/', UserCreateApiView.as_view(), name='user-create'),
    path('update/<int:pk>/', UserUpdateApiView.as_view(), name='user-update'),
    path('delete/<int:pk>/', UserDestroyApiView.as_view(), name='user-delete'),
    path('register/', UserCreateApiView.as_view(), name='register'),

    # payments urls
    path('payments/', PaymentsListApiView.as_view(), name='payments-list'),
    path('payments/create/', PaymentsCreateApiView.as_view(), name='payments-create'),
]
