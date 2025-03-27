from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from users.models import Payments, User
from users.services import get_stripe_price, get_stripe_session


class PaymentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payments
        fields = '__all__'


class PaymentsCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payments
        fields = '__all__'
        read_only_fields = ['user', 'payment']

    def validate(self, data):
        if not data['paid_course'] and not data['paid_lesson']:
            raise serializers.ValidationError("одно из полей 'paid_course' или 'paid_lesson' должно быть указано")
        if data['paid_course'] and data['paid_lesson']:
            raise serializers.ValidationError(
                "Только одно из полей 'paid_course' или 'paid_lesson' должно быть указано")
        return data


class UserSerializer(serializers.ModelSerializer):
    country = serializers.CharField(source='country.name')

    class Meta:
        model = User
        fields = '__all__'


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2')

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password": "Введенные пароли не совпадают"})
        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password')
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
        )
        user.password = make_password(password)
        user.save()
        return user
