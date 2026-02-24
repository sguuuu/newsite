"""
Команда для создания тестовых данных.
Запуск: python manage.py seed
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import date, timedelta


class Command(BaseCommand):
    help = 'Создаёт тестовые данные для разработки'

    def handle(self, *args, **options):
        from django.contrib.auth import get_user_model
        from apps.events.models import Event, EventRegistration, JuryAssignment
        from apps.notifications.models import Notification

        User = get_user_model()

        self.stdout.write('Создание пользователей...')

        admin, _ = User.objects.get_or_create(
            email='admin@finansy.ru',
            defaults={
                'first_name': 'Иван',
                'last_name': 'Петров',
                'role': 'admin',
                'is_staff': True,
                'is_superuser': True,
            },
        )
        admin.set_password('admin123')
        admin.save()

        teacher, _ = User.objects.get_or_create(
            email='teacher@finansy.ru',
            defaults={
                'first_name': 'Мария',
                'last_name': 'Сидорова',
                'role': 'teacher',
                'institution': 'МБОУ Гимназия №1',
                'grade_or_position': 'Учитель экономики',
            },
        )
        teacher.set_password('teacher123')
        teacher.save()

        participant, _ = User.objects.get_or_create(
            email='student@finansy.ru',
            defaults={
                'first_name': 'Алексей',
                'last_name': 'Иванов',
                'role': 'participant',
                'institution': 'МБОУ Гимназия №1',
                'grade_or_position': '10А',
                'teacher': teacher,
            },
        )
        participant.set_password('student123')
        participant.save()

        jury, _ = User.objects.get_or_create(
            email='jury@finansy.ru',
            defaults={
                'first_name': 'Елена',
                'last_name': 'Козлова',
                'role': 'jury',
                'institution': 'НИУ ВШЭ',
                'grade_or_position': 'Доцент кафедры финансов',
            },
        )
        jury.set_password('jury123')
        jury.save()

        self.stdout.write('Создание мероприятий...')

        today = date.today()

        event1, _ = Event.objects.get_or_create(
            title='Олимпиада по финансовой грамотности 2025',
            defaults={
                'description': 'Ежегодная олимпиада для школьников по основам финансовой грамотности.',
                'short_description': 'Всероссийская олимпиада по финансовой грамотности',
                'event_type': 'olympiad',
                'status': 'active',
                'format': 'online',
                'start_date': today - timedelta(days=5),
                'end_date': today + timedelta(days=25),
                'registration_deadline': today + timedelta(days=10),
                'max_participants': 500,
                'age_min': 14,
                'age_max': 18,
                'created_by': admin,
            },
        )

        event2, _ = Event.objects.get_or_create(
            title='Конкурс "Молодой инвестор"',
            defaults={
                'description': 'Конкурс проектов по инвестированию и управлению личными финансами.',
                'short_description': 'Конкурс инвестиционных проектов для молодёжи',
                'event_type': 'competition',
                'status': 'upcoming',
                'format': 'hybrid',
                'start_date': today + timedelta(days=15),
                'end_date': today + timedelta(days=60),
                'registration_deadline': today + timedelta(days=10),
                'max_participants': 200,
                'age_min': 16,
                'age_max': 25,
                'created_by': admin,
            },
        )

        self.stdout.write('Создание регистраций...')

        EventRegistration.objects.get_or_create(
            event=event1,
            participant=participant,
            defaults={'status': 'active', 'completion_percentage': 60},
        )

        self.stdout.write('Создание назначений жюри...')

        JuryAssignment.objects.get_or_create(
            jury=jury,
            event=event1,
        )

        self.stdout.write('Создание уведомлений...')

        Notification.objects.get_or_create(
            recipient=participant,
            title='Добро пожаловать!',
            defaults={
                'message': 'Вы успешно зарегистрировались на платформе.',
                'notif_type': 'system',
            },
        )

        self.stdout.write(self.style.SUCCESS('\nТестовые данные созданы!\n'))
        self.stdout.write('Учётные данные:')
        self.stdout.write('  Администратор:  admin@finansy.ru     / admin123')
        self.stdout.write('  Педагог:        teacher@finansy.ru  / teacher123')
        self.stdout.write('  Участник:       student@finansy.ru  / student123')
        self.stdout.write('  Жюри:           jury@finansy.ru     / jury123')
