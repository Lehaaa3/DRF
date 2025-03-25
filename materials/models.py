from django.conf import settings
from django.db import models

NULLABLE = {'null': True, 'blank': True}


class Course(models.Model):
    title = models.CharField(max_length=50, verbose_name='название')
    image = models.ImageField(upload_to='courses/', verbose_name='превью', **NULLABLE)
    description = models.TextField(verbose_name='описание')

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='владелец')

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "курс"
        verbose_name_plural = "курсы"
        ordering = ['owner']


class Lesson(models.Model):
    title = models.CharField(max_length=50, verbose_name='название')
    description = models.TextField(verbose_name='описание')
    image = models.ImageField(upload_to='lessons/', verbose_name='превью', **NULLABLE)
    url = models.URLField(verbose_name='ссылка на урок', max_length=200, **NULLABLE)

    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='курс', related_name='lesson')

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='владелец')

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "урок"
        verbose_name_plural = "уроки"
        ordering = ['owner']


class Subscription(models.Model):
    is_subscribed = models.BooleanField(default=False, verbose_name='статус подписки')

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='пользователь',
                             related_name='user')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='курс', related_name='course')
