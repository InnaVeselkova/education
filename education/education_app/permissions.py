from rest_framework.permissions import BasePermission, SAFE_METHODS


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
        if not request.user or not request.user.is_authenticated:
            return False

        if request.method in SAFE_METHODS:
            return True

        # запрещаем изменение администраторам и модераторам
        if request.user.is_staff:
            return False
        if request.user.groups.filter(name='Модераторы').exists():
            return False

        return True


class IsOwner(BasePermission):
    """
    Разрешение, позволяющее доступ только владельцам объекта.
    """

    def has_object_permission(self, request, view, obj):
        # Проверяем, является ли текущий пользователь владельцем объекта
        return obj.owner == request.user