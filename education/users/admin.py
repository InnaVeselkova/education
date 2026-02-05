from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Payment


# Класс для управления пользователями
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('email', 'is_staff', 'is_active', 'is_superuser')
    list_filter = ('is_staff', 'is_active')
    ordering = ('email',)
    search_fields = ('email', 'phone_number')

    #  поля, которые доступны для редактирования в админке
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'phone_number', 'avatar', 'city')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active', 'is_superuser', 'groups')}
         ),
    )


# Регистрация модели пользователя
admin.site.register(User, CustomUserAdmin)


# Класс для управления платежами
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'payment_date', 'amount', 'payment_method', 'paid_course', 'paid_lesson')
    list_filter = ('payment_method', 'payment_date', 'user')
    search_fields = ('user__email', 'amount')
    ordering = ('-payment_date',)


# Регистрация модели платежей
admin.site.register(Payment, PaymentAdmin)
