from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated

from users.models import Payments, User
from users.serializers import PaymentsSerializer, UserSerializer, UserRegistrationSerializer, PaymentsCreateSerializer
from users.services import get_stripe_price, get_stripe_session


class PaymentsListApiView(generics.ListAPIView):
    queryset = Payments.objects.all()
    serializer_class = PaymentsSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['paid_course', 'paid_lesson', 'payment_way']
    ordering_fields = ['payment_date']


class PaymentsCreateApiView(generics.CreateAPIView):
    queryset = Payments.objects.all()
    serializer_class = PaymentsCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        paid_course = serializer.validated_data.get('paid_course')
        if paid_course:
            payment = paid_course.payment
        else:
            paid_lesson = serializer.validated_data.get('paid_lesson')
            payment = paid_lesson.payment

        price = get_stripe_price(payment)
        payment_url = get_stripe_session(price)

        payment = serializer.save(user=self.request.user, payment=payment, payment_url=payment_url)
        payment.save()


class UserListApiView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class UserRetrieveApiView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class UserCreateApiView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer


class UserUpdateApiView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class UserDestroyApiView(generics.DestroyAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
