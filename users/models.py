from django.contrib.auth.models import AbstractUser
from django.db import models
from django_countries.fields import CountryField
import cities_light.models as cities_light

from materials.models import Course, Lesson

NULLABLE = {'null': True, 'blank': True}


class User(AbstractUser):
    avatar = models.ImageField(upload_to='users/', verbose_name='аватар', **NULLABLE)
    email = models.EmailField(unique=True, verbose_name='почта')
    phone = models.CharField(max_length=35, verbose_name='телефон', **NULLABLE)
    country = CountryField(verbose_name='страна', **NULLABLE)
    city = models.ForeignKey(cities_light.City, on_delete=models.SET_NULL, verbose_name='город', **NULLABLE)

    def __str__(self):
        return self.email

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username']


class Payments(models.Model):
    CASH = 'наличные'
    TRANSFER = 'перевод на счет'

    PAYMENT_CHOICES = [
        (CASH, 'наличные'),
        (TRANSFER, 'перевод на счет'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь')
    payment_date = models.DateField(verbose_name='дата оплаты')
    paid_course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='оплаченный курс', **NULLABLE)
    paid_lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name='отдельно оплаченный урок',
                                    **NULLABLE)
    payment = models.PositiveIntegerField(verbose_name='сумма оплаты')
    payment_way = models.CharField(choices=PAYMENT_CHOICES, verbose_name='способ оплаты')
