from django.core.management.base import BaseCommand
from users.models import User  # Импорт вашей модели пользователя
from django.contrib.auth.models import Group


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


class CommandModerators(BaseCommand):
    help = 'Проверить пользователей в группе "Модераторы" и добавить их в базу данных, если они отсутствуют'

    def handle(self, *args, **kwargs):
        group_name = "Модераторы"

        # Получаем или создаем группу "Модераторы"
        group, created = Group.objects.get_or_create(name=group_name)
        if created:
            self.stdout.write(self.style.SUCCESS(f'Группа "{group_name}" успешно создана.'))
        else:
            self.stdout.write(self.style.WARNING(f'Группа "{group_name}" уже существует.'))

        # Получаем пользователей в группе "Модераторы"
        moderators = User.objects.filter(groups=group)

        if not moderators.exists():
            self.stdout.write(self.style.WARNING(f'В группе "{group_name}" нет пользователей.'))
        else:
            for user in moderators:
                self.stdout.write(self.style.SUCCESS(f'Пользователь "{user.email}" уже в группе "{group_name}".'))

        self.stdout.write(self.style.SUCCESS('Команда выполнена успешно.'))
