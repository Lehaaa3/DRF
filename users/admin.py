from django.contrib import admin

from users.models import User, Payments


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'avatar', 'is_staff', 'is_superuser',)


@admin.register(Payments)
class PaymentsAdmin(admin.ModelAdmin):
    list_display = ('user', 'payment_date', 'paid_course', 'paid_lesson', 'payment', 'payment_way',)
