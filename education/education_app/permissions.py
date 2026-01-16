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


class IsNotModeratorOrAdmin(BasePermission):
    """
    Разрешение, запрещающее доступ для модераторов и администраторов
    к действиям, связанным с изменением курсов.
    """

    def has_permission(self, request, view):
        # Разрешаем доступ всем, кроме администраторов и модераторов при изменении
        if request.user.is_staff:  # Если пользователь администратор
            return view.action not in ['update', 'partial_update', 'destroy']
        return not request.user.groups.filter(name='Модераторы').exists()


class IsOwner(BasePermission):
    """
    Разрешение, позволяющее доступ только владельцам объекта.
    """

    def has_object_permission(self, request, view, obj):
        # Проверяем, является ли текущий пользователь владельцем объекта
        return obj.owner == request.user