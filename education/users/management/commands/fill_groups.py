from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from users.models import User  # Импорт вашей модели пользователя


class Command(BaseCommand):
    help = 'Заполняет базу данных пользователями и отображает их группы'

    def handle(self, *args, **kwargs):
        # Получаем все группы
        groups = Group.objects.all()

        if not groups:
            self.stdout.write(self.style.ERROR('Нет доступных групп!'))
            return

        self.stdout.write(self.style.SUCCESS('Пользователи и их группы:\n'))

        # Проходим по всем пользователям
        for user in User.objects.all():
            user_groups = user.groups.all()  # Получаем группы для пользователя
            group_names = ', '.join([group.name for group in user_groups]) if user_groups else 'Нет групп'
            self.stdout.write(f'Пользователь: {user.email} - Группы: {group_names}')
