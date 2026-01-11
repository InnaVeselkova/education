from rest_framework.permissions import BasePermission

class IsModeratorOrAdmin(BasePermission):
    """
    Разрешение, позволяющее доступ только модераторам или администраторам.
    """

    def has_permission(self, request, view):
        # Проверяем, является ли пользователь администратором или модератором
        if request.user.is_staff:  # Проверка на администраторские права
            return True
        return request.user.groups.filter(name='Модераторы').exists() # Проверка на принадлежность к группе "Модераторы"
