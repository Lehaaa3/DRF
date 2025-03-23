from django.urls import path

from users.apps import UsersConfig
from users.views import PaymentsListApiView

app_name = UsersConfig.name

urlpatterns = [
    path('payments/', PaymentsListApiView.as_view(), name='payments-list'),
]
